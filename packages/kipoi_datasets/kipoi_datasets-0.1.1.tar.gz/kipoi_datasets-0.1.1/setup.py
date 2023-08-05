#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    "kipoi-utils>=0.1.12",
    "kipoiseq",
    "genomelake",
    "numpy",
    "pandas",
    "tqdm",
]

test_requirements = [
    "bumpversion",
    "wheel",
    "epc",
    "jedi",
    "pytest>=3.3.1",
    "pytest-xdist",  # running tests in parallel
    "pytest-pep8",  # see https://github.com/kipoi/kipoi/issues/91
    "pytest-cov",
    "coveralls",
    "keras",
    "tensorflow",
    "pybedtools"
]

setup(
    name='kipoi_datasets',
    version='0.1.1',
    description="kipoi_datasets: training datasets for genomics",
    author="Kipoi team",
    author_email='avsec@in.tum.de',
    url='https://github.com/kipoi/datasets',
    long_description="kipoi_datasets: training datasets for genomics",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "develop": test_requirements,
    },
    license="MIT license",
    zip_safe=False,
    keywords=["model zoo", "deep learning",
              "computational biology", "bioinformatics", "genomics"],
    test_suite='tests',
    include_package_data=False,
    tests_require=test_requirements
)
