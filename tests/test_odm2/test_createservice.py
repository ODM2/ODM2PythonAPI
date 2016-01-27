import pytest
from os.path import *
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.createService import CreateODM2

# run this test from the root directory using:
# python -m pytest tests/test_odm2/test_createservice.py

globals = {}

class TestCreateService:

    @pytest.fixture(scope="class", autouse=True)
    def build_db(self):
        """
        Builds an empty sqlite (in-memory) database for testing
        :return: None
        """
        # path to the ddl script for building the database
        ddlpath= abspath(join(dirname(__file__), 'data/empty.sql'))

        # create and empty sqlite database for testing
        db = dbconnection.createConnection('sqlite', ':memory:')

        # read the ddl script and remove the first (BEGIN TRANSACTION) and last (COMMIT) lines
        ddl = open(ddlpath, 'r').read()
        ddl = ddl.replace('BEGIN TRANSACTION;','')
        ddl = ddl.replace('COMMIT;','')

        # execute each statement to build the odm2 database
        for line in ddl.split(');')[:-1]:
            try:
                db.engine.execute(line + ');')
            except Exception, e:
                print e

        self.write = CreateODM2(db)
        self.engine= db.engine

        globals['write'] = self.write
        globals['engine'] = self.engine
        # return self.write, self.engine

    def setup(self):

        self.writer = globals['write']
        self.engine = globals['engine']

    def test_createVariable(self):
        pass

    def test_createMethod(self):
        pass

    def test_createProcessingLevel(self):
        pass 

    def test_createSamplingFeature(self):
        pass

    def test_createUnit(self):
        pass
    
    def test_createOrganization(self):
        pass 

    def test_createPerson(self):
        pass

    def test_createAffiliation(self): 
        pass

    def test_createDataset(self):
        type = "Generic"
        code = "MyNewDataset"
        title= "Just a test dataset"
        desc = "this record represents a test dataset"

        # assert that there are no datasets in the database
        res = self.engine.execute('SELECT * from DataSets')
        assert(len(res.fetchall()) == 0)

        # create a new dataset
        dataset = self.writer.createDataset(dstype=type,
                                           dscode=code,
                                           dstitle=title,
                                           dsabstract=desc)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from DataSets')
        assert(len(res.fetchall()) == 1)


    def test_createDatasetResults(self):
        pass
    
    def test_createAction(self):
        pass

    def test_createActionBy(self): 
        pass
    
    def test_createFeatureAction(self):
        pass

    def test_createResult(self):
        pass

    def test_createTimeSeriesResult(self):
        pass


    def test_createTimeSeriesResultValues(self):
        pass


    def test_createSite(self): 
        pass


    def test_createSpatialReference(self): 
        pass

    def test_createDeploymentAction(self): 
        pass


    def test_createModel(self):
        pass


    def test_createRelatedModel(self):
        pass
    
    
    def test_createSimulation(self):
        pass
