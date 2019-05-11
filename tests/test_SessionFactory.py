from __future__ import (absolute_import, division, print_function)

from odm2api.ODMconnection import SessionFactory
from odm2api.models import CVElevationDatum, setSchema

import pytest

__author__ = 'valentine'


dbs_readonly = [
    ['mysql:ODM@Localhost/', 'mysql', 'mysql+pymysql://ODM:odm@localhost/'],
    ['mysql"root@Localhost/', 'mysql', 'mysql+pymysql://root@localhost/'],
    ['mysql:ODM@Localhost/odm2', 'mysql', 'mysql+pymysql://ODM:odm@localhost/odm2'],
    ['mysql"root@Localhost/odm2', 'mysql', 'mysql+pymysql://root@localhost/odm2'],
    ['postgresql_marchantariats_none', 'postgresql',
     'postgresql+psycopg2://postgres:None@localhost/marchantariats',
     'marchantariats', 'postgres', None],
    ['postgresql_marchantariats_empty', 'postgresql',
     'postgresql+psycopg2://postgres@localhost/marchantariats',
     'marchantariats', 'postgres', None],
    ['sqlite_wof', 'sqlite', 'sqlite:///./tests/spatialite/wof2odm/ODM2.sqlite', None, None, None]
]

dbs_test = [
    ['sqlite_test', 'sqlite' './tests/spatialite/odm2_test.sqlite', None, None, None]
]


class aSessionFactory:
    def __init__(self, request):
        db = request.param
        print ('dbtype', db[0], db[1])
        session_factory = SessionFactory(db[2])
        setSchema(session_factory.engine)
        assert session_factory is not None, ('failed to create a session for ', db[0], db[1])
        self.session = session_factory.getSession()


@pytest.fixture(scope='session', params=dbs_readonly)
def setup(request):
    return aSessionFactory(request)


def test_aSessionFactory(setup):
    q = setup.session.query(CVElevationDatum)
    results = q.all()
    assert len(results) > 0
