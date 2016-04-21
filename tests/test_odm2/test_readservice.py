import pytest
import datetime
from os.path import *
from odm2api.ODM2 import models
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import ReadODM2
from sqlalchemy.orm import class_mapper
import sqlalchemy

# run this test from the root directory using:
# python -m pytest tests/test_odm2/test_readservice.py

globals = {}


def rawSql2Alchemy(rawsqlresult, sqlalchemyClass):
    """
    converts the results of a raw sql select query into SqlAlchemy Model Object
    :param rawsqlresult: array of values, sql select results
    :param sqlalchemyModelObj: model object to convert into
    :return: populated model object
    """

    map = {}
    class_attributes = [prop.key for prop in class_mapper(sqlalchemyClass).iterate_properties
                            if isinstance(prop, sqlalchemy.orm.ColumnProperty)]

    for i in range(len(class_attributes)):
        map[class_attributes[i]] = rawsqlresult[i]

    modelObj = sqlalchemyClass()
    modelObj.__dict__ = map
    return modelObj



class TestReadService:

    @pytest.fixture(scope="class", autouse=True)
    def build_db(self):
        """
        Builds a populated sqlite (in-memory) database for testing
        :return: None
        """

        # path to the ddl script for building the database
        ddlpath= abspath(join(dirname(__file__), 'data/populated.sql'))

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

        self.reader = ReadODM2(db)
        self.engine= db.engine

        globals['reader'] = self.reader
        globals['engine'] = self.engine
        globals['db'] = db
        # return self.write, self.engine

    def setup(self):

        self.reader = globals['reader']
        self.engine = globals['engine']
        self.db = globals['db']




# ################################################################################
# Models
# ################################################################################

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
        resapi = self.reader.getAllModels()

        assert len(res) == len(resapi)

    def test_getModelByCode(self):

        # get a model from the database
        res = self.engine.execute('SELECT * FROM Models').fetchone()
        modelCode = res[1]


        # get the model using the api
        resapi = self.reader.getModelByCode(modelcode=modelCode)

        assert resapi is not None


# ################################################################################
# RelatedModels
# ################################################################################

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
        resapi = self.reader.getRelatedModelsByID(2)

        assert resapi is not None
        assert resapi[0].ModelObj.ModelCode == 'swat'

    def test_getRelatedModelsByCode(self):

        # get related models by id using the api
        resapi = self.reader.getRelatedModelsByCode('swmm')

        assert resapi is not None
        assert len(resapi) > 0
        assert resapi[0].ModelObj.ModelCode == 'swat'

        # test model code that doesn't exist
        resapi = self.reader.getRelatedModelsByCode('None')
        assert resapi is not None
        assert len(resapi) == 0

        # test invalid argument
        resapi = self.reader.getRelatedModelsByCode(models.ActionBy)
        assert resapi is None


# ################################################################################
# Simulations
# ################################################################################

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
        resapi = self.reader.getAllSimulations()

        assert len(res) == len(resapi)

    def test_getSimulationByName(self):

        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        simName = res[2]

        # get simulation by name using the api
        resapi = self.reader.getSimulationByName(simulationName=simName)
        assert resapi is not None

    def test_getSimulationByActionID(self):

        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        actionID = res[1]

        # get simulation by actionid using the api
        resapi = self.reader.getSimulationByActionID(actionID=actionID)
        assert resapi is not None

    def test_getResultsBySimulationID(self):

        # get a simulation from the database
        res = self.engine.execute('SELECT * FROM Simulations').fetchone()
        simulation = rawSql2Alchemy(res, models.Simulations)

        # get the results id associated with the simulation
        res = self.engine.execute('SELECT * from Results as r '\
                'inner join FeatureActions as fa on fa.FeatureActionID == r.FeatureActionID ' \
                'inner join Actions as a on a.ActionID == fa.ActionID ' \
                'inner join Simulations as s on s.ActionID == a.ActionID '\
                'where s.SimulationID = 1').first()
        assert len(res) > 0
        res = rawSql2Alchemy(res, models.Results)
        print res

        # get simulation by id using the api
        resapi = self.reader.getResultsBySimulationID(simulation.SimulationID)
        assert resapi is not None
        assert len(resapi) > 0
        assert res.ResultID == resapi[0].ResultID



