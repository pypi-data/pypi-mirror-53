<!--
# THIS FILE IS EXCLUSIVELY MAINTAINED IN THE AE ROOT PACKAGE. ANY CHANGES SHOULD BE DONE THERE.
# All changes will be deployed automatically to all the portions of this namespace package.
-->
# Version 0.0.5 Of ae_core Package

The modules and sub-packages of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.


## Installation

For to only use this sub-package in your code type in your command shell:
 
```shell script
pip install ae-core
```

If you instead want to contribute to this sub-package then first fork this repository,
then pull it to your machine and then execute in the root folder of this repository:

```shell script
pip install -e .[dev]
```

The last command will install this sub-package into your virtual environment, along with
the tools you need to develop and run tests or for to extend the sub-package documentation.
For to contribute only to the unit tests or the documentation of this sub-package replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## Sub-Package Documentation

More info on the features and usage of this sub-package are available at
[ReadTheDocs](https://ae-core.readthedocs.io "ae_core documentation").
