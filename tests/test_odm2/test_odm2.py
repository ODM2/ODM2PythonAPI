from __future__ import (absolute_import, division, print_function)

#import unittest

from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import  ReadODM2
from odm2api.ODM2.services.createService import CreateODM2
from odm2api.ODM2.services.updateService import UpdateODM2
from odm2api.ODM2.services.deleteService import DeleteODM2
from odm2api.ODM2.models import (People,
                                 Variables,
                                 Methods,
                                 ProcessingLevels,
                                 Models,
                                 RelatedModels)

from tests import test_connection as testConnection
import pytest


__author__ = ['tony castronova', 'david valentine']


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
    print("dbtype", db[0], db[1])
    session_factory = dbconnection.createConnection(db[1], db[2], db[3], db[4], db[5], echo=False)
    assert session_factory is not None, ("failed to create a session for ", db[0], db[1])
    assert session_factory.engine is not None, ("failed: session has no engine ", db[0], db[1])
    # dbconnection._setSchema(conn.engine)
    dbConn = odmConnection
    # build connectors for read, write, update, and delete operations
    dbConn.odmread = ReadODM2(session_factory)
    dbConn.odmcreate = CreateODM2(session_factory)
    dbConn.odmupdate = UpdateODM2(session_factory)
    dbConn.odmdelete = DeleteODM2(session_factory)
    s = session_factory.getSession()
    # initialize the in-memory database, loop through each command (skip first and last lines)
    #build = open('./tests/spatialite/build_empty.sqlite').read()
    if (db[2] == ':memory:'):
        build = open('./tests/schemas/sqlite/ODM2_for_SQLite.sql').read()
        for line in build.split(';\n'):
            s.execute(line)
        s.flush()
 #       s.invalidate()

    print('database initialization completed successfully')

    def fin():
        print("teardown odm2 test connection")
        del dbConn.odmread
        del dbConn.odmcreate
        del dbConn.odmupdate
        del dbConn.odmdelete
        session_factory.engine.dispose()
        session_factory.test_engine.dispose()
        s.invalidate()

    request.addfinalizer(fin)

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
    p1 = People(PersonFirstName="tony", PersonLastName='castronova', PersonMiddleName='Michael')
    p2 = People(PersonFirstName="tony", PersonLastName='castronova')
    p3 = People(PersonFirstName="john", PersonLastName='doe')
    setup.odmcreate.createPerson(p1)
    setup.odmcreate.createPerson(p2)
    setup.odmcreate.createPerson(p3)
    # setup.odmcreate.createPerson(firstName="tony",
    #                             lastName='castronova',
    #                             middleName='michael')
    #
    # setup.odmcreate.createPerson(firstName="tony",
    #                             lastName='castronova',
    #                             middleName=None)
    # setup.odmcreate.createPerson(firstName="john",
    #                             lastName='doe')

    people = setup.odmread.getPeople()
    assert len(people) == 3, "People should have been 3"

def test_personFail(setup):
   with pytest.raises(Exception) as excinfo:
        # this one should fail due to a not null constraint

        # setup.odmcreate.createPerson(firstName=None,
        #                         lastName='castronova',
        #                         middleName='michael')
       p1 = People(PersonFirstName=None, PersonLastName='doe', PersonMiddleName='john')
       setup.odmcreate.createPerson(p1)

   assert 'null' in str(excinfo.value).lower()

def test_createVariable(setup):
    v1 = Variables(VariableCode='Phos_TOT',
                   VariableNameCV='Phosphorus, total dissolved',
                   VariableTypeCV='Hydrology',
                   NoDataValue=-999,
                   SpeciationCV=None,
                   VariableDefinition=None)
    v2 = Variables(VariableCode='Phos_TOT2',
                   VariableNameCV='Phosphorus, total dissolved',
                   VariableTypeCV='Hydrology',
                   NoDataValue=-999,
                   SpeciationCV='mg/L',
                   VariableDefinition=None)
    v3 = Variables(VariableCode='Phos_TOT3',
                   VariableNameCV='Phosphorus, total dissolved',
                   VariableTypeCV='Hydrology',
                   NoDataValue=-999,
                   SpeciationCV=None,
                   VariableDefinition='some definition')
    # create some variables
    setup.odmcreate.createVariable(v1)
    setup.odmcreate.createVariable(v2)
    setup.odmcreate.createVariable(v3)

    variables = setup.odmread.getVariables()
    print(variables)
    assert len(variables) == 3

    with pytest.raises(Exception) as excinfo:
        # insert duplicate
        setup.odmcreate.createVariable(
            Variables(VariableCode='Phos_TOT',
                   VariableNameCV='Phosphorus, total dissolved',
                   VariableTypeCV='Hydrology',
                   NoDataValue=-999,
                   SpeciationCV=None,
                   VariableDefinition=None)
        )

    assert 'unique' in str(excinfo.value).lower()


