ODM2 Python API
====

A Python-based application programmer's interface for the [Observations Data Model 2 (ODM2)](http://odm2.org).

[List of current and planned functions included in the API](https://github.com/ODM2/ODM2PythonAPI/blob/master/doc/APIFunctionList.md)

## Installation

The easiest and most reliable way to install the ODM2 Python API (`odm2api`) is using the [Conda package management system](http://conda.pydata.org/docs/) via either [Anaconda](https://www.continuum.io/downloads) or [Miniconda](http://conda.pydata.org/miniconda.html). To start using conda (if it's not your system default), add conda to the PATH; on MacOSX and Linux, it's something like `export PATH=$HOME/miniconda/bin:$PATH`, but the exact path may vary.

To activate a conda environment, say, "myenv":
```bash
activate myenv  # On Windows
source activate myenv  # On MacOSX or Linux
```

**Note:** `odm2api` currently is only tested on Python 2.7. Some changes have been made to support Python 3.x, but they haven't been tested thoroughly.


### Latest release, from ODM2 anaconda.org channel

The [latest `odm2api` release](https://github.com/ODM2/ODM2PythonAPI/releases) is available on the [ODM2 anaconda.org channel](https://anaconda.org/odm2/odm2api) for all major OS paltforms (linux, OSX, win32/win64). To install it on an existing conda environment:
```
conda install -c odm2 odm2api
```
All dependencies are installed, including Pandas and its dependencies (numpy, etc).

To create a new environment "myenv" with the `odm2api` package:
```
conda create -n myenv -c odm2 python=2.7 odm2api
```

### Installing the development version from the `master` branch on github

**Note from 4/26/2016:** These instructions may be slightly outdated. Follow these directions for installing the bleeding edge github master branch, mainly for development and testing purposes.

To create a new environment "myenv" with `odm2api`, first download the conda environment file [condaenvironment_1.yml](https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/condaenvironment_1.yml). Go to the directory where `condaenvironment_1.yml` was downloaded. Then, on a terminal shell:
```bash
conda env create -n myenv --file py2_conda_environment.yml
```
Activate the new environment, then install `odm2api` into the environment:
```bash
activate myenv  # On Windows
source activate myenv  # On MacOSX or Linux

pip install --process-dependency-links git+https://github.com/ODM2/ODM2PythonAPI.git
```

## Credits

This work was supported by National Science Foundation Grants [EAR-1224638](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1224638) and [ACI-1339834](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1339834). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
