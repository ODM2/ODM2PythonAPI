ODM2 Python API
====

A Python-based application programmer's interface for the Observations Data Model 2 (ODM2) 

[List of current and planned functions included in the API](https://github.com/ODM2/ODM2PythonAPI/blob/master/doc/APIFunctionList.md)

### Installation

Currently the easiest and most reliable way to install the ODM2 Python API (`odm2api`) is using the [Conda package management system](http://conda.pydata.org/docs/) via either [Anaconda](https://www.continuum.io/downloads) or [Miniconda](http://conda.pydata.org/miniconda.html). To create a new `odm2api` environment, first download the conda environment file [condaenvironment_1.yml](https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/condaenvironment_1.yml). Then, on a terminal shell:

1. Add conda to the PATH; on MacOSX and Linux, it's something like `export PATH=$HOME/miniconda/bin:$PATH`, but the exact path may vary.
2. Go to the directory where `condaenvironment_1.yml` was downloaded.
3. Create a new conda environment. This command will create an environment called 'odm2api_env1':    

  ```bash
  conda env create -f condaenvironment_1.yml
  ```
4. Activate the new environment:    

  ```bash
  activate odm2api_env1  # On Windows
  source activate odm2api_env1  # On MacOSX or Linux
  ```
5. Install the `odm2api` package into the environment:  

  ```bash
  pip install --process-dependency-links git+https://github.com/ODM2/ODM2PythonAPI.git
  ```
  
### Credits

This work was supported by National Science Foundation Grants [EAR-1224638](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1224638) and [ACI-1339834](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1339834). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
