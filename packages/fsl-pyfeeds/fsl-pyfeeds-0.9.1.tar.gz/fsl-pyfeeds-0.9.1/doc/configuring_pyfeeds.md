# Configuring `pyfeeds`


 * [Specifying file tests](#specifying-file-tests)
 * [Excluding files](#excluding-files)
 * [Specifying tolerances](#specifying-tolerances)
 * [Self-evaluating tests](#self-evaluating-tests)
 * [`pyfeeds` configuration file](#pyfeeds-configuration-file)


---


This page gives an overview of the main options for controlling how `pyfeeds`
runs and evaluates tests.


## Specifying file tests


Most `pyfeeds` tests simply generate some output which is then compared by
`pyfeeds` against some pre-defined benchmark output. The way in which
`pyfeeds` compares files can be configured by specifying a file name pattern,
and one or more *evaluation routines*.



By default, the MD5 hash of each file is calculated, and compared with that of
the corresponding benchmark file. But you can choose from several other
evaluation routines, using the `--evalRoutines` (`-e`) command-line argument.


For example, to specify that all `.nii.gz` images are evaluated using the
`evalImage` function:


```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -e "*.nii.gz=evalImage" \
    examples
```


You can specify that multiple evaluation routines should be used for each file
type by separating the routine names with a comma, e.g.:


```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -e "*.nii.gz=evalImage,evalHeader" \
    examples
```


Separate different file types with a semi-colon character, e.g.:



```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -e "*.nii.gz=evalImage:*.txt=evalNumericalText" \
    examples
```


A list of available evaluation routines is given in the command line help for
the `run` and `compare` sub-commands:


```
$ pyfeeds run     --help
$ pyfeeds compare --help
```


## Excluding files


If your tests generate output files that you do not care about and hence do
not want to be evaluated, you can exclude them via the `--exclude` (`-x`)
command-line argument. For example, to ignore all `.log` and `.tmp` files:


```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -x "*.log:*.tmp" \
    examples
```


In the event of a file matching a pattern specified in both the `--exclude`
option and the `--evalRoutines` option, the `--exclude` option will take
precedence.


## Specifying tolerances


For each test output file, all of the built-in evaluation routines will, in
principle, produce a value between 0 and 1 which represents the difference
between the file and its corresponding benchmark file. Values closer to 0
indicate a smaller difference, and values closer to 1 indicate a larger
difference. By default, files which produce a value smaller than or equal
to 0.05 will be deemed acceptable, whereas files with an error value greater
than 0.05 will cause the test to fail.


The default tolerance can be changed via the `--defaultTolerance` (`-d`)
command-line option. It is also possible to specify different tolerances for
different file types via the `--tolerances` (`-t`) option, for example:

```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -d 0.01 \
    -t "*.nii.gz=0.05:*.txt=0.02" \
    examples
```


## Self-evaluating tests


The evaluation process performed by `pyfeeds` may not be suitable for some
tests, for example those which produce highly non-deterministic outputs. Tests
such as this can evaluate their own output - this can simply be implemented in
the `feedsRun` script. These self-evaluating tests can be marked as such via
the `--selfEval` (`-s`) command-line option.


The test output-benchmark file evaluation will be skipped for all tests that
have been marked as self-evaluating.


```
$ pyfeeds run \
    -i exampleInputData \
    -b exampleBenchmarkData \
    -o exampleOutput \
    -s "selfEvalTest1:selfEvalTest2" \
    examples
```


## `pyfeeds` configuration file


All `pyfeeds` command-line options can be specified in a configuration file,
rather than on the command-line. A `pyfeeds` configuration file is an
`.ini`-style file which contains three sections:


 - `general`: All arguments except for `--evalRoutines` and `--tolerances`
 - `evalRoutines`: Evaluation routines to use for different file types.
 - `tolerances`: Error tolerances to use for different file types.


The [`examplePyfeedsConfig`](./examplePyfeedsConfig) file is an example of a
typical `pyfeeds` configuration file.
