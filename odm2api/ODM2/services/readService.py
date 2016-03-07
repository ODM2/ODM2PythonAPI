__author__ = 'jmeline'

from sqlalchemy import func
import pandas as pd

from odm2api.ODM2 import serviceBase
from odm2api.ODM2.models import *


class DetailedResult:
    def __init__(self, result,
                 samplingFeature,
                 method, variable,
                 processingLevel,
                 unit):
        # result.result_id etc.
        self.resultID = result.ResultID
        self.samplingFeatureCode = samplingFeature.SamplingFeatureCode
        self.methodCode = method.MethodCode
        self.variableCode = variable.VariableCode
        self.processingLevelCode = processingLevel.ProcessingLevelCode
        self.unitsName = unit.UnitsName

        self.samplingFeatureName = samplingFeature.SamplingFeatureName
        self.methodName = method.MethodName
        self.variableNameCV = variable.VariableNameCV
        self.processingLevelDef = processingLevel.Definition


class DetailedAffiliation:
    def __init__(self, affiliation, person, org):
        self.affiliationID = affiliation.AffiliationID
        self.name = person.PersonFirstName + \
                    " " + \
                    person.PersonLastName
        self.organization = "(" + org.OrganizationCode + ") " + \
                            org.OrganizationName

        # def __repr__(self):
        #    return str(self.name) + " " + str(self.organization)


