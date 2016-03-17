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

    def getAnnotations(self, type=None):

        #TODO What keywords do I use for type
        a = Annotations
        if type =="action": a=ActionAnnotations
        elif type =="categoricalresultvalue": a=CategoricalResultValueAnnotations
        elif type =="equipmentannotation": a=EquipmentAnnotations
        elif type =="measurementresultvalue": a=MeasurementResultValueAnnotations
        elif type =="method": a=MethodAnnotations
        elif type =="pointcoverageresultvalue": a=PointCoverageResultValueAnnotations
        elif type =="profileresultvalue": a= ProfileResultValueAnnotations
        elif type =="result": a = ResultAnnotations
        elif type =="samplingfeature": a=SamplingFeatureAnnotations
        elif type =="sectionresultvalue": a=SectionResultValueAnnotations
        elif type =="spectraresultvalue": a=SpectraResultValueAnnotations
        elif type =="timeSeriesresultvalue": a=TimeSeriesResultValueAnnotations
        elif type =="trajectoryresultvalue": a= TrajectoryResultValueAnnotations
        elif type =="transectresultvalue": a= TransectResultValueAnnotations
        try:
            return self._session.query(a).all()
        except:
            return None


    # ################################################################################
    # CV
    # ##############################################################################

    def getCVs(self, type):

        CV = CVActionType
        if type == "actiontype": CV = CVActionType
        elif type == "aggregationstatistic": CV = CVAggregationStatistic
        elif type == "annotationtype": CV = CVAnnotationType
        elif type == "censorcode": CV = CVCensorCode
        elif type == "dataqualitytype": CV = CVDataQualityType
        elif type == "dataset type": CV = CVDataSetType
        elif type == "Directive Type": CV = CVDirectiveType
        elif type == "Elevation Datum": CV = CVElevationDatum
        elif type == "Equipment Type": CV = CVEquipmentType
        elif type == "Medium": CV = CVMediumType
        elif type == "Method Type": CV = CVMethodType
        elif type == "Organization Type": CV = CVOrganizationType
        elif type == "Property Data Type": CV = CVPropertyDataType
        elif type == "Quality Code": CV = CVQualityCode
        elif type == "Relationship Type": CV = CVRelationshipType
        elif type == "Result Type": CV = CVResultType
        elif type == "Sampling Feature Geo-type": CV = CVSamplingFeatureGeoType
        elif type == "Sampling Feature Type": CV = CVSamplingFeatureType
        elif type == "Site Type": CV = CVSiteType
        elif type == "Spatial Offset Type": CV = CVSpatialOffsetType
        elif type == "Speciation": CV = CVSpeciation
        elif type == "Specimen Type": CV = CVSpecimenType
        elif type == "Status": CV = CVStatus
        elif type == "Taxonomic Classifier Type": CV = CVTaxonomicClassifierType
        elif type == "Units Type": CV = CVUnitsType
        elif type == "Variable Name": CV = CVVariableName
        elif type == "Variable Type": CV = CVVariableType
        else: return None
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
        """
        getVariables()
        * Pass nothing - returns full list of variable objects
        * Pass a VariableID - returns a single variable object
        * Pass a VariableCode - returns a single variable object
        """
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
        """
        * Pass nothing - returns a list of all sampling feature objects with each object of type specific to that sampling feature
        * Pass a SamplingFeatureID - returns a single sampling feature object
        * Pass a SamplingFeatureCode - returns a single sampling feature object
        * Pass a SamplingFeatureType - returns a list of sampling feature objects of the type passed in
        * Pass a SamplingFeatureGeometry(TYPE????) - return a list of sampling feature objects
        """

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

    def getRelatedSamplingFeatures(self, id):
        """

        getRelatedSamplingFeatures()
        * Pass a SamplingFeatureID - get a list of sampling feature objects related to the input sampling feature along with the relationship type
        """

        sf= self._session.query(SamplingFeatures).select_from(RelatedFeatures).join(RelatedFeatures.RelatedFeatureObj)
        if id: sf= sf.filter(RelatedFeatures.RelatedFeatureID == id)
        return sf.all()

    """
    Action
    """

    def getActions(self, id = None, type=None, sfid=None):
        a=Actions
        if type =="equipment": a=EquipmentActions
        elif type =="calibration": a=CalibrationActions
        elif type =="maintenance": a=MaintenanceActions

        q= self._session.query(Actions)
        if id: q= q.filter_by(ActionID=id)
        # if type: q=q.filter_by(Actions.ActionTypeCV.ilike(type))
        if sfid:
            q=q.join(FeatureActions).filter(FeatureActions.SamplingFeatureID == sfid)
            # return self._session.query(Results) \
            #     .join(FeatureActions) \
            #     .join(Actions) \
            #     .join(Simulations) \
            #     .filter(Simulations.SimulationID == simulationid).all()
        try:
            return q.all()
        except:
            return None

    def getRelatedActions(self, actionid=None):

        """
        getRelatedActions()
        * Pass an ActionID - get a list of Action objects related to the input action along with the relatinship type

        """
        q= self._session.query(Actions).select_from(RelatedActions).join(RelatedActions.RelatedActionObj)
        if actionid: q= q.filter(RelatedActions.ActionID ==actionid)

        return q.all()

    """
    Unit
    """

    def getUnits(self, id=None, name=None, type=None):
        """
        getUnits()
    * Pass nothing - returns a list of all units objects
    * Pass UnitsID - returns a single units object
    * Pass UnitsName - returns a single units object
        """


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


    def getAffiliations(self, id,  personfirst=None, personlast=None, orgcode=None):
        """
        Select all affiliation of person
        :param personfirst: first name of person
        :param personlast: last name of person
        :param orgcode: organization code (e.g. uwrl)
        :return: ODM2.Affiliation
        """
        q=self._session.query(Affiliations)
        if id: q=q.filter(AffiliationID = id)
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

    def getResults(self, id=None, actionid = None, type=None):

        #TODO what if user sends in both type and actionid vs just actionid
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
            elif type == "pointcoverage":R = PointCoverageResults
            elif type == "profile": R = ProfileResults
            elif type == "section": R = SectionResults
            elif type == "spectra": R = SpectraResults
            elif type == "timeseries": R = TimeSeriesResults
            elif type == "trajectory": R = TrajectoryResults
            elif type == "transect": R = TransectResults
                # elif "truthObservation": R=

        query = self._session.query(R)
        if actionid: query = query.join(FeatureActions).filter_by(ActionID = actionid)
        if id: query = query.filter_by(ResultID=id)

        # if type: query=query.filter_by(ResultTypeCV=type)
        try:
            return query.all()
        except:
            return None
    #
    #
    # def getResultValidDateTime(self, resultId):
    #     q = self._session.query(Results.ValidDateTime).filter(Results.ResultID == int(resultId))
    #     return q.first()
    #
    # def getResultAndGeomByID(self, resultID):
    #     try:
    #         return self._session.query(Results, SamplingFeatures.FeatureGeometry.ST_AsText()). \
    #             join(FeatureActions). \
    #             join(SamplingFeatures). \
    #             join(Results). \
    #             filter_by(ResultID=resultID).one()
    #     except:
    #         return None
    #
    # def getResultAndGeomByActionID(self, actionID):
    #
    #     try:
    #         return self._session.query(Results, SamplingFeatures.FeatureGeometry.ST_AsText()). \
    #             join(FeatureActions). \
    #             join(SamplingFeatures). \
    #             join(Actions). \
    #             filter_by(ActionID=actionID).all()
    #     except:
    #         return None

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

    def getDataQuality(self):
        """Select all on Data Quality

        :return Dataquality Objects:
            :type list:
        """
        return self._session.query(DataQuality).all()
    #TODO DataQuality Schema Queries
    def getReferenceMaterials(self):
        return self._session.query(ReferenceMaterials).all()
    def getReferenceMaterialValues(self):
        return self._session.query(ReferenceMaterialValues).all()
    def getResultNormalizationValues(self):
        return self._session.query(ResultNormalizationValues).all()
    def getResultsDataQuality(self):
        return self._session.query(ResultsDataQuality).all()

    # ################################################################################
    # Equipment
    # ################################################################################


    #TODO Equipment Schema Queries
    def getEquipment(self, code=None, type = None , sfid=None, actionid=None):
        e = self._session.query(Equipment)
        if sfid: e= e.join(EquipmentUsed)\
            .join(Actions)\
            .join(FeatureActions)\
            .filter(FeatureActions.SamplingFeatureID == sfid)
        if actionid: e=e.join(EquipmentUsed).join(Actions)\
            .filter(Actions.ActionID == actionid)
        return e.all()

    def CalibrationReferenceEquipment(self):
        return self._session.query(CalibrationReferenceEquipment).all()
    def CalibrationStandards(self):
        return self._session.query(CalibrationStandards).all()
    def DataloggerFileColumns(self):
        return self._session.query(DataLoggerFileColumns).all()
    def DataLoggerFiles(self):
        return self._session.query(DataLoggerFiles).all()
    def DataloggerProgramFiles(self):
        return self._session.query(DataLoggerProgramFiles).all()
    def EquipmentModels(self):
        return self._session.query(EquipmentModels).all()
    def EquipmentUsed(self):
        return self._session.query(EquipmentUsed).all()
    def InstrumentOutputVariables(self, modelid=None, variableid=None):
        i=self._session.query(InstrumentOutputVariables)
        if modelid: i=i.filter_by(ModelID=modelid)
        if variableid: i=i.filter_by(VariableID= variableid)
        return i.all()


    def RelatedEquipment(self, code=None):
        r=self._session.query(RelatedEquipment)
        if code: r=r.filter_by(EquipmentCode=code)
        return r.all()

    # ################################################################################
    # Extension Properties
    # ################################################################################

    def getExtensionProperties(self, type=None):
        #Todo what values to use for extensionproperties type
        e = ExtensionProperties
        if type =="action": e = ActionExtensionPropertyValues
        elif type =="citation": e= CitationExtensionPropertyValues
        elif type =="method": e= MethodExtensionPropertyValues
        elif type =="result":e=ResultExtensionPropertyValues
        elif type =="samplingfeature": e= SamplingFeatureExtensionPropertyValues
        elif type =="variable": e=VariableExtensionPropertyValues
        try:
            return self._session.query(e).all()
        except:
            return None


    # ################################################################################
    # External Identifiers
    # ################################################################################
    def getExternalIdentifiers(self, type=None):
        e = ExternalIdentifierSystems
        if type.lowercase =="citation": e = CitationExternalIdentifiers
        elif type =="method": e = MethodExternalIdentifiers
        elif type =="person": e = PersonExternalIdentifiers
        elif type =="referencematerial": e = ReferenceMaterialExternalIdentifiers
        elif type =="samplingfeature": e = SamplingFeatureExternalIdentifiers
        elif type =="spatialreference": e = SpatialReferenceExternalIdentifiers
        elif type =="taxonomicclassifier": e = TaxonomicClassifierExternalIdentifiers
        elif type =="variable": e = VariableExternalIdentifiers
        try:
            return self._session.query(e).all()
        except:
            return None


    # ################################################################################
    # Lab Analyses
    # ################################################################################
    #TODO functions for Lab Analyses
    def getDirectives(self):
        return self._session.query(Directives).all()
    def getActionDirectives(self):
        return self._session.query(ActionDirectives).all()
    def getSpecimenBatchPositions(self):
        return self._session.query(SpecimenBatchPositions).all()



    # ################################################################################
    # Provenance
    # ################################################################################

    #TODO functions for Provenance
    def getAuthorLists(self):
        self._session.query(AuthorLists).all()

    def getDatasetCitations(self):
        self._session.query(DataSetCitations).all()
    def getDerivationEquations(self):
        self._session.query(DerivationEquations).all()
    def getMethodCitations(self):
        self._session.query(MethodCitations).all()

    def getRelatedAnnotations(self):
        #q= read._session.query(Actions).select_from(RelatedActions).join(RelatedActions.RelatedActionObj)
        self._session.query(RelatedAnnotations).all()
    def getRelatedCitations(self):
        self._session.query(RelatedCitations).all()
    def getRelatedDatasets(self):
        self._session.query(RelatedDataSets).all()
    def getRelatedResults(self):
        self._session.query(RelatedResults).all()
    def getResultDerivationEquations(self):
        self._session.query(ResultDerivationEquations).all()

    # ################################################################################
    # Results
    # ################################################################################


    """
    ResultValues
    """



    def getResultValues(self, resultid= None, type=None, starttime=None, endtime=None):

        """Select all on TimeSeriesResults
        getResultValues()
        * Pass a ResultID - Returns a result values object of type that is specific to the result type
        * Pass a ResultID and a date range - returns a result values object of type that is specific to the result type with values between the input date range
        NOTE:  Another option here would be to put a flag on getResults that specifies whether values should be returned
        :return TimeSeriesResultsValue Objects:
            :type list:
        """
        Result=TimeSeriesResults

        if type == "categorical": Result = CategoricalResultValues
        elif type == "measurement": Result = MeasurementResultValues
        elif type == "pointsoverage": Result = PointCoverageResultValues
        elif type == "profile": Result = ProfileResultValues
        elif type == "section": Result = SectionResults
        elif type == "spectra": Result = SpectraResultValues
        elif type == "timeseries": Result = TimeSeriesResultValues
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
    # SamplingFeatures
    # ################################################################################

    """
    Site
    """
    #ToDo function for get sampling features
    def getSites(self):
        """Select all on Sites

        :return Site Objects:
            :type list:
        """
        return self._session.query(Sites).all()

    # def getSiteBySFId(self, siteId):
    #     """Select by siteId
    #
    #     :param siteId:
    #         :type Integer:
    #     :return Return matching Site Object filtered by siteId:
    #         :type Site:
    #     """
    #     try:
    #         return self._session.query(Sites).filter_by(SamplingFeatureID=siteId).one()
    #     except:
    #         return None
    #
    # def getSiteBySFCode(self, siteCode):
    #     """Select by siteCode
    #
    #     :param siteCode:
    #         :type String:
    #     :return Return matching Samplingfeature Object filtered by siteCode:
    #         :type Samplingfeature:
    #     """
    #
    #     sf = self._session.query(SamplingFeatures).filter_by(SamplingFeatureCode=siteCode).one()
    #     return self._session.query(Sites).filter_by(SamplingFeatureID=sf.SamplingFeatureID).one()

    # def getSpatialReferenceByCode(self, srsCode):
    #
    #     try:
    #         return self._session.query(SpatialReferences).filter(SpatialReferences.SRSCode.ilike(srsCode)).first()
    #     except:
    #         return None


    # ################################################################################
    # Equipment
    # ################################################################################




    # ################################################################################
    # Simulation
    # ################################################################################

    def getSimulations(self, name=None, actionid=None):
        """
        getSimulations()
* Pass nothing - get a list of all model simuation objects
* Pass a SimulationName - get a single simulation object
* Pass an ActionID - get a single simulation object
        :param name:
        :type name:
        :param actionid:
        :type actionid:
        :return:
        :rtype:
        """
        s=self._session.query(Simulations)
        if name: s = s.filter(Simulations.SimulationName.ilike(name))
        if actionid: s= s.filter_by(ActionID=actionid)
        try:
            return s.all()
        except:
            return None
    #
    # def getResultsBySimulationID(self, simulationid):
    #     try:
    #         return self._session.query(Results) \
    #             .join(FeatureActions) \
    #             .join(Actions) \
    #             .join(Simulations) \
    #             .filter(Simulations.SimulationID == simulationid).all()
    #     except Exception, e:
    #         print e
    #         return None

    def getModels(self, code= None):
        m= self._session.query(Models)
        if code: m = m.filter(Models.ModelCode.ilike(code))
        try:
            return m.all()
        except:
            return None


    def getRelatedModels(self, id = None, code = None):
        """
        getRelatedModels()
        * Pass a ModelID - get a list of model objects related to the model having ModelID
        * Pass a ModelCode - get a list of model objects related to the model having ModeCode
        :param id:
        :type id:
        :param code:
        :type code:
        :return:
        :rtype:
        """


        m=self._session.query(Models).select_from(RelatedModels).join(RelatedModels.RelatedModelObj)
        if id: m= m.filter(RelatedModels.ModelID==id)
        if code: m= m.filter(RelatedModels.ModelCode == code)

        try:
            return m.all()
        except Exception, e:
            print e
            return None





# ################################################################################
# ODM2
# ################################################################################

class readODM2(object):
    def test(self):
        return None
