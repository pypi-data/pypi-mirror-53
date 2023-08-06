# RCSB Python Reference Sequence Data Utilities

 [![Build Status](https://dev.azure.com/jdwestbrook/jdwestbrook/_apis/build/status/rcsb.py-rcsb_utils_seq?branchName=master)](https://dev.azure.com/jdwestbrook/jdwestbrook/_build/latest?definitionId=7&branchName=master)

## Introduction

This module contains utility methods for processing linear polymer reference
 sequence data.

### Installation

Download the library source software from the project repository:

```bash

git clone --recurse-submodules https://github.com/rcsb/py-rcsb_utils_seq.git

```

Optionally, run test suite (Python versions 2.7, and 3.7) using
[setuptools](https://setuptools.readthedocs.io/en/latest/) or
[tox](http://tox.readthedocs.io/en/latest/example/platform.html):

```bash
python setup.py test

or simply run

tox
```

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

```bash
pip install rcsb.utils.seq

or for the local repository:

pip install .
```
