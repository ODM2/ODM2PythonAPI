Installation
------------

The easiest and most reliable way to install the ODM2 Python API
(``odm2api``) is using the `Conda package management
system <https://conda.io/docs/>`__ via either
`Anaconda <https://www.anaconda.com/download/>`__ or
`Miniconda <https://conda.io/miniconda.html>`__. To start using
conda (if it's not your system default), add conda to the PATH; on
OS X and Linux, it's something like
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
for all major OS paltforms (linux, OS X, win32/win64). To install it on
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

To create a new environment "myenv" with ``odm2api``, first clone the repository.
Then, on a terminal shell:

.. code:: bash

    conda env create -n myenv --file py2_conda_environment.yml
    conda create --name myenv python=2.7 --file requirements.txt --file requirements-dev.txt

Activate the new environment, then install ``odm2api`` into the
environment:

.. code:: bash

    activate myenv  # On Windows
    source activate myenv  # On MacOSX or Linux
