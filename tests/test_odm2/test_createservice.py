import pytest
import datetime
from os.path import *
from odm2api.ODM2 import models
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
            except Exception as e:
                print e

        self.write = CreateODM2(db)
        self.engine= db.engine

        globals['write'] = self.write
        globals['engine'] = self.engine
        globals['db'] = db
        # return self.write, self.engine

    def setup(self):

        self.writer = globals['write']
        self.engine = globals['engine']
        self.db = globals['db']

    def test_createVariable(self):

        # assert that there are no variables in the database
        res = self.engine.execute('SELECT * from Variables')
        assert(len(res.fetchall()) == 0)


        # create a new variable
        code = 'MyVar'
        name = 'My Test Variable'
        vType = 'Hydrology'
        nodv = -9999
        speciation="mg/L as PO4"
        definition="This is a test variable"
        self.writer.createVariable(code = code,name = name,vType = vType,nodv =nodv,speciation=None,definition=None)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC').first()
        assert(res is not None)
        assert(res[1] == vType )        # vType
        assert(res[2] == code )         # code
        assert(res[3] == name )         # name
        assert(res[4] == None)          # definition
        assert(res[5] == None)          # speciation
        assert(res[6] == nodv )         # nodata

        self.writer.createVariable(code = code, name = name, vType = vType, nodv =nodv, speciation=speciation,definition=None)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC').first()
        assert(res is not None)
        assert(res[1] == vType )        # vType
        assert(res[2] == code )         # code
        assert(res[3] == name )         # name
        assert(res[4] == None)          # definition
        assert(res[5] == speciation)    # speciation
        assert(res[6] == nodv )         # nodata


        self.writer.createVariable(code = code,name = name,vType = vType,nodv =nodv,speciation=None,definition=definition)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC').first()
        assert(res is not None)
        assert(res[1] == vType )        # vType
        assert(res[2] == code )         # code
        assert(res[3] == name )         # name
        assert(res[4] == definition)    # definition
        assert(res[5] == None)          # speciation
        assert(res[6] == nodv )         # nodata


        self.writer.createVariable(code = code,name = name,vType = vType,nodv =nodv,speciation=speciation,definition=definition)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC').first()
        assert(res is not None)
        assert(res[1] == vType )        # vType
        assert(res[2] == code )         # code
        assert(res[3] == name )         # name
        assert(res[4] == definition)    # definition
        assert(res[5] == speciation)    # speciation
        assert(res[6] == nodv )         # nodata

    @pytest.mark.skipif(True, reason="implement")
    def test_createMethod(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createProcessingLevel(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createSamplingFeature(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createUnit(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createOrganization(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createPerson(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
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

    @pytest.mark.skipif(True, reason="implement")
    def test_createDatasetResults(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createAction(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createActionBy(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createFeatureAction(self):
        pass

    def test_createResult(self):

        # assert that there are no results
        res = self.engine.execute('SELECT * FROM Results')
        assert(len(res.fetchall()) == 0)

        # create a result record
        self.writer.createResult(featureactionid = 1,
                                variableid = 1,
                                unitid = 1,
                                processinglevelid = 1,
                                valuecount = 0,
                                sampledmedium = 'unknown',
                                resulttypecv = 'time series',
                                taxonomicclass=None, resultdatetime=None, resultdatetimeutcoffset=None,
                                validdatetime=None, validdatetimeutcoffset=None, statuscv=None)


        # assert that there are results
        res = self.engine.execute('SELECT * FROM Results')
        assert(len(res.fetchall()) == 1)

    def test_createTimeSeriesResult(self):

        # assert that there are no time series results in the database
        res = self.engine.execute('SELECT * FROM TimeSeriesResults').first()
        assert(res is None)
        
        # create a result record if it doesnt exist (required to test foriegn key relationship)
        result = self.engine.execute('SELECT * FROM Results').first()
        if result is None:
            # create a basic result record
            self.writer.createResult(featureactionid = 1,variableid = 1,unitid = 1,processinglevelid = 1,
                                    valuecount = 0,sampledmedium = 'unknown',resulttypecv = 'time series')
            result = self.engine.execute('SELECT * FROM Results').first()
            assert(result is not None)


        # create most basic time series result record possible
        tsr = self.writer.createTimeSeriesResult(result=result, aggregationstatistic='unknown')

        # assert that this basic tsr exists in the datbase
        res = self.engine.execute('SELECT * FROM TimeSeriesResults').first()
        assert(res is not None)

    @pytest.mark.skipif(True, reason="implement")
    def test_createTimeSeriesResultValues(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createSite(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createSpatialReference(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createDeploymentAction(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createModel(self):
        pass

    @pytest.mark.skipif(True, reason="implement")
    def test_createRelatedModel(self):
        pass
    
    
    def test_createSimulation(self):

        # todo: insert should fail if unitID or actionID do not exist

        # assert that there are no datasets in the database
        res = self.engine.execute('SELECT * from Simulations')
        assert(len(res.fetchall()) == 0)

        # create a new simulation
        st = datetime.datetime(2016,1,1)
        et = datetime.datetime(2016,1,25)
        dataset = self.writer.createSimulation( actionid = 1,
                                                modelID=1,
                                                simulationName= 'MySimulation',
                                                simulationDescription = 'My simulation description',
                                                simulationStartDateTime = st,
                                                simulationStartOffset = 6,
                                                simulationEndDateTime = et,
                                                simulationEndOffset = 6,
                                                timeStepValue = 1,
                                                timeStepUnitID = 1,
                                                inputDatasetID=None)

        # assert that this record has been successfully inserted
        res = self.engine.execute('SELECT * from Simulations')
        assert(len(res.fetchall()) == 1)

