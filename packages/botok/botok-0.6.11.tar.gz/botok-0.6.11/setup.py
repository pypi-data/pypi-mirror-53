#! /usr/bin/env python
# coding: utf8

from __future__ import print_function

from pathlib import Path
import setuptools
from pkg_resources import parse_version

assert parse_version(setuptools.__version__) >= parse_version("38.6.0")


def read(fname):
    p = Path(__file__).parent / fname
    with p.open(encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="botok",
    version="0.6.11",  # also edit version in botok/__init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Tibetan Word Tokenizer",
    license="Apache2",
    keywords="nlp computational_linguistics tibetan tokenizer token",
    url="https://github.com/Esukhia/botok",
    packages=setuptools.find_packages(),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/Esukhia/botok",
        "Tracker": "https://github.com/Esukhia/botok/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Tibetan",
    ],
    package_data={
        "botok": [
            "resources/*",
            "resources/lexica_bo/*",
            "resources/frequency/*",
            "resources/entry_data/*",
            "resources/lexica_non_inflected/*",
            "resources/lemmas/*",
            "resources/rules/*",
            "resources/lexica_skrt/*",
            "resources/adjustment/*",
        ]
    },
    python_requires=">=3.6",
    tests_require=["pytest"],
    install_requires=["pyyaml"],
)
