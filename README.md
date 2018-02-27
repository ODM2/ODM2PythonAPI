ODM2 Python API
===============

[![Build Status](https://travis-ci.org/ODM2/ODM2PythonAPI.svg?branch=master)](https://travis-ci.org/ODM2/ODM2PythonAPI)
[![Build status](https://ci.appveyor.com/api/projects/status/c13bxn6xvgv5kglt?svg=true)](https://ci.appveyor.com/project/odm2bot/odm2pythonapi)


A Python-based application programmer's interface for the
[Observations Data Model 2 (ODM2)](http://odm2.org).

[List of current and planned functions included in the API](https://github.com/ODM2/ODM2PythonAPI/blob/master/doc/APIFunctionList.md)

## Documentation

For the latest documentation of the ODM2 Python API, see [http://odm2.github.io/ODM2PythonAPI/](http://odm2.github.io/ODM2PythonAPI/)

## Installation

The easiest and most reliable way to install the ODM2 Python API (`odm2api`) is using the
[Conda package management system](http://conda.pydata.org/docs/)
via either
[Anaconda](https://www.continuum.io/downloads)
or
[Miniconda](http://conda.pydata.org/miniconda.html).
To start using conda (if it's not your system default),
add conda to the PATH; on MacOSX and Linux,
it's something like `export PATH=$HOME/miniconda/bin:$PATH`,
but the exact path may vary.

To activate a conda environment, say, "myenv":

```bash
activate myenv  # On Windows
source activate myenv  # On MacOSX or Linux
```

**Note:** `odm2api` currently is only tested on Python 2.7. Some changes have been made to support Python 3.x,
but they haven't been tested thoroughly.


### Latest release, from conda-forge anaconda.org channel

The
[latest `odm2api` release](https://github.com/ODM2/ODM2PythonAPI/releases)
is available on the
[conda-forge anaconda.org channel](https://anaconda.org/conda-forge/odm2api)
for all major OS paltforms (linux, OSX, win32/win64).
To install it on an existing conda environment:

```
conda install -c conda-forge odm2api
```

All dependencies are installed,
including Pandas and its dependencies (numpy, etc).

To create a new environment "myenv" with the `odm2api` package:

```
conda create -n myenv -c conda-forge python=2.7 odm2api
```

### Installing the development version from the `development` branch on github

Note: We follow the [Gitflow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) for development.

1. Download both `requirements.txt` and `requirements-dev.txt`.
    ``` bash
    wget https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/requirements.txt
    wget https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/requirements-dev.txt
    ```

2. Create conda environment `odm2api_dev` from the two `requirements*` text files.
    ```bash
    conda create -n odm2api_dev -c conda-forge python=2.7 --file requirements.txt --file requirements-dev.txt
    ```

3. Activate conda environment.
   - MacOSX/Linux:
   ```bash
   source activate odm2api_dev
   ```
   - Windows:
   ```
   activate odm2api_dev
   ```
    
3. Install the latest commit from the development branch
    ```bash
    pip install git+https://github.com/ODM2/ODM2PythonAPI.git@development#egg=odm2api
    ```

## Credits

This work was supported by National Science Foundation Grants
[EAR-1224638](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1224638)
and
[ACI-1339834](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1339834).
Any opinions, findings,
and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
