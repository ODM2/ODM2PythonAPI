from __future__ import (absolute_import, division, print_function)

import uuid

from odm2api.ODM2 import serviceBase
from odm2api.ODM2.models import TimeSeriesResultValues

__author__ = 'sreeder'


class CreateODM2(serviceBase):
    # Annotations

    def create(self, value):
        self._session.add(value)
        self._session.commit()
        return value

    def createAll(self, values):
        self._session.add_all(values)
        self._session.commit()
        return values

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
        if samplingfeature.SamplingFeatureUUID is None:
            samplingfeature.SamplingFeatureUUID = str(uuid.uuid1())
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

    def createFeatureAction(self, action):
        self._session.add(action)
        self._session.commit()
        return action

    def createAnnotations(self, anno):
        self._session.add(anno)
        self._session.commit()
        return anno

    def createRelatedAction(self, relatedaction):
        self._session.add(relatedaction)
        self._session.commit()
        return relatedaction

    def createResult(self, result):
        if result.ResultUUID is None:
            result.ResultUUID = str(uuid.uuid1())
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
            # FXIME: F841 local variable 'tablename' is assigned to but never used.
            # tablename = TimeSeriesResultValues.__tablename__
            datavalues.to_sql(
                name='TimeSeriesResultValues',
                schema=TimeSeriesResultValues.__table_args__['schema'],
                if_exists='append',
                chunksize=1000,
                con=self._session_factory.engine,
                index=False
            )
            self._session.commit()

            return datavalues
        except Exception as e:
            print(e)
            return None
