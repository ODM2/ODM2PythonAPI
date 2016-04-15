__author__ = 'tonycastronova'
__author__ = 'david valentin'

#import unittest

from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import  ReadODM2
from odm2api.ODM2.services.createService import CreateODM2
from odm2api.ODM2.services.updateService import UpdateODM2
from odm2api.ODM2.services.deleteService import DeleteODM2

from tests import test_connection as testConnection
import pytest
xfail = pytest.mark.xfail
skipif = xfail = pytest.mark.skipif
#from pytest import raises use pytest.raises()


dbs = testConnection.dbs_test

# @pytest.fixture(scope="session", params = dbs)
# def setup(request):
#     return testConnection.Connection(request)

class odmConnection():
    pass
#class test_sqlite(unittest.TestCase):
# class Testsqlite():
@pytest.fixture(scope="function", params=dbs)
#@classmethod
def setup( request):

    # build an empty database for testing
    # conn = dbconnection.createConnection('sqlite', ':memory:')
    db = request.param
    print ("dbtype", db[0], db[1])
    session_factory = dbconnection.createConnection(db[1], db[2], db[3], db[4], db[5], echo=True)
    assert session_factory is not None, ("failed to create a session for ", db[0], db[1])
    assert session_factory.engine is not None, ("failed: session has no engine ", db[0], db[1])
    # dbconnection._setSchema(conn.engine)
    dbConn = odmConnection
    # build connectors for read, write, update, and delete operations
    dbConn.odmread = ReadODM2(session_factory)
    dbConn.odmcreate = CreateODM2(session_factory)
    dbConn.odmupdate = UpdateODM2(session_factory)
    dbConn.odmdelete = DeleteODM2(session_factory)

    # initialize the in-memory database, loop through each command (skip first and last lines)
    #build = open('./tests/spatialite/build_empty.sqlite').read()
    if (db[2] == ':memory:'):
        build = open('./tests/schemas/sqlite/ODM2_for_SQLite.sql').read()
        for line in build.split(';\n'):
            session_factory.getSession().execute(line)

    print 'database initialization completed successfully'
    return dbConn

@pytest.mark.skipif(True, reason="Enable for testing: CreateService Session closes on failed create #52")
def test_SessionNotFailed(setup):
    # goal of this is to see that if we force errors like a null value, or duplicate that the session does not fail

    # create some people
    setup.odmcreate.createPerson(firstName="tony",
                                 lastName='castronova',
                                 middleName='michael')

    with pytest.raises(Exception) as excinfo:
        # this one should fail due to a not null constraint
        setup.odmcreate.createPerson(firstName=None,
                                     lastName='castronova',
                                     middleName='michael')

    assert 'NULL' in str(excinfo.value)

    # now add again
    setup.odmcreate.createPerson(firstName="tony",
                                 lastName='castronova',
                                 middleName=None)


    # with pytest.raises(Exception) as excinfo:
    #     # duplicate
    #     setup.odmcreate.createPerson(firstName="tony",
    #                                  lastName='castronova',
    #                                  middleName='michael')
    #
    # assert 'People.PersonFirstName may not be NULL' in str(excinfo.value)

    setup.odmcreate.createPerson(firstName="john",
                             lastName='doe')


    people = setup.odmread.getPeople()
    assert len(people) == 3, "People should have been 3"

# @classmethod
# def tearDownClass(self):
#     del self.odmread
#     del self.odmcreate
#     del self.odmupdate
#     del self.odmdelete

def test_createPerson(setup):

    # create some people
    setup.odmcreate.createPerson(firstName="tony",
                                lastName='castronova',
                                middleName='michael')

    setup.odmcreate.createPerson(firstName="tony",
                                lastName='castronova',
                                middleName=None)
    setup.odmcreate.createPerson(firstName="john",
                                lastName='doe')

    people = setup.odmread.getPeople()
    assert len(people) == 3, "People should have been 3"

def test_personFail(setup):
   with pytest.raises(Exception) as excinfo:
        # this one should fail due to a not null constraint
        setup.odmcreate.createPerson(firstName=None,
                                lastName='castronova',
                                middleName='michael')

   assert 'null' in str(excinfo.value).lower()

def test_createVariable(setup):

    # create some variables
    setup.odmcreate.createVariable( code = 'Phos_TOT',
                                   name = 'Phosphorus, total dissolved',
                                   vType = 'Hydrology',
                                   nodv = -999,
                                   speciation =None ,
                                   definition =None )
    setup.odmcreate.createVariable( code = 'Phos_TOT2',
                                   name = 'Phosphorus, total dissolved',
                                   vType = 'Hydrology',
                                   nodv = -999,
                                   speciation ='mg/L' ,
                                   definition =None )
    setup.odmcreate.createVariable( code = 'Phos_TOT3',
                                   name = 'Phosphorus, total dissolved',
                                   vType = 'Hydrology',
                                   nodv = -999,
                                   speciation =None ,
                                   definition ='some definition' )

    with pytest.raises(Exception) as excinfo:
        # insert duplicate
        setup.odmcreate.createVariable(code='Phos_TOT',
                                       name='Phosphorus, total dissolved',
                                       vType='Hydrology',
                                       nodv=-999,
                                       speciation=None,
                                       definition=None)

    assert 'unique' in str(excinfo.value).lower()

    vars = setup.odmread.getVariables()

    assert len(vars) == 3



