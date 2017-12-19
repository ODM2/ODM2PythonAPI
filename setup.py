from __future__ import (absolute_import, division, print_function)

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
from codecs import open

from setuptools import find_packages, setup

import versioneer

here = os.path.abspath(os.path.dirname(__file__))

# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
install_requires = [t.strip() for t in requirements]

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='odm2api',
    version=versioneer.get_version(),
    description='Python interface for the Observations Data Model 2 (ODM2)',
    long_description=long_description,
    url='https://github.com/ODM2/ODM2PythonAPI',
    author='ODM2 team-Stephanie Reeder',
    author_email='stephanie.reeder@usu.edu',
    maintainer='David Valentine',
    maintainer_email='david.valentine@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering'
    ],
    keywords='Observations Data Model ODM2',
    packages=find_packages(exclude=['samplefiles', 'setup', 'tests*', 'Forms']),
    install_requires=install_requires,
    extras_require={
        'mysql': ['pymysql'],
        'postgis': ['psycopg2'],
        'sqlite': ['pyspatialite >=3.0.0'],
    },
    cmdclass=versioneer.get_cmdclass(),
)
