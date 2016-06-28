__author__ = 'sreeder'

import datetime as dt
import uuid

# from src.api.ODM2.LikeODM1.model import Site
from odm2api.ODM2.models import *
from odm2api.ODM2 import serviceBase


class CreateODM2(serviceBase):
    '''
    def __init__(self, session):
        self._session = session
    '''
    # ################################################################################
    # Annotations
    # ################################################################################

    def create(self, values):
        if len(values)>1:
            self._session.add_all(values)
        else:
             self._session.add(values)
        self._session.commit()


    def createVariable(self, var):
        self._session.add(var)
        self._session.commit()

        return var

    def createMethod(self, method):
        self._session.add(method)
        self._session.commit()

        return method

    def createProcessingLevel(self, proclevel):
        self._session.add(proclevel)
        self._session.commit()

        return proclevel

    def createSamplingFeature(self, samplingfeature):
        self._session.add(samplingfeature)
        self._session.commit()

        return samplingfeature

    def createUnit(self, unit):
        self._session.add(unit)
        self._session.commit()
        return unit

    def createOrganization(self, org):
        self._session.add(org)
        self._session.commit()
        return org

    def createPerson(self, person):
        self._session.add(person)
        self._session.commit()

        return person

    def createAffiliation(self, affiliation):
        self._session.add(affiliation)
        self._session.commit()

        return affiliation

    def createDataset(self, dataset):
        self._session.add(dataset)
        self._session.commit()

        return dataset

    def createDatasetResults(self, datasetresult):
        self._session.add(datasetresult)
        self._session.commit()

        return datasetresult

    def createAction(self, action):
        self._session.add(action)
        self._session.commit()
        return action

    def createActionby(self, actionby):

        self._session.add(actionby)
        self._session.commit()
        return actionby

    def createRelatedAction(self, relatedaction):
        self._session.add(relatedaction)
        self._session.commit()

        return relatedaction

    def createResult(self, result):
        self._session.add(result)
        self._session.commit()
        return result



    def createResultValue(self, value):
        self._session.add(value)
        self._session.commit()
        self._session.flush()
        return value


    def createSpatialReference(self, spatialref):
        self._session.add(spatialref)
        self._session.commit()

        return spatialref

    def createModel(self, model):
        self._session.add(model)
        self._session.commit()

        return model

    def createRelatedModel(self, relatedmodel):
        self._session.add(relatedmodel)
        self._session.commit()

        return relatedmodel

    def createSimulation(self, simulation):
        self._session.add(simulation)
        self._session.commit()

        return simulation

    def createTimeSeriesResultValues(self, datavalues):
        try:
            tablename = TimeSeriesResultValues.__tablename__
            print "I am TS saving name the table name"+ tablename
            datavalues.to_sql(name="TimeSeriesResultValues",
                              schema=TimeSeriesResultValues.__table_args__['schema'],
                              if_exists='append',
                              chunksize=1000,
                              con=self._session_factory.engine,
                              index=False)
            self._session.commit()

            return datavalues
        except Exception as e:
            print(e)
            return None


#     def createTimeSeriesResultValues(self, resultid, datavalues, datetimes, datetimeoffsets, censorcodecv,
#                                      qualitycodecv,
#                                      timeaggregationinterval, timeaggregationunit):
#
#
#         try:
#             values = TimeSeriesResultValues()
#             for i in range(len(datavalues)):
#                 values.ResultID = resultid
#                 values.CensorCodeCV = censorcodecv
#                 values.QualityCodeCV = qualitycodecv
#                 values.TimeAggregationInterval = timeaggregationinterval
#                 values.TimeAggregationIntervalUnitsID = timeaggregationunit
#                 values.DataValue = datavalues[i]
#                 values.ValueDateTime = datetimes[i]
#                 values.ValueDateTimeUTCOffset = datetimeoffsets[i]
#                 self._session.add(values)
#             self._session.commit()
#             return values
#         except Exception, e:
#             print e
#             return None
#     '''
#
#     def createTimeSeriesResultValues(self, datavalues):
#         try:
#             #using Pandas built-in  --slow
#             #changing way values sent --unknown error on insert
#             #cols = datavalues.columns.tolist()
#             #['ValueDateTime', 'DataValue', 'TimeAggregationInterval', 'TimeAggregationIntervalUnitsID', 'QualityCodeCV', 'CensorCodeCV', 'ResultID', 'ValueDateTimeUTCOffset']
#             #cols = ['ResultID','DataValue','ValueDateTime','ValueDateTimeUTCOffset','CensorCodeCV','QualityCodeCV','TimeAggregationInterval','TimeAggregationIntervalUnitsID']
#             #datavalues = datavalues[cols]
#             #print datavalues
#             #datavalues.to_sql(name=TimeSeriesResultValues.__tablename__,
#             datavalues.to_sql(name="TimeSeriesResultValues",
#                               schema=TimeSeriesResultValues.__table_args__['schema'],
#                               if_exists='append',
#                               chunksize= 1000,
#                               con=self._session_factory.engine,
#                               index=False)
#             self._session.commit()
#
#
#             #using sqlalchemy core --sending empty parameters
#             # data = datavalues.to_dict('records')
#             # self._session.execute(TimeSeriesResultValues.__table__.insert(data))
#
#             #using cursor and StringIO --not all cursors have the copy_from function
#             # print "using cursor"
#             # import cStringIO
#             # #stream the data using 'to_csv' and StringIO(); then use sql's 'copy_from' function
#             # output = cStringIO.StringIO()
#             # #ignore the index
#             # datavalues.to_csv(output, sep='\t', header=False, index=False)
#             # #jump to start of stream
#             # output.seek(0)
#             # contents = output.getvalue()
#             # connection = self._session_factory.engine.raw_connection()
#             # cur = connection.cursor()
#             # #null values become ''
#             # cur.copy_from(output, 'ODM2.TimeSeriesResultValues', null="")
#             # connection.commit()
#             # cur.close()
#
#             #using Bulk Insert  * user must have permissions --file created locally code running remote
#            #  datavalues.to_csv('C:\\Users\\Stephanie\\temp.csv')
#            #  sql = """
#            #     BULK INSERT ODM2.TimeSeriesResultValues
#            #     FROM 'C:\\Users\\Stephanie\\temp.csv' WITH (
#            #     FIELDTERMINATOR=',',
#            #     ROWTERMINATOR='\\n');
#            # """
#            #  self._session.execute(sql)
#
#
#
#
#             return datavalues
#         except Exception, e:
#             print e
#             return None
#