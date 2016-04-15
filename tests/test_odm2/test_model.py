__author__ = 'stephanie'
# run with 'py.test -s test_example.py'
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.models import *
from .. import test_connection as testConnection
import pytest

# class Connection:
#     def __init__(self, request):
#         #session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
#         db = request.param
#         session_factory = dbconnection.createConnection(db[0],db[1],db[2],db[3],)
#         self.session = session_factory.getSession()

# assumes that pytest is being run from ODM2PythonAPI directory
dbs = testConnection.dbs_readonly
# dbs = [
#  #   ['mysql', 'localhost', 'odm2', 'ODM', 'odm'],
#  #      ["sqlite", "./tests/spatialite/odm2_test.sqlite",None, None]
#     ["sqlite", "../odm2_test.sqlite",None, None, None]
# ]

#
#              params=["sqlite+pysqlite:///../../ODM2PythonAPI/tests/spatialite/odm2_test.sqlite", "mail.python.org"])
@pytest.fixture(scope="session", params = dbs)
def setup(request):
    return testConnection.Connection(request)
    # #session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
    # db = request.param
    # session_factory = dbconnection.createConnection(db[0],db[1],db[2],db[3],)
    # self.session = session_factory.getSession()
############
# Fixtures #
############
#class TestODM2:

#    @pytest.fixture(autouse=True)

def test_cvelevationdatum(setup):
    q= setup.session.query(CVElevationDatum)
    results= q.all()
    #print results
    assert len(results) > 0

def test_cvsamplingfeatuergeotype(setup):
    q=setup.session.query(CVSamplingFeatureGeoType)
    results = q.all()
    #print results
    assert len(results) > 0

def test_cvsamplingfeaturetype(setup):
    q = setup.session.query(CVSamplingFeatureType)
    results = q.all()
    #print results
    assert len(results) > 0

def test_sampling_feature(setup):
    q = setup.session.query(SamplingFeatures)
    results = q.all()
    '''
    for r in results:
        print r
        print r.SamplingFeatureGeotypeCV
        print r.FeatureGeometry
    #print results
    '''
    assert len(results) > 0