class ReadODM2(serviceBase):
    '''
    def __init__(self, session):
        self._session = session
    '''

    # ################################################################################
    # Annotations
    # ################################################################################




    # ################################################################################
    # CV
    # ################################################################################


    def getCVs(self, type):

        CV = CVActionType
        if type == "ActionType":
            CV = CVActionType
        elif type == "Aggregation Statistic":
            CV = CVAggregationStatistic
        elif type == "Annotation Type":
            CV = CVAnnotationType
        elif type == "Censor Code":
            CV = CVCensorCode
        elif type == "Data Quality Type":
            CV = CVDataQualityType
        elif type == "Dataset Type":
            CV = CVDataSetType
        elif type == "Directive Type":
            CV = CVDirectiveType
        elif type == "Elevation Datum":
            CV = CVElevationDatum
        elif type == "Equipment Type":
            CV = CVEquipmentType
        elif type == "Medium":
            CV = CVMediumType
        elif type == "Method Type":
            CV = CVMethodType
        elif type == "Organization Type":
            CV = CVOrganizationType
        elif type == "Property Data Type":
            CV = CVPropertyDataType
        elif type == "Quality Code":
            CV = CVQualityCode
        elif type == "Relationship Type":
            CV = CVRelationshipType
        elif type == "Result Type":
            CV = CVResultType
        elif type == "Sampling Feature Geo-type":
            CV = CVSamplingFeatureGeoType
        elif type == "Sampling Feature Type":
            CV = CVSamplingFeatureType
        elif type == "Site Type":
            CV = CVSiteType
        elif type == "Spatial Offset Type":
            CV = CVSpatialOffsetType
        elif type == "Speciation":
            CV = CVSpeciation
        elif type == "Specimen Type":
            CV = CVSpecimenType
        elif type == "Status":
            CV = CVStatus
        elif type == "Taxonomic Classifier Type":
            CV = CVTaxonomicClassifierType
        elif type == "Units Type":
            CV = CVUnitsType
        elif type == "Variable Name":
            CV = CVVariableName
        elif type == "Variable Type":
            CV = CVVariableType
        else:
            return None
        return self._session.query(CV).all()

    # ################################################################################
    # Core
    # ################################################################################

    def getDetailedAffiliationInfo(self):
        q = self._session.query(Affiliations, People, Organizations) \
            .filter(Affiliations.PersonID == People.PersonID) \
            .filter(Affiliations.OrganizationID == Organizations.OrganizationID)
        affiliationList = []
        for a, p, o in q.all():
            detailedAffiliation = DetailedAffiliation(a, p, o)
            affiliationList.append(detailedAffiliation)
        return affiliationList

    def getDetailedResultInfo(self, resultTypeCV, resultID=None):
        q = self._session.query(Results, SamplingFeatures, Methods, Variables,
                                ProcessingLevels, Units).filter(Results.VariableID == Variables.VariableID) \
            .filter(Results.UnitsID == Units.UnitsID) \
            .filter(Results.FeatureActionID == FeatureActions.FeatureActionID) \
            .filter(FeatureActions.SamplingFeatureID == SamplingFeatures.SamplingFeatureID) \
            .filter(FeatureActions.ActionID == Actions.ActionID) \
            .filter(Actions.MethodID == Methods.MethodID) \
            .filter(Results.ProcessingLevelID == ProcessingLevels.ProcessingLevelID) \
            .filter(Results.ResultTypeCV == resultTypeCV)
        resultList = []
        if resultID:
            for r, s, m, v, p, u in q.filter_by(ResultID=resultID).all():
                detailedResult = DetailedResult( \
                    r, s, m, v, p, u)
                resultList.append(detailedResult)
        else:
            for r, s, m, v, p, u in q.all():
                detailedResult = DetailedResult( \
                    r, s, m, v, p, u)
                resultList.append(detailedResult)
        return resultList

    """
    Taxonomic Classifiers
    """

    def getTaxonomicClassifiers(self):
        return self._session.query(TaxonomicClassifiers).all()

    """
    Variable
    """

    def getVariables(self, id=None, code=None):
        query = self._session.query(Variables)
        if id: query = query.filter_by(VariableID=id)
        if code: query = query.filter_by(VariableCode=code)
        try:
            return query.all()
        except:
            return None

    """
    Method
    """

    def getMethods(self, id=None, code=None, type=None):
        q = self._session.query(Methods)
        if id: q = q.filter_by(MethodID=id)
        if code: q = q.filter_by(MethodCode=str(code))
        if type: q = q.filter_by(MethodTypeCV=type)

        try:
            q.all()
        except:
            return None

    """
    ProcessingLevel
    """

    def getProcessingLevels(self, id=None, code=None):

        q = self._session.query(ProcessingLevels)
        if id: q = q.filter_by(ProcessingLevelID=id)
        if code: q = q.filter_by(ProcessingLevelCode=str(code))

        try:
            return q.all()
        except:
            return None

    """
    Sampling Feature
    """

    def getSamplingFeatures(self, id=None, code=None, type=None, wkt=None):
        q = self._session.query(SamplingFeatures)

        if type: q = q.filter_by(SamplingFeatureTypeCV=type)
        if id: q = q.filter_by(SamplingFeatureID=id)
        if code: q = q.filter_by(SamplingFeatureCode=code)
        if wkt: q = q.filter_by(FeatureGeometryWKT=wkt)
        try:
            return q.all()
        except Exception as e:
            print e
            return None

    def getGeometryTest(self, TestGeom):
        Geom = self._session.query(SamplingFeatures).first()
        print "Queried Geometry: ", self._session.query(Geom.FeatureGeometry.ST_AsText()).first()
        GeomText = self._session.query(
            func.ST_Union(Geom.FeatureGeometry, func.ST_GeomFromText(TestGeom)).ST_AsText()).first()

        print GeomText

    """
    Action
    """

    def getActions(self, id = None):

        q= self._session.query(Actions)
        if id: q= q.filter_by(ActionID=id)
        try:
            return q.all()
        except:
            return None


    """
    Unit
    """

    def getUnits(self, id=None, name=None, type=None):
        q = self._session.query(Units)
        if id: q = q.filter_by(UnitsID=id)
        if name: q = q.filter(Units.UnitsName.ilike(name))
        if type: q = q.filter(Units.UnitsTypeCV.ilike(type))
        try:
            return q.all()
        except:
            return None



    """
    Organization
    """

    def getOrganizations(self, id =None, code =None):
        """Select all on Organization

        :return Organization Objects:
            :type list:
        """
        q = self._session.query(Organizations)
        if id: q = q.filter_by(OrganizationID=id)
        if code:q = q.filter_by(OrganizationCode=code)
        try:
            return q.all()
        except:
            return None



    """
    Person
    """

    def getPeople(self, id =None, firstname=None, lastname=None):
        """Select all on Person

        :return Person Objects:
            :type list:
        """
        q = self._session.query(People)
        if id: q = q.filter_by(PersonID=id)
        if firstname: q = q.filter(People.PersonFirstName.ilike(firstname))
        if lastname: q = q.filter(People.PersonLastName.ilike(lastname))
        try:
            return q.all()
        except:
            return None


    def getAffiliations(self, personfirst=None, personlast=None, orgcode=None):
        """
        Select all affiliation of person
        :param personfirst: first name of person
        :param personlast: last name of person
        :param orgcode: organization code (e.g. uwrl)
        :return: ODM2.Affiliation
        """
        q=self._session.query(Affiliations)

        if orgcode: q = q.filter(Organizations.OrganizationCode.ilike(orgcode))
        if personfirst: q = q.filter(People.PersonFirstName.ilike(personfirst))
        if personlast: q = q.filter(People.PersonLastName.ilike(personlast)).first()
        try:
            return q.all()
        except:
            return None

    """
    Results
    """

    def getResults(self, id=None, type=None):
        """Select by variableId

         :param id:
             :type Integer:
         :return Return matching Variable object filtered by variableId:
             :type Variable:
         """
        R = Results
        if type is not None:
            if type == "categorical": R = CategoricalResults
            # elif "countObservation": R=
            elif type == "measurement": R = MeasurementResults
            elif type == "pointCoverage":R = PointCoverageResults
            elif type == "profile": R = ProfileResults
            elif type == "section": R = SectionResults
            elif type == "spectra": R = SpectraResults
            elif type == "timeSeries": R = TimeSeriesResults
            elif type == "trajectory": R = TrajectoryResults
            elif type == "transect": R = TransectResults
                # elif "truthObservation": R=

        query = self._session.query(R)
        if id: query = query.filter_by(ResultID=id)
        # if type: query=query.filter_by(ResultTypeCV=type)
        try:
            return query.all()
        except:
            return None

    def getResultByActionID(self, actionID):

        try:
            return self._session.query(Results).join(FeatureActions).join(Actions).filter_by(ActionID=actionID).all()
        except:
            return None

    def getResultValidDateTime(self, resultId):
        q = self._session.query(Results.ValidDateTime).filter(Results.ResultID == int(resultId))
        return q.first()

    def getResultAndGeomByID(self, resultID):
        try:
            return self._session.query(Results, SamplingFeatures.FeatureGeometry.ST_AsText()). \
                join(FeatureActions). \
                join(SamplingFeatures). \
                join(Results). \
                filter_by(ResultID=resultID).one()
        except:
            return None

    def getResultAndGeomByActionID(self, actionID):

        try:
            return self._session.query(Results, SamplingFeatures.FeatureGeometry.ST_AsText()). \
                join(FeatureActions). \
                join(SamplingFeatures). \
                join(Actions). \
                filter_by(ActionID=actionID).all()
        except:
            return None

    """
    Datasets
    """

    def getDataSets(self, code=None):
        q = self._session.query(DataSets)
        if code:
            q = q.filter(DataSets.DataSetCode.ilike(code))
        try:
            return q.all()
        except:
            return None


    # ################################################################################
    # Data Quality
    # ################################################################################

    def getAllDataQuality(self):
        """Select all on Data Quality

        :return Dataquality Objects:
            :type list:
        """
        return self._session.query(DataQuality).all()

    # ################################################################################
    # Equipment
    # ################################################################################


    def getAllEquipment(self):
        return self._session.query(Equipment).all()

    # ################################################################################
    # Extension Properties
    # ################################################################################

    def getExtensionProperties(self ):
        pass

    # ################################################################################
    # External Identifiers
    # ################################################################################




    # ################################################################################
    # Lab Analyses
    # ################################################################################




    # ################################################################################
    # Provenance
    # ################################################################################


    """
    Citation
    """

    def getCitations(self):
        self._session.query(Citations).all()

    # ################################################################################
    # Results
    # ################################################################################


    """
    ResultValues
    """



    def getResultValues(self, resultid= None, type=None, starttime=None, endtime=None):
        """Select all on TimeSeriesResults

        :return TimeSeriesResultsValue Objects:
            :type list:
        """
        Result=TimeSeriesResults

        if type == "categorical": Result = CategoricalResultValues
        elif type == "measurement": Result = MeasurementResultValues
        elif type == "pointCoverage": Result = PointCoverageResultValues
        elif type == "profile": Result = ProfileResultValues
        elif type == "section": Result = SectionResults
        elif type == "spectra": Result = SpectraResultValues
        elif type == "timeSeries": Result = TimeSeriesResultValues
        elif type == "trajectory": Result = TrajectoryResultValues
        elif type == "transect": Result = TransectResultValues



        q = self._session.query(Result)
        if resultid: q = q.filter_by(ResultID=resultid)
        if starttime: q= q.filter(Result.ValueDateTime >= starttime)
        if endtime: q=q.filter(Result.ValueDateTime <= endtime)
        try:
            q=q.order_by(Result.ValueDateTime).all()
            df = pd.DataFrame([dv.list_repr() for dv in q.all()])
            df.columns = q[0].get_columns()
            return df
        except:
            return None



            # ################################################################################
            # Annotations
            # ################################################################################

    """
    Site
    """

    def getAllSites(self):
        """Select all on Sites

        :return Site Objects:
            :type list:
        """
        return self._session.query(Sites).all()

    def getSiteBySFId(self, siteId):
        """Select by siteId

        :param siteId:
            :type Integer:
        :return Return matching Site Object filtered by siteId:
            :type Site: 
        """
        try:
            return self._session.query(Sites).filter_by(SamplingFeatureID=siteId).one()
        except:
            return None

    def getSiteBySFCode(self, siteCode):
        """Select by siteCode

        :param siteCode:
            :type String:
        :return Return matching Samplingfeature Object filtered by siteCode:
            :type Samplingfeature:
        """

        sf = self._session.query(SamplingFeatures).filter_by(SamplingFeatureCode=siteCode).one()
        return self._session.query(Sites).filter_by(SamplingFeatureID=sf.SamplingFeatureID).one()

    def getSpatialReferenceByCode(self, srsCode):

        try:
            return self._session.query(SpatialReferences).filter(SpatialReferences.SRSCode.ilike(srsCode)).first()
        except:
            return None


            # ################################################################################
            # Sensors
            # ################################################################################

    def getAllDeploymentAction(self):
        """Select all on DeploymentAction

        :return DeploymentAction Objects:
            :type list:
        """
        return self._session.query(DeploymentActions).all()

        # return self._session.query)

    def getDeploymentActionById(self, deploymentId):
        """Select by deploymentId

        :param deploymentId:
            :type Integer:
        :return Return Matching DeploymentAction Object filtered by deploymentId:
            :type DeploymentAction:
        """
        try:
            return self._session.query(DeploymentActions).filter_by(DeploymentActionID=deploymentId).one()
        except:
            return None

    def getDeploymentActionByCode(self, deploymentCode):
        """Select by deploymentCode

        :param deploymentCode:
            :type String:
        :return Return matching DeploymentAction Object filtered by deploymentCode:
            :type DeploymentAction:
        """
        try:
            return self._session.query(DeploymentActions).filter_by(DeploymentActionCode=deploymentCode).one()
        except:
            return None


            # ################################################################################
            # Simulation
            # ################################################################################

    def getAllModels(self):

        try:
            return self._session.query(Models).all()
        except:
            return None

    def getModelByCode(self, modelcode):
        try:
            return self._session.query(Models).filter(Models.ModelCode.ilike(modelcode)).first()
        except:
            return None

    def getAllSimulations(self):

        try:
            return self._session.query(Simulations).all()
        except:
            return None

    def getSimulationByName(self, simulationName):
        try:
            return self._session.query(Simulations).filter(Simulations.SimulationName.ilike(simulationName)).first()
        except:
            return None

    def getSimulationByActionID(self, actionID):
        try:
            return self._session.query(Simulations).filter_by(ActionID=actionID).first()
        except:
            return None

    def getRelatedModelsByID(self, modelid):
        """
        queries the ODM2 for any models that have a relationship with the provided model id
        :param modelid: id of the model to search
        :return: all models related to the specified id
        """
        try:
            return self._session.query(RelatedModels).filter_by(RelatedModelID=modelid).all()
        except Exception, e:
            print e
        return None

    def getRelatedModelsByCode(self, modelcode):
        """
        queries the ODM2 for any models that have a relationship with the provided model id
        :param modelcode: the code of the model to search
        :return: all models related to the provided model code
        """
        try:
            return self._session.query(RelatedModels).join(Models, RelatedModels.RelatedModelID == Models.ModelID) \
                .filter(Models.ModelCode == modelcode).all()
        except Exception, e:
            print e
        return None

    def getResultsBySimulationID(self, simulationID):
        try:
            return self._session.query(Results) \
                .join(FeatureActions) \
                .join(Actions) \
                .join(Simulations) \
                .filter(Simulations.SimulationID == simulationID).all()
        except Exception, e:
            print e
        return None


# ################################################################################
# ODM2
# ################################################################################

class readODM2(object):
    def test(self):
        return None
