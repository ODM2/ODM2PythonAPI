Installation
============

The easiest and most reliable way to install the ODM2 Python API
(``odm2api``) is using the `Conda package management
system <https://conda.io/docs/>`__ via either
`Anaconda <https://www.anaconda.com/download/>`__ or
`Miniconda <https://conda.io/miniconda.html>`__. To start using
conda (if it's not your system default), add conda to the PATH; on
OS X and Linux, it's something like
``export PATH=$HOME/miniconda3/bin:$PATH``, but the exact path may vary.

To activate a conda environment, say, "myenv":

.. code-block:: bash

    activate myenv  # On Windows
    source activate myenv  # On MacOSX or Linux

**Note:** ``odm2api`` currently is only tested on Python 2.7. Some
changes have been made to support Python 3.x, but they haven't been
tested thoroughly.

Latest release, from conda-forge anaconda.org channel
----------------------------------------------

The `latest release <https://github.com/ODM2/ODM2PythonAPI/releases>`_ is available
on the `conda-forge anaconda.org channel <https://anaconda.org/conda-forge/odm2api>`_
for all major OS platforms (linux, OS X, win32/win64). To install it on
an existing conda environment:

::

    conda install -c conda-forge odm2api

All dependencies are installed, including Pandas and its dependencies
(numpy, etc).

To create a new environment "myenv" with the ``odm2api`` package:

::

    conda create -n myenv -c conda-forge python=2.7 odm2api


Installing the development version from the ``development`` branch on github
----------------------------------

Note: We follow the `Gitflow workflow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__ for development.

1. Download both ``requirements.txt`` and ``requirements-dev.txt``.
   
   .. code-block:: bash
   
       wget https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/requirements.txt
       wget https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/requirements-dev.txt

2. Create conda environment ``odm2api_dev`` from the two ``requirements*`` text files.

   .. code-block:: bash
  
       conda create -n odm2api_dev -c conda-forge python=2.7 --file requirements.txt --file requirements-dev.txt

3. Activate conda environment.
   - MacOSX/Linux:
   
   .. code-block:: bash
       
       source activate odm2api_dev
   
   - Windows:
   
   .. code-block:: bash
      
       activate odm2api_dev
    
4. Install the latest commit from the development branch

   .. code-block:: bash
      
       pip install git+https://github.com/ODM2/ODM2PythonAPI.git@development#egg=odm2api
