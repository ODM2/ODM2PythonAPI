Installation
------------

The easiest and most reliable way to install the ODM2 Python API
(``odm2api``) is using the `Conda package management
system <http://conda.pydata.org/docs/>`__ via either
`Anaconda <https://www.continuum.io/downloads>`__ or
`Miniconda <http://conda.pydata.org/miniconda.html>`__. To start using
conda (if it's not your system default), add conda to the PATH; on
MacOSX and Linux, it's something like
``export PATH=$HOME/miniconda/bin:$PATH``, but the exact path may vary.

To activate a conda environment, say, "myenv":

.. code:: bash

    activate myenv  # On Windows
    source activate myenv  # On MacOSX or Linux

**Note:** ``odm2api`` currently is only tested on Python 2.7. Some
changes have been made to support Python 3.x, but they haven't been
tested thoroughly.

Latest release, from ODM2 anaconda.org channel
----------------------------------------------

The `latest ``odm2api``
release <https://github.com/ODM2/ODM2PythonAPI/releases>`__ is available
on the `ODM2 anaconda.org channel <https://anaconda.org/odm2/odm2api>`__
for all major OS paltforms (linux, OSX, win32/win64). To install it on
an existing conda environment:

::

    conda install -c odm2 odm2api

All dependencies are installed, including Pandas and its dependencies
(numpy, etc).

To create a new environment "myenv" with the ``odm2api`` package:

::

    conda create -n myenv -c odm2 python=2.7 odm2api


Installing the development version from the ``master`` branch on GitHub
-----------------------------------------------------------------------

**Note from 4/26/2016:** These instructions may be slightly outdated.
Follow these directions for installing the bleeding edge GitHub master
branch, mainly for development and testing purposes.

To create a new environment "myenv" with ``odm2api``, first download the
conda environment file
`condaenvironment\_1.yml <https://raw.githubusercontent.com/ODM2/ODM2PythonAPI/master/condaenvironment_1.yml>`__.
Go to the directory where ``condaenvironment_1.yml`` was downloaded.
Then, on a terminal shell:

.. code:: bash

    conda env create -n myenv --file py2_conda_environment.yml

Activate the new environment, then install ``odm2api`` into the
environment:

.. code:: bash

    activate myenv  # On Windows
    source activate myenv  # On MacOSX or Linux

    pip install --process-dependency-links git+https://github.com/ODM2/ODM2PythonAPI.git
