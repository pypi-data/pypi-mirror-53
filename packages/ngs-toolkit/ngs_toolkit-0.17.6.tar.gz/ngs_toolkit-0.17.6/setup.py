#! /usr/bin/env python

import sys
import os
import glob


def parse_requirements(req_file):
    requirements = open(req_file).read().strip().split("\n")
    requirements = [r for r in requirements if not r.startswith("#")]
    return [r for r in requirements if "#egg=" not in r]


# take care of extra required modules depending on Python version
extra = {}
try:
    from setuptools import setup, find_packages

    if sys.version_info < (2, 7):
        extra["install_requires"] = ["argparse"]
    if sys.version_info >= (3,):
        extra["use_2to3"] = True
except ImportError:
    from distutils.core import setup

    if sys.version_info < (2, 7):
        extra["dependencies"] = ["argparse"]

# Requirements
requirements = parse_requirements(
    "requirements/requirements.txt")
test_requirements = parse_requirements(
    "requirements/requirements.test.txt")
requirements_sc = parse_requirements(
    "requirements/requirements.single_cell.txt")

# Recipes
recipes = glob.glob(
    os.path.join(os.path.curdir, "ngs_toolkit", "recipes", "*.py"))
recipes = list(
    map(
        lambda x: x.replace(".py", "").replace("./", "").replace("/", "."),
        recipes)
)
recipes = [
    " = ".join([i, j + ":main"])
    for i, j in zip(map(lambda x: x.split(".")[-1], recipes), recipes)
]
recipes = [r for r in recipes if not r.startswith("__init__")]

long_description = open("README.md").read()


# setup
setup(
    name="ngs_toolkit",
    packages=find_packages(),
    use_scm_version={
        'write_to': 'ngs_toolkit/_version.py',
        'write_to_template': '__version__ = "{version}"\n'
    },
    entry_points={
        "console_scripts": [
            "projectmanager = ngs_toolkit.project_manager:main",
            "trackmanager = ngs_toolkit.track_manager:main",
        ] + recipes
    },
    description="A toolkit for NGS analysis with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="bioinformatics, sequencing, ngs, ngs analysis, "
             "ATAC-Seq, ChIP-seq, RNA-seq, project management",
    url="https://github.com/afrendeiro/toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/afrendeiro/toolkit/issues",
        "Documentation": "https://ngs-toolkit.readthedocs.io",
        "Source Code": "https://github.com/afrendeiro/toolkit",
    },
    author=u"Andre Rendeiro",
    author_email="andre.rendeiro@pm.me",
    license="GPL3",
    setup_requires=['setuptools_scm'],
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require={
        "testing": test_requirements,
        "single_cell": requirements_sc},
    package_data={"ngs_toolkit": ["config/*.yaml", "templates/*.html"]},
    data_files=[
        "requirements/requirements.txt",
        "requirements/requirements.test.txt",
        "requirements/requirements.single_cell.txt",
    ],
    **extra
)
