#!/usr/bin/env python

import os

import pytest

from .conftest import file_exists, file_exists_and_not_empty


# Note:
# The DESeq2 1.24.0 version in Debian archives
# differs from the DESeq2 1.24.0 version in bioconductor version 3.9
# If estimateDispersions with default fitType="parametric" fails,
# (as often happens with the quickly generated synthetic data from tests),
# it tries to use local fit using the locfit package, but in Debian
# version this is not a valid choice of fit, causing failure.
# Due to this, and since I'm using Debian packages for faster testing
# I'm manually setting fitType="mean" for testing only.


@pytest.fixture
def outputs(atac_analysis):
    output_dir = os.path.join(atac_analysis.results_dir, "differential_analysis_ATAC-seq")
    prefix = os.path.join(output_dir, "differential_analysis.")
    outputs = [
        os.path.join(output_dir, "Factor_a_2vs1"),
        os.path.join(
            output_dir,
            "Factor_a_2vs1",
            "differential_analysis.deseq_result.Factor_a_2vs1.csv",
        ),
        prefix + "comparison_table.tsv",
        prefix + "count_matrix.tsv",
        prefix + "deseq_result.all_comparisons.csv",
        prefix + "experiment_matrix.tsv",
    ]
    return outputs


# @pytest.fixture
# def outputs_no_subdirectories(analysis):
#     output_dir = os.path.join(analysis.results_dir, "differential_analysis_ATAC-seq")
#     prefix = os.path.join(output_dir, "differential_analysis.")
#     outputs = [
#         prefix + "deseq_result.Factor_a_2vs1.csv",
#         prefix + "comparison_table.tsv",
#         prefix + "count_matrix.tsv",
#         prefix + "deseq_result.all_comparisons.csv",
#         prefix + "experiment_matrix.tsv"]
#     return outputs


def test_deseq_functionality():
    import warnings

    import pandas as pd

    from rpy2.rinterface import RRuntimeWarning
    from rpy2.robjects import numpy2ri, pandas2ri
    import rpy2.robjects as robjects

    from ngs_toolkit.utils import recarray2pandas_df

    numpy2ri.activate()
    pandas2ri.activate()
    warnings.filterwarnings("ignore", category=RRuntimeWarning)

    robjects.r('suppressMessages(library("DESeq2"))')
    _makeExampleDESeqDataSet = robjects.r("DESeq2::makeExampleDESeqDataSet")
    _estimateSizeFactors = robjects.r("DESeq2::estimateSizeFactors")
    _estimateDispersions = robjects.r("DESeq2::estimateDispersions")
    _nbinomWaldTest = robjects.r("DESeq2::nbinomWaldTest")
    _DESeq = robjects.r("DESeq2::DESeq")
    _results = robjects.r("DESeq2::results")
    _as_data_frame = robjects.r("as.data.frame")

    dds = _makeExampleDESeqDataSet()
    dds = _estimateSizeFactors(dds)
    dds = _estimateDispersions(dds)
    dds = _nbinomWaldTest(dds)
    res = recarray2pandas_df(_as_data_frame(_results(dds)))
    assert isinstance(res, pd.DataFrame)

    dds = _makeExampleDESeqDataSet()
    dds = _DESeq(dds)
    res = recarray2pandas_df(_as_data_frame(_results(dds)))
    assert isinstance(res, pd.DataFrame)


class Test_differential_analysis:
    def test_simple_design(self, atac_analysis, outputs):
        import pandas as pd

        atac_analysis.differential_analysis(
            filter_support=False, deseq_kwargs={"fitType": "mean"})
        assert file_exists(
            os.path.join(atac_analysis.results_dir, "differential_analysis_ATAC-seq")
        )
        assert file_exists(outputs[0])
        assert os.path.isdir(outputs[0])
        for output in outputs[1:]:
            assert file_exists_and_not_empty(output)
        assert hasattr(atac_analysis, "differential_results")
        assert isinstance(atac_analysis.differential_results, pd.DataFrame)
        assert atac_analysis.differential_results.index.str.startswith("chr").all()
        assert atac_analysis.differential_results.index.name == "index"
        cols = [
            "baseMean",
            "log2FoldChange",
            "lfcSE",
            "stat",
            "pvalue",
            "padj",
            "comparison_name",
        ]
        assert atac_analysis.differential_results.columns.tolist() == cols

    def test_complex_design(self, atac_analysis, outputs):
        import pandas as pd

        atac_analysis.differential_analysis(
            filter_support=False, deseq_kwargs={"fitType": "mean"})
        assert file_exists(
            os.path.join(atac_analysis.results_dir, "differential_analysis_ATAC-seq")
        )
        assert file_exists(outputs[0])
        assert os.path.isdir(outputs[0])
        for output in outputs[1:]:
            assert file_exists_and_not_empty(output)
        assert hasattr(atac_analysis, "differential_results")
        assert isinstance(atac_analysis.differential_results, pd.DataFrame)
        assert atac_analysis.differential_results.index.str.startswith("chr").all()
        assert atac_analysis.differential_results.index.name == "index"
        cols = [
            "baseMean",
            "log2FoldChange",
            "lfcSE",
            "stat",
            "pvalue",
            "padj",
            "comparison_name",
        ]
        assert atac_analysis.differential_results.columns.tolist() == cols

    # def test_no_subdirectories(self, atac_analysis, outputs):
    #     atac_analysis.differential_analysis()
    #     assert file_exists(
    #         os.path.join(atac_analysis.results_dir, "differential_analysis_ATAC-seq"))
    #     assert file_exists(outputs[0])
    #     assert os.path.isdir(outputs[0])
    #     for output in outputs[1:]:
    #         assert file_exists(output)
    #         assert os.stat(output).st_size > 0
