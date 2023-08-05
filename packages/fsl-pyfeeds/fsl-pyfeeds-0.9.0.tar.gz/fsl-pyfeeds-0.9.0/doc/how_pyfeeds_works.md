# How `pyfeeds` works

 * [Test directories](#test-directories)
 * [External/shared data](#externalshared-data)
 * [Test bundles](#test-bundles)
 * [Tracking changes to tests and data](#tracking-changes-to-tests-and-data)


## Test directories


`pyfeeds` expects to be provided with one or more input directories, in which
a set of tests are contained. These tests can be located anywhere within the
input directory, i.e. nested arbitrarily deep within the input directory
tree. However, each test must be contained within its own sub-directory.  Each
test sub-directory may contain data, libraries, code, etc, but must contain an
executable file called `feedsRun`, or multiple executable files, each with a
different suffix, e.g. `feedsRun.test1`, `feedsRun.test2`, etc. For example,
a typical `pyfeeds` test directory might look like this:


```
$ ls examples/flirt/

examples/flirt/feedsRun
examples/flirt/input.nii.gz
examples/flirt/xform.mat

$
```


Each `feedsRun` script is executed with the following parameters (see the page
on [Writing a test](writing_a_test.md) for an overview of the parameters):


```
$ ./feedsRun outputDir dataDir benchmarkDir
```


When `pyfeeds` runs a test, it creates an output directory for the test (as a
sub-directory of the `--outputDir` argument passed to the `pyfeeds` `run`
command), and checks for the existence of a `feedsInput` file in the test
directory. If this file does not exist, the test `feedsRun` file is simply
executed. Otherwise a test *sandbox* directory is created as described in the
next section - the test is passed this sandbox as its data directory.


## External/shared data


`pyfeeds` tests can be either self-contained (i.e. the data they use lives
alongside the `feedsRun` script in the test sub-directory), or they can be
dependent upon some external data. All external data used by any `pyfeeds` test
lives in a data directory, organised into logical sub-directories (each of
which may be locally stored, or symlinked):


```
$ ls exampleInputData/

exampleInputData/dti/
exampleInputData/exampleData/
exampleInputData/feat/
exampleInputData/flirt/

$
```

A test which relies upon an external data set *must* specify which data they
use, via a text file called `feedsInputs`, stored alongside the `feedsRun`
script:


```
$ ls examples/flirt_shared/

examples/flirt_shared/feedsRun
examples/flirt_shared/feedsInputs

$
```


The ``feedsInputs`` file simply contains a list of file/directory names,
specifying the files/directories that are used by the test. The names are
specified relative to the root of the data directory - for example, a
`feedsInputs` file may look like this (leading/trailing slashes on directories
are optional):


```
$ cat examples/flirt_shared/feedsInputs

flirt/input.nii.gz
flirt/xform.mat

$
```


But will (probably) more realistically be a bit simpler - for example, a test
called FEAT may have its own data directory, in which case the `feedsInputs`
file for the FEAT test would simply contain:


```
$ cat examples/feat/feedsInputs

feat/

$
```


When `pyfeeds` runs a test which depends upon external data, all of the
files/directories listed in `feedInputs` are copied/symlinked into a *sandbox*
directory, which is passed as the `dataDir` parameter to the test script.


## Test bundles


The `pyfeeds` `bundle` command is used to extract all detected tests and copy
them, and their external data dependencies, into a new directory - a
*bundle*. This is useful if you want to create a sub-set of *standalone* tests
to be executed in another location. A bundle is standalone because the
`bundle` command creates a copy of all of the input and benchmark data that is
required by the tests included in the bundle.


When you use the `bundle` command, you must specify a directory in which the
bundle is to be created. For example, say we want to create a test bundle for
all FLIRT-related tests:


```
$ pyfeeds bundle -i exampleInputData     \
                 -b exampleBenchmarkData \
                 -o myBundle             \
                 examples/flirt          \
                 examples/flirt_shared   \
                 examples/nested/flirt

2015-11-26 15:30:36,608 INFO - Adding flirt to bundle...
2015-11-26 15:30:36,610 INFO - Adding flirt_shared to bundle...
2015-11-26 15:30:36,615 INFO - Adding nested/flirt to bundle...

$
```

 > You can use the `-g` flag to generate a hash file, which will be included
 > in the bundle.


The `bundle` command creates this directory and organises it so it has the
following structure:


```
$ ls myBundle

benchmarks/
data/
tests/

$
```

The `myBundle/data/` directory contains the input data required by all of the
tests that have been included in the bundle. The `myBundle/benchmarks/`
directory contains the benchmark data for each test. The `myBundle/tests/`
directory contains one sub-directory for every test included in the bundle;
the directory for each test is given a unique name, based upon its original
location:


```
$ tree myBundle/tests

bundle/tests
├── flirt
│   ├── feedsRun
│   ├── input.nii.gz
│   └── xform.mat
├── flirt_shared
│   ├── feedsInputs
│   └── feedsRun
└── nested
    └── flirt
        └── feedsRun

$
```


So once you have created a bundle (e.g. ``myBundle``), you can run the tests
contained within with a command such as the following:

```
$ cd myBundle
$ pyfeeds run -i data -b benchmarks -o bundleTestOutput tests
```


## Tracking changes to tests and data


`pyfeeds` keeps track of changes to tests and to test data, and outputs a
warning when it detects that a test (or its data) has changed since it was
last executed.  When `pyfeeds` runs a test, it calculates an MD5 digest upon
the contents of test directory. For all tests with a `feedsInput` file,
`pyfeeds` also calculates a MD5 digest upon all of the files and directories
listed in `feedsInputs`.  The digests for each test are stored in a file
(called `.feedsHashes`, and located in the `--inputDir` directory by default;
a different location can be specified via the `--hashFile` argument). This
file looks something like the following:


```
$ cat exampleInputData/.feedsHashes

db96c131504ba709dfe9a6c4af5c7a2a c1333ef13d031be5fc29365e34e551a2
d27e3cda6a2dc1c737fd014fddc5813b None
0eaf79d5c4988e9686de808f5634cec6 7867f5598930ce992e6e5a0c49f44ea4
06182094c1e82e46e0e6c2050c650ac6 b3039335d985e68e11a44bb5e997f6db
323e035aef25b6744c0dc18daec4b36e None
20b6f482c2cc64af2b800ac0f61a422f None
b6000201f7daff9d0e9f98a0963c99e6 1cc970e2700c119874dbf304bacc6cc4

$
```


The digests in the first column are those calculated upon each test directory,
and the digests in the second column are those calculated upon the input data
for each test. A value of `None` in the second column indicates that this
particular test does not depend upon any external data.  When a test is run,
its test and data digest values are calculated and compared against the
digests contained in the `.feedsHashes` file.  If the digests do not match, a
warning is output, but the test is still executed.


---


The `pyfeeds genhash` command allows you to calculate the digests for a set of
tests:


```
$ pyfeeds genhash  -i exampleInputData/ examples/

Test verification hashes

Test name     | Test directory hash              | Test data hash
------------- | -------------------------------- | --------------------------------
call_cmd      | b6000201f7daff9d0e9f98a0963c99e6 | 1cc970e2700c119874dbf304bacc6cc4
csv_data      | 323e035aef25b6744c0dc18daec4b36e | None
feat          | 06182094c1e82e46e0e6c2050c650ac6 | b3039335d985e68e11a44bb5e997f6db
flirt         | d27e3cda6a2dc1c737fd014fddc5813b | None
flirt_shared  | 0eaf79d5c4988e9686de808f5634cec6 | 7867f5598930ce992e6e5a0c49f44ea4
nested/flirt  | 20b6f482c2cc64af2b800ac0f61a422f | None
nested/ntest1 | 20b6f482c2cc64af2b800ac0f61a422f | None
shared_data   | db96c131504ba709dfe9a6c4af5c7a2a | c1333ef13d031be5fc29365e34e551a2

$
```


If you use the `--hashFile` argument, `genhash` will output the digests to a file,
in the same format as that of the `.feedsHashes` file described above.


---


The `pyfeeds checkhash` command allows you to verify a set of tests without
running them:


```
$ pyfeeds checkhash -i exampleInputData/ examples/

Test verification results

Test name     | Verification test result
------------- | ------------------------------------------
call_cmd      | Passed
csv_data      | Passed (test does not use any shared data)
feat          | Passed
flirt         | Passed (test does not use any shared data)
flirt_shared  | Passed
nested/flirt  | Passed (test does not use any shared data)
nested/ntest1 | Passed (test does not use any shared data)
shared_data   | Passed

$
```
