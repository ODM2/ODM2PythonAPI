Get Started
============


Install the latest release with conda
-------------------------------------

The easiest and most reliable way to install the ODM2 Python API package
(``odm2api``) is using the `**Conda** package management
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
^^^^^^^^^^^^^^^^^^^^^^^^^

The `latest release <https://github.com/ODM2/ODM2PythonAPI/releases>`_ is available
as a package on the `conda-forge anaconda.org channel <https://anaconda.org/conda-forge/odm2api>`_
for all major OS platforms (linux, OS X, win32/win64). To install it on
an existing conda environment:

::

    conda install -c conda-forge odm2api

All dependencies are installed, including Pandas and its dependencies
(numpy, etc).

To create a new environment "myenv" with the ``odm2api`` package:

::

    conda create -n myenv -c conda-forge python=2.7 odm2api

Sample Jupyter notebooks
------------------------

These two notebooks are complete, extended examples that illustrate reading from ODM2 databases and using the resulting data and metadata. They use SQLite ODM2 file databases that can be `downloaded here <https://github.com/ODM2/ODM2PythonAPI/tree/master/Examples/data>`_.
A conda environment to run these notebooks can be created with the conda environment file
`clientenvironment.yml <https://github.com/ODM2/ODM2PythonAPI/blob/master/Examples/clientenvironment.yml>`_.

1. `WaterQualityMeasurements_RetrieveVisualize.ipynb <https://nbviewer.jupyter.org/github/ODM2/ODM2PythonAPI/blob/master/Examples/WaterQualityMeasurements_RetrieveVisualize.ipynb>`_

2. `TimeSeries_RetrieveVisualize.ipynb <https://nbviewer.jupyter.org/github/ODM2/ODM2PythonAPI/blob/master/Examples/TimeSeries_RetrieveVisualize.ipynb>`_

Code examples
-------------

Connecting to an ODM2 database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Connect to an ODM2 database and open the connection for reading.

.. code-block:: python

    from odm2api.ODMconnection import dbconnection
    import odm2api.services.readService as odm2rs

    # -----------------------------------------------------
    # 1. A SQLite file-based connection
    session_factory = dbconnection.createConnection('sqlite',
                                                    '/myfilepath/odm2db.sqlite')
    read = odm2rs.ReadODM2(session_factory)

    # -----------------------------------------------------
    # 2. A server-based database system connection
    db_credentials = {
        'address': 'ip-or-domainname',
        'db': 'dbname',
        'user': 'dbuser',
        'password': 'password'
    }
    session_factory = dbconnection.createConnection('postgresql',
                                                    **db_credentials)
    read = odm2rs.ReadODM2(session_factory)


Updating an entity (table)
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `update services <https://github.com/ODM2/ODM2PythonAPI/blob/master/odm2api/services/updateService.py>`_
have not been fleshed out at this time, for the most part. However, updates can be easily
accomplished by reusing the connection setup at the start of an odm2api session,
then constructing and issuing a direct ``SQL UPDATE`` statement, like this:

.. code-block:: python

    from odm2api.ODMconnection import dbconnection

    session_factory = dbconnection.createConnection('postgresql',
                                                    **db_credentials)
    DBSession = session_factory.getSession()

    sq_str = " UPDATE mytable SET variablecode = 'xyz' WHERE variablecode = 'abc' "
    DBSession.execute(sql_str)
    DBSession.commit()
