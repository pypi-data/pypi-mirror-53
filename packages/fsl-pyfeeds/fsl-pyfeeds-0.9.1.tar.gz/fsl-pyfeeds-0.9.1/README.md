# `pyfeeds`


[![PyPi version](https://img.shields.io/pypi/v/fsl-pyfeeds.svg)](https://pypi.python.org/pypi/fsl-pyfeeds/) [![Anaconda version](https://anaconda.org/conda-forge/fsl-pyfeeds/badges/version.svg)](https://anaconda.org/conda-forge/fsl-pyfeeds/)
[![Coverage report](https://git.fmrib.ox.ac.uk/fsl/pyfeeds/badges/master/coverage.svg)](https://git.fmrib.ox.ac.uk/fsl/pyfeeds/commits/master)

## The FSL Evaluation and Example Data Suite (FEEDS), now in Python!


`pyfeeds` (the FMRIB Evaluation and Example Data Suite) is a framework for
running and managing tests for the FSL code base.


### Test writers

If you want to write a test for your project, check out the page on [how to
write a `pyfeeds` test](doc/writing_a_test.md).


### `pyfeeds` users


If you are going to be running `pyfeeds` tests, or are just interested, check
out these pages:

  - [Using `pyfeeds`](doc/using_pyfeeds.md)
  - [Configuring `pyfeeds`](doc/configuring_pyfeeds.md)
  - [How `pyfeeds` works](doc/how_pyfeeds_works.md)


### Running the example tests


To run the examples included with `pyfeeds`, you will need
[FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/) 5.0.9 or newer installed, and
you will need to download the example and benchmark data sets from the
`pyfeeds` [git repository](https://git.fmrib.ox.ac.uk/fsl/pyfeeds).

Use the following commands to run the tests:

    exprs="*.nii.gz=evalImage"
    exprs="$exprs:dti_V?.nii.gz=evalVectorImage"
    exprs="$exprs:*.txt=evalNumericalText"
    exprs="$exprs:*.mat=evalNumericalText"
    pyfeeds run -e "$exprs" \
        -i exampleInputData \
        -b exampleBenchmarkData \
        -o exampleOutput examples

| Note that the FEAT example test may not pass for you, as different versions
| of FSL may produce slightly different results.
