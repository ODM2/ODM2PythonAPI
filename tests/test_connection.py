from __future__ import (absolute_import, division, print_function)

from odm2api.ODMconnection import dbconnection
from odm2api.models import CVElevationDatum

import pytest

from sqlalchemy.engine import reflection


__author__ = 'valentine'

dbs_readonly = [
    ['mysql_odm2_odm', 'mysql', 'localhost', 'odm2', 'ODM', 'odm'],
    ['mysql_odm2_root', 'mysql', 'localhost', 'odm2', 'root', None],
    ['postgresql_marchantariats', 'postgresql', 'localhost', 'marchantariats', 'postgres', 'iforget'],
    ['sqlite_wof', 'sqlite', './tests/spatialite/wof2odm/ODM2.sqlite', None, None, None]
]

dbs_test = [
    ['sqlite_memory', 'sqlite', ':memory:', None, None, None]
]


class Connection:
    def __init__(self, request):
        db = request.param
        print ('dbtype', db[0], db[1])
        session_factory = dbconnection.createConnection(db[1], db[2], db[3], db[4], db[5], echo=True)
        assert session_factory is not None, ('failed to create a session for ', db[0], db[1])
        assert session_factory.engine is not None, ('failed: session has no engine ', db[0], db[1])

        insp = reflection.Inspector.from_engine(session_factory.engine)
        insp.get_table_names()
        self.session = session_factory.getSession()


@pytest.fixture(scope='session', params=dbs_readonly)
def setup(request):
    return Connection(request)


def test_connection(setup):
    q = setup.session.query(CVElevationDatum)
    results = q.all()
    assert len(results) > 0


def test_create_all_schema():
    pass


def test_create_all_no_schema():
    pass
