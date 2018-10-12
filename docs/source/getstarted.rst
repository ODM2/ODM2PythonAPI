Get Started
============


Install the latest release as a conda package from conda-forge
----------------------------------------------

conda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Install the conda package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


Code examples
----------------------------------------------




Sample Jupyter notebooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Also mention the associated SQLite ODM2 databases. And the conda environment file.

1. `WaterQualityMeasurements_RetrieveVisualize.ipynb <https://github.com/ODM2/ODM2PythonAPI/blob/master/Examples/WaterQualityMeasurements_RetrieveVisualize.ipynb>`_

2. `TimeSeries_RetrieveVisualize.ipynb <https://github.com/ODM2/ODM2PythonAPI/blob/master/Examples/TimeSeries_RetrieveVisualize.ipynb>`_