def test_createMethod(setup):
    m1 = Methods(MethodCode='mycode',
                 MethodName='my test method',
                 MethodTypeCV='Unknown',
                 MethodDescription='method description',
                 MethodLink=None,
                 OrganizationID=None)
    m2 = Methods(MethodCode='mycode2',
                 MethodName='my test method',
                 MethodTypeCV='Unknown',
                 MethodDescription='method description',
                 MethodLink=None,
                 OrganizationID=1)
    m3 = Methods(MethodCode='mycode3',
                 MethodName='my test method',
                 MethodTypeCV='Unknown',
                 MethodDescription=None,
                 MethodLink=None,
                 OrganizationID=None)
    setup.odmcreate.createMethod(m1)
    setup.odmcreate.createMethod(m2)
    setup.odmcreate.createMethod(m3)
    methods = setup.odmread.getMethods()

    assert len(methods) == 3


def test_ProcessingLevel(setup):
    pl = ProcessingLevels(ProcessingLevelCode='testlevel',
                          Definition='this is a test processing level',
                          Explanation=None)
    setup.odmcreate.createProcessingLevel(pl)
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
    mod1 = Models(ModelCode='converter',
                  ModelName='mymodel',
                  ModelDescription='my test converter')
    mod2 = Models(ModelCode='model2',
                  ModelName='mymodel',
                  ModelDescription=None)
    mod3 = Models(ModelCode='converter',
                  ModelName='mymodel2',
                  ModelDescription='my test model2')
    # create converter  (expected: record inserted)
    setup.odmcreate.createModel(mod1)

    # create with no description (expected: record inserted)
    setup.odmcreate.createModel(mod2)


    res = setup.odmread.getModels()

    assert len(res) == 2

    res = setup.odmread.getModels(codes=['converter'])
    assert res is not None
    assert res.ModelCode == 'converter'

    with pytest.raises(Exception) as excinfo:
        # create converter with duplicate code (expected: fail to insert record)
        setup.odmcreate.createModel(mod3)
    assert 'unique' in str(excinfo.value).lower()


def test_createRelatedModel(setup):
    # create a relationship type
    setup.odmcreate.getSession().execute(
        "insert into cv_relationshiptype values ('coupled', 'coupled converter', 'models that have been coupled together', 'modeling', NULL)")
    mod1 = Models(ModelCode='converter',
                  ModelName='mymodel',
                  ModelDescription='my test converter')
    mod2 = Models(ModelCode='model2',
                  ModelName='mymodel',
                  ModelDescription='my test model2')
    # create converter  (expected: record inserted)
    m1 = setup.odmcreate.createModel(mod1)
    # create converter  (expected: record inserted)
    m2 = setup.odmcreate.createModel(mod2)

    rm = RelatedModels(ModelID=m1.ModelID,
                       RelatedModelID=m2.ModelID,
                       RelationshipTypeCV='Is part of')
    # create related records
    setup.odmcreate.createRelatedModel(rm)

    m1r = setup.odmread.getModels(codes=['converter'])
    assert m1r is not None
    assert m1r.ModelCode == 'converter'

    m2r = setup.odmread.getModels(codes=['model2'])
    assert m2r is not None
    assert m2r.ModelCode == 'model2'

    m1rel = setup.odmread.getRelatedModels(code='converter')
    assert len(m1rel) == 1

    m2rel = setup.odmread.getRelatedModels(code='model2')
    assert len(m2rel) == 0

@skipif(True, reason="Needs data")
def test_createSimulation(setup):
    res = setup.odmread.getAllSimulations()

    assert len(res) == 1
