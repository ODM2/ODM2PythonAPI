from __future__ import (absolute_import, division, print_function)

from os.path import abspath, dirname, join

from odm2api.ODM2 import models
from odm2api.ODM2.services.readService import ReadODM2
from odm2api.ODMconnection import dbconnection

import pytest

import sqlalchemy
from sqlalchemy.orm import class_mapper


globals_vars = {}


def rawSql2Alchemy(rawsqlresult, sqlalchemyClass):
    """
    converts the results of a raw sql select query into SqlAlchemy converter Object
    :param rawsqlresult: array of values, sql select results
    :param sqlalchemyModelObj: converter object to convert into
    :return: populated converter object

    """
    m = {}
    class_attributes = [
        prop.key for prop in class_mapper(sqlalchemyClass).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)
    ]

    for i in range(len(class_attributes)):
        m[class_attributes[i]] = rawsqlresult[i]

    modelObj = sqlalchemyClass()
    modelObj.__dict__ = m
    return modelObj


class TestReadService:
    @pytest.fixture(scope='class', autouse=True)
    def build_db(self):
        """
        Builds a populated sqlite (in-memory) database for testing
        :return: None

        """
        # path to the ddl script for building the database
        ddlpath = abspath(join(dirname(__file__), 'data/populated.sql'))

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

        self.reader = ReadODM2(db)
        self.engine = db.engine

        globals_vars['reader'] = self.reader
        globals_vars['engine'] = self.engine
        globals_vars['db'] = db

    def setup(self):
        self.reader = globals_vars['reader']
        self.engine = globals_vars['engine']
        self.db = globals_vars['db']


# Sampling Features
    def test_getAllSamplingFeatures(self):
        # get all models from the database
        res = self.engine.execute('SELECT * FROM SamplingFeatures').fetchall()
        # get all simulations using the api
        resapi = self.reader.getSamplingFeatures()
        assert len(res) == len(resapi)

    def test_getSamplingFeatureByID(self):
        # get all models from the database
        res = self.engine.execute('SELECT * FROM SamplingFeatures').fetchone()
        sfid = res[0]
        # get all simulations using the api
        resapi = self.reader.getSamplingFeatures(ids=[sfid])
        assert resapi is not None

# Models
    """
        TABLE Models
        ModelID INTEGER   NOT NULL PRIMARY KEY,
        ModelCode VARCHAR (50)  NOT NULL,
        ModelName VARCHAR (255)  NOT NULL,
        ModelDescription VARCHAR (500)  NULL,
        Version VARCHAR (255)  NULL,
        ModelLink VARCHAR (255)  NULL
    """

    def test_getAllModels(self):
        # get all models from the database
        res = self.engine.execute('SELECT * FROM Models').fetchall()
        # get all simulations using the api
        resapi = self.reader.getModels()
        assert len(res) == len(resapi)

    def test_getModelByCode(self):
        # get a converter from the database
        res = self.engine.execute('SELECT * FROM Models').fetchone()
        modelCode = res[1]
        # get the converter using the api
        resapi = self.reader.getModels(codes=[modelCode])
        assert resapi is not None


# RelatedModels
    """
        TABLE RelatedModels (
        RelatedID INTEGER   NOT NULL PRIMARY KEY,
        ModelID INTEGER   NOT NULL,
        RelationshipTypeCV VARCHAR (255)  NOT NULL,
        RelatedModelID INTEGER   NOT NULL,
        FOREIGN KEY (RelationshipTypeCV) REFERENCES CV_RelationshipType (Name)
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY (ModelID) REFERENCES Models (ModelID)
        ON UPDATE NO ACTION ON DELETE NO ACTION
    """

    def test_getRelatedModelsByID(self):
        # get related models by id using the api
        resapi = self.reader.getRelatedModels(id=1)
        assert resapi is not None
        assert resapi[0].ModelCode == 'swat'

    def test_getRelatedModelsByCode(self):
        # get related models by id using the api
        resapi = self.reader.getRelatedModels(code='swat')
        assert resapi is not None
        assert len(resapi) > 0
        print(resapi[0].ModelCode)
        assert resapi[0].ModelCode == 'swat'
        # test converter code that doesn't exist
        resapi = self.reader.getRelatedModels(code='None')

        assert resapi is not None
        assert len(resapi) == 0

        # test invalid argument
        resapi = self.reader.getRelatedModels(code=234123)
        assert not resapi


