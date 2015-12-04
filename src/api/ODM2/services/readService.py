from sqlalchemy import func
import pandas as pd

from api.ODM2.models import *
from .. import serviceBase


__author__ = 'jmeline'


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
        self.organization = "(" + org.OrganizationCode + ") " +\
                            org.OrganizationName

    #def __repr__(self):
    #    return str(self.name) + " " + str(self.organization)

class ReadODM2( serviceBase   ):
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

    def getCVSamplingFeatureTypes(self):
        """Select all on Sampling Features

        :return CVSamplingFeatureType Objects:
            :type list:
        """
        return self._session.query(CVSamplingFeatureType).all()
    
    def getCVSiteTypes(self):
        """Select all on Sampling Features

        :return CVSiteType Objects:
            :type list:
        """
        return self._session.query(CVSiteType).all()
    
    def getCVSpacialReferenceTypes(self):
        """Select all on SpatialReferences

        :return CVSpacialReferenceType Objects:
            :type list:
        """
        return self._session.query(SpatialReferences).all()

    def getCVSamplingFeatureGeoTypes(self):
        """Select all on Sampling Features

        :return CVSamplingFeatureGeoType Objects:
            :type list:
        """
        return self._session.query(CVSamplingFeatureGeoType).all()

    def getCVElevationDatums(self):
        """Select all on CVElevationDatum

        :return CVElevationDatum Objects:
            :type list:
        """
        return self._session.query(CVElevationDatum).all()
    
    def getCVVariableTypes(self):
        """Select all on CVVariableType

        :return CVVariableType Objects:
            :type list:
        """
        return self._session.query(CVVariableType).all()
    
    def getCVVariableNames(self):
        """Select all on CVVariableName

        :return CVVariableName Objects:
            :type list:
        """
        return self._session.query(CVVariableName).all()
    
    def getCVSpeciations(self):
        """Select all on CVSpeciation

        :return CVSpeciation Objects:
            :type list:
        """
        return self._session.query(CVSpeciation).all()
    
    def getCVUnitsTypes(self):
        """Select all on CVUnitsType

        :return CVUnitsType Objects:
            :type list:
        """
        return self._session.query(CVUnitsType).all()

    def getCVActionTypes(self):
        """
        Select all on CVActionType
        """
        return self._session.query(CVActionType).all()
    
    def getCVMethodTypes(self):
        """
        Select all on CVMethodType
        """
        return self._session.query(CVMethodType).all()
    
    def getCVMediumTypes(self):
        """
        Select all on CVMediumType
        """
        return self._session.query(CVMediumType).all()
    
    def getCVAggregationStatistics(self):
        """
        Select all on CVAggregationStatistic
        """
        return self._session.query(CVAggregationStatistic).all()
    
    def getCVStatus(self):
        """
        Select all on CVStatus
        """
        return self._session.query(CVStatus).all()

