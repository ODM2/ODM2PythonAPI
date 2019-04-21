from __future__ import (absolute_import, division, print_function)

import datetime
import uuid
from os.path import abspath, dirname, join

from odm2api import models
from odm2api.services.createService import CreateODM2
from odm2api.ODMconnection import dbconnection

import pytest
# run this test from the root directory using:
# python -m pytest tests/test_odm2/test_createservice.py

globals_vars = {}


class TestCreateService:

    @pytest.fixture(scope='class', autouse=True)
    def build_db(self):
        """
        Builds an empty sqlite (in-memory) database for testing
        :return: None

        """
        # path to the ddl script for building the database
        ddlpath = abspath(join(dirname(__file__), 'data/empty.sql'))

        # create and empty sqlite database for testing
        db = dbconnection.createConnection('sqlite', ':memory:')

        # read the ddl script and remove the first (BEGIN TRANSACTION) and last (COMMIT) lines
        ddl = open(ddlpath, 'r').read()
        ddl = ddl.replace('BEGIN TRANSACTION;', '')
        ddl = ddl.replace('COMMIT;', '')

        # execute each statement to build the odm2 database
        for line in ddl.split(');')[:-1]:
            try:
                db.engine.execute(line + ');')
            except Exception as e:
                print(e)

        self.write = CreateODM2(db)
        self.engine = db.engine

        globals_vars['write'] = self.write
        globals_vars['engine'] = self.engine
        globals_vars['db'] = db

    def setup(self):
        self.writer = globals_vars['write']
        self.engine = globals_vars['engine']
        self.db = globals_vars['db']

    def test_createVariable(self):
        # assert that there are no variables in the database
        res = self.engine.execute('SELECT * from Variables')
        assert(len(res.fetchall()) == 0)

        # create a new variable
        code = 'MyVar'
        name = 'My Test Variable'
        vType = 'Hydrology'
        nodv = -9999
        speciation = 'mg/L as PO4'
        definition = 'This is a test variable'
        v = models.Variables(
            VariableCode=code,
            VariableNameCV=name,
            VariableTypeCV=vType,
            NoDataValue=nodv,
            SpeciationCV=None,
            VariableDefinition=None
        )
        val = self.writer.createVariable(v)
        res = self.engine.execute(
            'SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC'
        ).first()
        assert(res is not None)
        assert(res[0] == val.VariableID)
        assert(res[1] == vType)  # vType
        assert(res[2] == code)  # code
        assert(res[3] == name)  # name
        assert(res[4] is None)  # definition
        assert(res[5] is None)  # speciation
        assert(res[6] == nodv)  # nodata

        v = models.Variables(
            VariableCode=code,
            VariableNameCV=name,
            VariableTypeCV=vType,
            NoDataValue=nodv,
            SpeciationCV=speciation,
            VariableDefinition=None
        )
        val = self.writer.createVariable(v)
        # assert that this dataset has been successfully inserted
        res = self.engine.execute(
            'SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC'
        ).first()
        assert(res is not None)
        assert(res[0] == val.VariableID)
        assert(res[1] == vType)  # vType
        assert(res[2] == code)  # code
        assert(res[3] == name)  # name
        assert(res[4] is None)  # definition
        assert(res[5] == speciation)  # speciation
        assert(res[6] == nodv)  # nodata

        v = models.Variables(
            VariableCode=code,
            VariableNameCV=name,
            VariableTypeCV=vType,
            NoDataValue=nodv,
            SpeciationCV=None,
            VariableDefinition=definition
        )
        val = self.writer.createVariable(v)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute(
            'SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC'
        ).first()
        assert(res is not None)
        assert(res[0] == val.VariableID)
        assert(res[1] == vType)  # vType
        assert(res[2] == code)  # code
        assert(res[3] == name)  # name
        assert(res[4] == definition)  # definition
        assert(res[5] is None)  # speciation
        assert(res[6] == nodv)  # nodata

        v = models.Variables(
            VariableCode=code,
            VariableNameCV=name,
            VariableTypeCV=vType,
            NoDataValue=nodv,
            SpeciationCV=speciation,
            VariableDefinition=definition
        )

        val = self.writer.createVariable(v)

        res = self.engine.execute(
            'SELECT * from Variables WHERE VariableCode = "MyVar" ORDER BY VariableID DESC'
        ).first()
        assert(res is not None)
        assert(res[0] == val.VariableID)
        assert(res[1] == vType)  # vType
        assert(res[2] == code)  # code
        assert(res[3] == name)  # name
        assert(res[4] == definition)  # definition
        assert(res[5] == speciation)  # speciation
        assert(res[6] == nodv)  # nodata

    @pytest.mark.skipif(True, reason='implement')
    def test_createMethod(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createProcessingLevel(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createSamplingFeature(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createUnit(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createOrganization(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createPerson(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createAffiliation(self):
        pass

    def test_createDataset(self):
        dataset_type_cv = 'Generic'
        code = 'MyNewDataset'
        title = 'Just a test dataset'
        desc = 'this record represents a test dataset'

        res = self.engine.execute('SELECT * from DataSets')
        assert(len(res.fetchall()) == 0)

        # create a new dataset
        d = models.DataSets(
            DataSetTypeCV=dataset_type_cv,
            DataSetCode=code,
            DataSetTitle=title,
            DataSetAbstract=desc,
            DataSetUUID=uuid.uuid4().hex
        )
        dataset = self.writer.createDataset(d)
        assert(dataset == d)
        assert (dataset.DataSetID == 1)

        # assert that this dataset has been successfully inserted
        res = self.engine.execute('SELECT * from DataSets').fetchall()

        assert(len(res) == 1)
        assert(res[0][0] == dataset.DataSetID)

    @pytest.mark.skipif(True, reason='implement')
    def test_createDatasetResults(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createAction(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createActionBy(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createFeatureAction(self):
        pass

    def test_createTimeSeriesResult(self):
        # assert that there are no time series results in the database
        res = self.engine.execute('SELECT * FROM TimeSeriesResults').first()
        assert(res is None)

        # create most basic time series result record possible
        r = models.TimeSeriesResults(
            FeatureActionID=1,
            VariableID=1,
            UnitsID=1,
            ProcessingLevelID=1,
            ValueCount=0,
            SampledMediumCV='unknown',
            ResultTypeCV='time series',
            ResultUUID=str(uuid.uuid4()),
            AggregationStatisticCV='unknown'
        )
        newres = self.writer.createResult(r)
        # assert that this basic tsr exists in the database
        tsr = self.engine.execute('SELECT * FROM TimeSeriesResults').first()
        assert(tsr is not None)

        assert (newres == r)
        result = self.engine.execute('SELECT * FROM Results').first()
        assert(result is not None)

        assert(newres.ResultID == 1)
        assert(result[0] == newres.ResultID)

    @pytest.mark.skipif(True, reason='implement')
    def test_createTimeSeriesResultValues(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createSite(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createSpatialReference(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createDeploymentAction(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createModel(self):
        pass

    @pytest.mark.skipif(True, reason='implement')
    def test_createRelatedModel(self):
        pass

    def test_createSimulation(self):
        # todo: insert should fail if unitID or actionID do not exist
        # assert that there are no datasets in the database
        res = self.engine.execute('SELECT * from Simulations')
        assert(len(res.fetchall()) == 0)

        # create a new simulation
        st = datetime.datetime(2016, 1, 1)
        et = datetime.datetime(2016, 1, 25)
        s = models.Simulations(
            ActionID=1,
            SimulationName='MySimulation',
            SimulationDescription='My simulation description',
            SimulationStartDateTime=st,
            SimulationStartDateTimeUTCOffset=6,
            SimulationEndDateTime=et,
            SimulationEndDateTimeUTCOffset=6,
            TimeStepValue=1,
            TimeStepUnitsID=1,
            InputDataSetID=None,
            ModelID=1
        )
        sim = self.writer.createSimulation(s)
        assert (s == sim)
        assert (s.SimulationID == 1)
        # assert that this record has been successfully inserted
        res = self.engine.execute('SELECT * from Simulations').fetchall()
        assert(len(res) == 1)
        assert(res[0][0] == s.SimulationID)