def test_createMethod(setup):
    setup.odmcreate.createMethod(code ='mycode',
                                name='my test method',
                                vType='test method type',
                                orgId=None,
                                link=None,
                                description='method description')
    setup.odmcreate.createMethod(code ='mycode2',
                                name='my test method',
                                vType='test method type',
                                orgId=1,
                                link=None,
                                description='method description')
    setup.odmcreate.createMethod(code ='mycode3',
                                name='my test method',
                                vType='test method type',
                                orgId=None,
                                link=None,
                                description=None)
    methods = setup.odmread.getMethods()

    assert len(methods) == 3


def test_ProcessingLevel(setup):
    setup.odmcreate.createProcessingLevel(code="testlevel",
                                         definition="this is a test processing level",
                                         explanation=None)
    res = setup.odmread.getProcessingLevels()

    assert len(res) == 1

@skipif(True, reason="Needs data")
def test_createSamplingFeature(setup):


    res = setup.odmread.getSamplingFeatures()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createUnit(setup):

    res = setup.odmread.getUnits()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createOrganization(setup):
    res = setup.odmread.getOrganizations()

    assert len(res) == 1


@skipif(True, reason="Needs data")
def test_createAffiliation(setup):
    res = setup.odmread.getAffiliationsByPerson()

    assert len(res) == 1

@skipif(True, reason="Needs data")
def test_createDataset(setup):
    res = setup.odmread.getDataSets()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createDatasetResults(setup):
    res = setup.odmread.getProcessingLevels()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createAction(setup):
    # todo: this function is missing
    # res = self.odmread.getActions()

    assert 0 == 1
@skipif(True, reason="Needs data")
def test_createActionBy(setup):
    # todo; this function is missing
    # res = self.odmread.getActionsBy()

    assert 0 == 1
@skipif(True, reason="Needs data")
def test_createFeatureAction(setup):

    # todo: this function is missing
    # res = self.odmread.getFeatureActions()

    assert 0 == 1
@skipif(True, reason="Needs data")
def test_createResult(setup):
    res = setup.odmread.getResults()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createTimeSeriesResult(setup):
    res = setup.odmread.getTimeSeriesResults()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createTimeSeriesResultValues(setup):
    res = setup.odmread.getTimeSeriesResultValues()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createSite(setup):
    res = setup.odmread.getAllSites()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createSpatialReference(setup):
    res = setup.odmread.getSpatialReferenceByCode()

    assert len(res) == 1
@skipif(True, reason="Needs data")
def test_createDeploymentAction(setup):
    res = setup.odmread.getAllDeploymentAction()

    assert len(res) == 1

def test_createModel(setup):

    # create model  (expected: record inserted)
    setup.odmcreate.createModel(code='model',
                               name='mymodel',
                               description='my test model')

    # create with no description (expected: record inserted)
    setup.odmcreate.createModel(code='model2',
                               name='mymodel',
                               description=None)


    res = setup.odmread.getAllModels()

    assert len(res) == 2

    res = setup.odmread.getModelByCode('model')
    assert res is not None
    assert res.ModelCode == 'model'

    with pytest.raises(Exception) as excinfo:
        # create model with duplicate code (expected: fail to insert record)
        setup.odmcreate.createModel(code='model',
                                    name='mymodel2',
                                    description='my test model2')
    assert 'unique' in str(excinfo.value).lower()


def test_createRelatedModel(setup):
    # create a relationship type
    setup.odmcreate.getSession().execute(
        "insert into cv_relationshiptype values ('coupled', 'coupled model', 'models that have been coupled together', 'modeling', NULL)")
    # create model  (expected: record inserted)
    m1 = setup.odmcreate.createModel(code='model',
                                     name='mymodel',
                                     description='my test model')
    # create model  (expected: record inserted)
    m2 = setup.odmcreate.createModel(code='model2',
                                     name='mymodel2',
                                     description='my test model2')

    # create related records
    setup.odmcreate.createRelatedModel(modelid=m1.ModelID,
                                       relatedModelID=m2.ModelID,
                                       relationshipType='coupled')

    m1r = setup.odmread.getModelByCode('model')
    assert m1r is not None
    assert m1r.ModelCode == 'model'

    m2r = setup.odmread.getModelByCode('model2')
    assert m2r is not None
    assert m2r.ModelCode == 'model2'

    m1rel = setup.odmread.getRelatedModelsByCode('model')
    assert len(m1rel) == 1

    m2rel = setup.odmread.getRelatedModelsByCode('model2')
    assert len(m2rel) == 0

@skipif(True, reason="Needs data")
def test_createSimulation(setup):
    res = setup.odmread.getAllSimulations()

    assert len(res) == 1