# ################################################################################
# Core
# ################################################################################
    
    def getDetailedAffiliationInfo(self):
        q = self._session.query(Affiliations, People, Organizations)\
            .filter(Affiliations.PersonID==People.PersonID)\
            .filter(Affiliations.OrganizationID==Organizations.OrganizationID)
        affiliationList = []
        for a,p,o in q.all():
            detailedAffiliation = DetailedAffiliation(a,p,o)
            affiliationList.append(detailedAffiliation)
        return affiliationList

    def getDetailedResultInfo(self, resultTypeCV, resultID=None):
        q = self._session.query(Results, SamplingFeatures, Methods, Variables,
            ProcessingLevels, Units).filter(Results.VariableID==Variables.VariableID)\
            .filter(Results.UnitsID==Units.UnitsID)\
            .filter(Results.FeatureActionID==FeatureActions.FeatureActionID)\
            .filter(FeatureActions.SamplingFeatureID==SamplingFeatures.SamplingFeatureID)\
            .filter(FeatureActions.ActionID==Actions.ActionID)\
            .filter(Actions.MethodID==Methods.MethodID)\
            .filter(Results.ProcessingLevelID==ProcessingLevels.ProcessingLevelID)\
            .filter(Results.ResultTypeCV==resultTypeCV)
        resultList = []
        if resultID:
            for r,s,m,v,p,u in q.filter_by(ResultID=resultID).all():
                detailedResult = DetailedResult(\
                    r,s,m,v,p,u)
                resultList.append(detailedResult)
        else:
            for r,s,m,v,p,u in q.all():
                detailedResult = DetailedResult(\
                    r,s,m,v,p,u)
                resultList.append(detailedResult)
        return resultList

    """
    Variable
    """

    def getVariables(self):
        """Select all on Variables

        :return Variable Objects:
            :type list:
        """
        return self._session.query(Variables).all()

    def getVariableById(self, variableId):
        """Select by variableId

        :param variableId:
            :type Integer:
        :return Return matching Variable object filtered by variableId:
            :type Variable:
        """
        try:
            return self._session.query(Variables).filter_by(VariableID=variableId).first()
        except:
            return None

    def getVariableByCode(self, variableCode):
        """Select by variableCode

        :param variableCode:
            :type String:
        :return Return matching Variable Object filtered by variableCode:
            :type Variable:
        """
        try:
            return self._session.query(Variables).filter_by(VariableCode=variableCode).first()
        except:
            return None

    def getResultById(self, resultId):
        """Select by variableId

        :param variableId:
            :type Integer:
        :return Return matching Variable object filtered by variableId:
            :type Variable:
        """
        try:
            return self._session.query(Results).filter_by(ResultID=resultId).first()
        except:
            return None
    """
    Method
    """

    def getMethods(self):
        """Select all on Methods

        :return Method Objects:
            :type list:
        """
        return self._session.query(Methods).all()

    def getMethodById(self, methodId):
        """Select by methodId

        :param methodId:
            :type Integer
        :return Return matching Method Object filtered by methodId:
            :type Method:
        """
        try:
            return self._session.query(Methods).filter_by(MethodID=methodId).first()
        except:
            return None

    def getMethodByCode(self, methodCode):
        """Select by methodCode

        :param methodCode:
            :type String:
        :return Return matching Method Object filtered by method Code:
            :type Method:
        """
        try:
            return self._session.query(Methods).filter_by(MethodCode=methodCode).first()
        except:
            return None
    
    def getMethodsByType(self, methodTypeCV):
        return self._session.query(Methods).filter_by(MethodTypeCV=methodTypeCV).all()

    """
    ProcessingLevel
    """

    def getProcessingLevels(self):
        """Select all on Processing Level

        :return ProcessingLevel Objects:
            :type list:
        """
        return self._session.query(ProcessingLevels).all()

    def getProcessingLevelById(self, processingId):
        """Select by processingId

        :param processingId:
            :type Integer:
        :return Return matching ProcessingLevel Object filtered by processingId:
            :type Processinglevel:
        """
        try:
            return self._session.query(ProcessingLevels).filter_by(ProcessingLevelID=processingId).first()
        except:
            return None

    def getProcessingLevelByCode(self, processingCode):
        """Select by processingCode

        :param processingCode:
            :type String(50):
        :return Return matching Processinglevel Object filtered by processingCode:
            :type Processinglevel:
        """
        try:
            return self._session.query(ProcessingLevels).filter_by(ProcessingLevelCode=str(processingCode)).first()
        except Exception, e:
            print e
            return None

    """
    Sampling Feature
    """

    def getSamplingFeatures(self):
        """Select all on SamplingFeatures

        :return SamplingFeature Objects:
            :type list:
        """

        return self._session.query(SamplingFeatures).all()

    def getSamplingFeatureById(self, samplingId):
        """Select by samplingId

        :param samplingId:
            :type Integer:
        :return Return matching SamplingFeature Object filtered by samplingId:
            :type SamplingFeature:
        """
        try:
            return self._session.query(SamplingFeatures).filter_by(SamplingFeatureID=samplingId).first()
        except:
            return None

    def getSamplingFeatureByCode(self, samplingFeatureCode):
        """Select by samplingFeatureCode

        :param samplingFeatureCode:
            :type String:
        :return Return matching SamplingFeature Object filtered by samplingId
            :type list:
        """

        try:
            return self._session.query(SamplingFeatures).filter_by(SamplingFeatureCode=samplingFeatureCode).first()
        except Exception as e:
            return None

    def getSamplingFeaturesByType(self, samplingFeatureTypeCV):
        """Select by samplingFeatureTypeCV

        :param samplingFeatureTypeCV:
            :type String:
        :return Return matching SamplingFeature Objects filtered by samplingFeatureTypeCV:
            :type list:
        """

        try:
            return self._session.query(SamplingFeatures).filter_by(SamplingFeatureTypeCV=samplingFeatureTypeCV).all()
        except Exception as e:
            print e
            return None

    def getSamplingFeatureByGeometry(self, wkt_geometry):

        try:
            # ST_Equals(geometry, geometry)
            return self._session.query(SamplingFeatures).filter(
                func.ST_AsText(SamplingFeatures.FeatureGeometry) == func.ST_AsText(wkt_geometry)).first()
        except Exception, e:
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

    def getActions(self):
        """
        Select all on Action
        """
        return self._session.query(Actions).all()

    def getActionById(self, actionId):
        """
        Select by actionId
        """
        try:
            return self._session.query(Actions).filter_by(ActionID=actionId).first()
        except:
            return None
    
    
    """
    Unit
    """

    def getUnits(self):
        """Select all on Unit

        :return Unit Objects:
            :type list:
        """
        return self._session.query(Units).all()

    def getUnitById(self, unitId):
        """Select by samplingId

        :param unitId:
            :type Integer:
        :return Return matching Unit Object filtered by UnitId:
            :type Unit:
        """
        try:
            return self._session.query(Units).filter_by(UnitsID=unitId).first()
        except:
            return None

    def getUnitByName(self, unitName):


        try:
            return self._session.query(Units).filter(Units.UnitsName.ilike(unitName)).first()
        except:
            return None
    
    def getUnitsByTypeCV(self, unitsTypeCV):
        try:
            return self._session.query(Units).filter(Units.UnitsTypeCV.ilike(unitsTypeCV)).all()
        except:
            return None

    """
    Organization
    """

    def getOrganizations(self):
        """Select all on Organization

        :return Organization Objects:
            :type list:
        """
        return self._session.query(Organizations).all()

    def getOrganizationById(self, orgId):
        """Select by orgId

        :param orgId:
            :type Integer:
        :return Return matching Unit Object filtered by orgId:
            :type Organization:
        """
        try:
            return self._session.query(Organizations).filter_by(OrganizationID=orgId).first()
        except:
            return None

    def getOrganizationByCode(self, orgCode):
        """Select by orgCode

        :param orgCode:
            :type String:
        :return Return matching Organization Object filtered by orgCode
            :type Organization:
        """
        try:
            return self._session.query(Organizations).filter_by(OrganizationCode=orgCode).first()

        except:
            return None

    """
    Person
    """

    def getPeople(self):
        """Select all on Person

        :return Person Objects:
            :type list:
        """
        return self._session.query(People).all()

    def getPersonById(self, personId):
        """Select by personId

        :param personId:
            :type Integer:
        :return Return matching Person Object filtered by personId:
            :type Person:
        """
        try:
            return self._session.query(People).filter_by(PersonID=personId).first()

        except:
            return None

    def getPersonByName(self, personfirst, personlast):
        """Select by person name, last name combination

        :param personfirst: first name of person
        :param personlast: last name of person
        :return Return matching Person Object:
            :type Person:
        """
        try:
            return self._session.query(People).filter(People.PersonFirstName.ilike(personfirst)). \
                filter(People.PersonLastName.ilike(personlast)).first()
        except:
            return None

    def getAllAffiliations(self):
        try:
            return self._session.query(Affiliations).all()
        except:
            return None

    def getAffiliationByPersonAndOrg(self, personfirst, personlast, orgcode):
        """
        Select all affiliation of person
        :param personfirst: first name of person
        :param personlast: last name of person
        :param orgcode: organization code (e.g. uwrl)
        :return: ODM2.Affiliation
        """

        try:
            return self._session.query(Affiliations).filter(Organizations.OrganizationCode.ilike(orgcode)) \
                .filter(People.PersonFirstName.ilike(personfirst)) \
                .filter(People.PersonLastName.ilike(personlast)).first()
        except:
            return None
    
    def getAffiliations(self):
        return self._session.query(Affiliations).all()

    def getAffiliationsByPerson(self, personfirst, personlast):
        """
        Select all affiliation of person
        :param personfirst: first name of person
        :param personlast: last name of person
        :return: [ODM2.Affiliation]
        """

        try:
            return self._session.query(Affiliations).filter(People.PersonFirstName.ilike(personfirst)) \
                .filter(People.PersonLastName.ilike(personlast)).all()
        except:
            return None

    """
    Results
    """

    def getResults(self):

        try:
            return self._session.query(Results).all()
        except:
            return None

    def getResultByActionID(self, actionID):

        try:
            return self._session.query(Results).join(FeatureActions).join(Actions).filter_by(ActionID=actionID).all()
        except:
            return None

    def getResultByID(self, resultID):
        try:
            return self._session.query(Results).filter_by(ResultID=resultID).one()
        except:
            return None

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

    def getResultValidDateTime(self, resultId):
        q = self._session.query(Results.ValidDateTime).filter(Results.ResultID==int(resultId))
        return q.first()

    """
    Datasets
    """

    def getDataSets(self):
        try:
            return self._session.query(DataSets).all()
        except:
            return None

    def getDatasetByCode(self, dscode):

        try:
            return self._session.query(DataSets).filer(DataSets.DataSetCode.ilike(dscode)).first()
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
    TimeSeriesResults
    """

    def getTimeSeriesResults(self):
        """Select all on TimeSeriesResults

        :return TimeSeriesResults Objects:
            :type list:
        """
        return self._session.query(TimeSeriesResults).all()

    def getTimeSeriesResultByResultId(self, resultId):
        """Select by resultID on ResultID

        :param resultId:
            :type Integer:
        :return return matching Timeseriesresult Object filtered by resultId
        """

        try:
            return self._session.query(TimeSeriesResults).filter_by(ResultID=resultId).one()
        except:
            return None

    def getTimeSeriesResultbyCode(self, timeSeriesCode):
        """Select by time
        """
        pass

    """
    TimeSeriesResultValues
    """

    def getTimeSeriesResultValues(self):
        """Select all on TimeSeriesResults

        :return TimeSeriesResultsValue Objects:
            :type list:
        """

        q = self._session.query(TimeSeriesResults).all()
        df = pd.DataFrame([dv.list_repr() for dv in q])
        df.columns = q[0].get_columns()
        return df
        # return self._session.query(Timeseriesresultvalue).all()

    def getTimeSeriesResultValuesByResultId(self, resultId):
        """Select by resultId

        :param timeSeriesId:
            :type Integer:
        :return return matching Timeseriesresultvalue Object filtered by resultId:
            :type Timeseriesresultvalue:
        """
        try:
            q = self._session.query(TimeSeriesResults).filter_by(ResultID=resultId).all()

            df = pd.DataFrame([dv.list_repr() for dv in q])
            df.columns = q[0].get_columns()
            return df
            # return self._session.query(Timeseriesresultvalue).filter_by(ResultID=resultId).all()
        except Exception as e:
            return None

    def getTimeSeriesResultValuesByCode(self, timeSeriesCode):
        """

        :param timeSeriesCode:
        :return:
        """
        pass

    def getTimeSeriesResultValuesByTime(self, resultid, starttime, endtime=None):

        # set end = start if it is None
        endtime = starttime if not endtime else endtime

        try:
            return self._session.query(TimeSeriesResultValues).filter_by(ResultID=resultid) \
                .filter(TimeSeriesResultValues.ValueDateTime >= starttime) \
                .filter(TimeSeriesResultValues.ValueDateTime <= endtime) \
                .order_by(TimeSeriesResultValues.ValueDateTime).all()
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
        return self._session.query(DeploymentAction).all()

        # return self._session.query)

    def getDeploymentActionById(self, deploymentId):
        """Select by deploymentId

        :param deploymentId:
            :type Integer:
        :return Return Matching DeploymentAction Object filtered by deploymentId:
            :type DeploymentAction:
        """
        try:
            return self._session.query(DeploymentAction).filter_by(DeploymentActionID=deploymentId).one()
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
            return self._session.query(Deploymentaction).filter_by(DeploymentActionCode=deploymentCode).one()
        except:
            return None


# ################################################################################
# Simulation
# ################################################################################


    def getAllModels(self):

        try:
            return self._session.query(Model).all()
        except:
            return None

    def getModelByCode(self, modelcode):
        try:
            return self._session.query(Model).filter(Model.ModelCode.ilike(modelcode)).first()
        except:
            return None

    def getAllSimulations(self):

        try:
            return self._session.query(Simulation).all()
        except:
            return None

    def getSimulationByName(self, simulationName):
        try:
            return self._session.query(Simulation).filter(Simulation.SimulationName.ilike(simulationName)).first()
        except:
            return None

    def getSimulationByActionID(self, actionID):
        try:
            return self._session.query(Simulation).filter_by(ActionID=actionID).first()
        except:
            return None

    def getRelatedModelsByID(self, modelid):
        try:
            return self._session.query(Relatedmodel).filter_by(RelatedModelID=modelid).all()
        except:
            return None

    def getRelatedModelsByCode(self, modelcode):
        try:
            return self._session.query(Relatedmodel).join(Relatedmodel.ModelID == Model.ModelID) \
                .filter(Model.ModelCode == modelcode)
        except:
            return None

    def getResultsBySimulationID(self, simulationID):
        try:
            return self._session.query(Result).filter(Simulation.SimulationID == simulationID).all()
        except:
            return None

# ################################################################################
# ODM2
# ################################################################################

class readODM2(object):
   def test(self):
        return None