# Results
    """
        TABLE Results (
        ResultID INTEGER   NOT NULL PRIMARY KEY,
        ResultUUID VARCHAR(36)   NOT NULL,
        FeatureActionID INTEGER   NOT NULL,
        ResultTypeCV VARCHAR (255)  NOT NULL,
        VariableID INTEGER   NOT NULL,
        UnitsID INTEGER   NOT NULL,
        TaxonomicClassifierID INTEGER   NULL,
        ProcessingLevelID INTEGER   NOT NULL,
        ResultDateTime DATETIME   NULL,
        ResultDateTimeUTCOffset INTEGER   NULL,
        ValidDateTime DATETIME   NULL,
        ValidDateTimeUTCOffset INTEGER   NULL,
        StatusCV VARCHAR (255)  NULL,
        SampledMediumCV VARCHAR (255)  NOT NULL,
        ValueCount INTEGER   NOT NULL
    """
    def test_getAllResults(self):
        # get all results from the database
        res = self.engine.execute('SELECT * FROM Results').fetchall()
        print(res)
        # get all results using the api
        resapi = self.reader.getResults()
        assert len(res) == len(resapi)

    def test_getResultsByID(self):
        # get a result from the database
        res = self.engine.execute('SELECT * FROM Results').fetchone()
        resultid = res[1]

        # get the result using the api
        resapi = self.reader.getResults(ids=[resultid])
        assert resapi is not None

# Simulations
    """
        TABLE Simulations (
        SimulationID INTEGER   NOT NULL PRIMARY KEY,
        ActionID INTEGER   NOT NULL,
        SimulationName VARCHAR (255)  NOT NULL,
        SimulationDescription VARCHAR (500)  NULL,
        SimulationStartDateTime DATETIME   NOT NULL,
        SimulationStartDateTimeUTCOffset INTEGER   NOT NULL,
        SimulationEndDateTime DATETIME   NOT NULL,
        SimulationEndDateTimeUTCOffset INTEGER   NOT NULL,
        TimeStepValue FLOAT   NOT NULL,
        TimeStepUnitsID INTEGER   NOT NULL,
        InputDataSetID INTEGER   NULL,
        ModelID INTEGER   NOT NULL,
    """

    def test_getAllSimulations(self):
        # get all simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchall()
        # get all simulations using the api
        resapi = self.reader.getSimulations()
        assert len(res) == len(resapi)

    def test_getSimulationByName(self):
        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        simName = res[2]
        # get simulation by name using the api
        resapi = self.reader.getSimulations(name=simName)
        assert resapi is not None

    def test_getSimulationByActionID(self):
        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        actionID = res[1]
        # get simulation by actionid using the api
        resapi = self.reader.getSimulations(actionid=actionID)
        assert resapi is not None

    def test_getResultsBySimulationID(self):
        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        simulation = rawSql2Alchemy(res, models.Simulations)
        # get the results id associated with the simulation
        res = self.engine.execute(
            'SELECT * from Results as r '
            'inner join FeatureActions as fa on fa.FeatureActionID == r.FeatureActionID '
            'inner join Actions as a on a.ActionID == fa.ActionID '
            'inner join Simulations as s on s.ActionID == a.ActionID '
            'where s.SimulationID = 1'
        ).first()
        assert len(res) > 0
        res = rawSql2Alchemy(res, models.Results)
        print(res)

        # get simulation by id using the api
        # resapi = self.reader.getResultsBySimulationID(simulation.SimulationID)
        resapi = self.reader.getResults(simulationid=simulation.SimulationID)

        assert resapi is not None
        assert len(resapi) > 0
        assert res.ResultID == resapi[0].ResultID
