"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

'''
to install in development mode, run the following code from command line
"python setup.py develop"
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

from pip.req import parse_requirements
install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
     long_description = f.read()
#long_description = ""
setup(
    name='odm2api',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.5.2',

    description='A Python-based application programmers interface for the Observations Data converter 2 (ODM2) ',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ODM2/ODM2PythonAPI',

    # Author details
    author='ODM2 team-Stephanie Reeder',
    author_email='stephanie.reeder@usu.edu',

    # note: maintainer gets listed as author in PKG-INFO, so leaving
    # this commented out for now
    maintainer='David Valentine',
    maintainer_email='david.valentine@gmail.com',

    # Choose your license
    license='BSD-3-Clause',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering'
    ],

    # What does your project relate to?
    keywords='Observations Data converter ODM2',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().

    packages=find_packages(exclude=['samplefiles', 'setup', 'tests*', 'Forms']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html

    install_requires=install_reqs,
    # install_requires=[
    #     'pyodbc',
    #     'six',
    #     'sqlalchemy',
    #     'geoalchemy>=0.7.3',
    #     'shapely',
    #     'pandas',
    # ],
    # dependency_links- geoalchemy from the ODM repository
    dependency_links=[
        "git+https://github.com/ODM2/geoalchemy.git@v0.7.4#egg=geoalchemy-0.7.4"
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'mysql': ['pymysql'],
        'postgis': ['psycopg2'],
        'sqlite': ['pyspatialite >=3.0.0'], # need to look at: http://www.gaia-gis.it/spatialite-2.4.0-4/splite-python.html
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'

    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.

    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
