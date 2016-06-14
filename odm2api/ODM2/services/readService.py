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

        # TODO What keywords do I use for type
        a = Annotations
        if type == "action":
            a = ActionAnnotations
        elif type == "categoricalresultvalue":
            a = CategoricalResultValueAnnotations
        elif type == "equipmentannotation":
            a = EquipmentAnnotations
        elif type == "measurementresultvalue":
            a = MeasurementResultValueAnnotations
        elif type == "method":
            a = MethodAnnotations
        elif type == "pointcoverageresultvalue":
            a = PointCoverageResultValueAnnotations
        elif type == "profileresultvalue":
            a = ProfileResultValueAnnotations
        elif type == "result":
            a = ResultAnnotations
        elif type == "samplingfeature":
            a = SamplingFeatureAnnotations
        elif type == "sectionresultvalue":
            a = SectionResultValueAnnotations
        elif type == "spectraresultvalue":
            a = SpectraResultValueAnnotations
        elif type == "timeSeriesresultvalue":
            a = TimeSeriesResultValueAnnotations
        elif type == "trajectoryresultvalue":
            a = TrajectoryResultValueAnnotations
        elif type == "transectresultvalue":
            a = TransectResultValueAnnotations
        try:
            return self._session.query(a).all()
        except:
            return None

    # ################################################################################
    # CV
    # ##############################################################################

    def getCVs(self, type):

        CV = CVActionType
        if type == "actiontype":
            CV = CVActionType
        elif type == "aggregationstatistic":
            CV = CVAggregationStatistic
        elif type == "annotationtype":
            CV = CVAnnotationType
        elif type == "censorcode":
            CV = CVCensorCode
        elif type == "dataqualitytype":
            CV = CVDataQualityType
        elif type == "dataset type":
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
        try:
            return self._session.query(CV).all()
        except Exception as e:
            print("Error running Query: %s" % e)

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

    def getVariables(self, ids=None, codes=None):
        """
        getVariables()
        * Pass nothing - returns full list of variable objects
        * Pass a list of VariableID - returns a single variable object
        * Pass a list of VariableCode - returns a single variable object
        """

        query = self._session.query(Variables)
        if ids: query = query.filter(Variables.VariableID.in_(ids))
        if codes: query = query.filter(Variables.VariableCode.in_(codes))
        try:
            return query.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Method
    """

    def getMethods(self, ids=None, codes=None, type=None):

        """
        getMethods()
        * Pass nothing - returns full list of method objects
        * Pass a list of MethodID - returns a single method object
        * Pass a list of MethodCode - returns a single method object
        * Pass a MethodType - returns a list of method objects
        """
        q = self._session.query(Methods)
        if ids: q = q.filter(Methods.MethodID.in_(ids))
        if codes: q = q.filter(Methods.MethodCode.in_(codes))
        if type: q = q.filter_by(MethodTypeCV=type)

        try:
            q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    ProcessingLevel
    """

    def getProcessingLevels(self, ids=None, codes=None):
        """
        getProcessingLevels()
        * Pass nothing - returns full list of ProcessingLevel objects
        * Pass a list of ProcessingLevelID - returns a single processingLevel object
        * Pass a list of ProcessingLevelCode - returns a single processingLevel object
        """
        q = self._session.query(ProcessingLevels)
        if ids: q = q.filter(ProcessingLevels.ProcessingLevels.in_(ids))
        if codes: q = q.filter(ProcessingLevels.ProcessingLevelCode.in_(codes))

        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Sampling Feature
    """

    def getSamplingFeatures(self, ids=None, codes=None, uuids=None, type=None, wkt=None):
        """
        getSamplingFeatures
        * Pass nothing - returns a list of all sampling feature objects with each object of type specific to that sampling feature
        * Pass a list of SamplingFeatureID - returns a single sampling feature object
        * Pass a list of SamplingFeatureCode - returns a single sampling feature object
        * Pass a SamplingFeatureType - returns a list of sampling feature objects of the type passed in
        * Pass a SamplingFeatureGeometry(TYPE????) - return a list of sampling feature objects
        """

        q = self._session.query(SamplingFeatures)

        if type: q = q.filter_by(SamplingFeatureTypeCV=type)
        if ids: q = q.filter(SamplingFeatures.SamplingFeatureID.in_(ids))
        if codes: q = q.filter(SamplingFeatures.SamplingFeatureCode.in_(codes))
        if uuids: q = q.filter(SamplingFeatures.SamplingFeatureUUID.in_(uuids))
        if wkt: q = q.filter_by(FeatureGeometryWKT=wkt)
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    def getRelatedSamplingFeatures(self, id):
        """

        getRelatedSamplingFeatures()
        * Pass a SamplingFeatureID - get a list of sampling feature objects related to the input sampling feature along with the relationship type
        """

        sf = self._session.query(SamplingFeatures).select_from(RelatedFeatures).join(RelatedFeatures.RelatedFeatureObj)
        if id: sf = sf.filter(RelatedFeatures.RelatedFeatureID == id)
        try:
            return sf.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Action
    """

    def getActions(self, ids=None, type=None, sfid=None):

        """
        getSamplingFeatures
        * Pass nothing - returns a list of all Actions
        * Pass a  SamplingFeatureID - returns a single Action object
        * Pass a list of ActionIDs - returns a single Action object
        * Pass a ActionType - returns a list of Action objects of the type passed in
        """
        a = Actions
        if type == "equipment":
            a = EquipmentActions
        elif type == "calibration":
            a = CalibrationActions
        elif type == "maintenance":
            a = MaintenanceActions

        q = self._session.query(a)
        if ids: q = q.filter(a.ActionID.in_(ids))
        if sfid:
            q = q.join(FeatureActions).filter(FeatureActions.SamplingFeatureID == sfid)

        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    def getRelatedActions(self, actionid=None):

        """
        getRelatedActions()
        * Pass an ActionID - get a list of Action objects related to the input action along with the relatinship type

        """
        q = self._session.query(Actions).select_from(RelatedActions).join(RelatedActions.RelatedActionObj)
        if actionid: q = q.filter(RelatedActions.ActionID == actionid)
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Unit
    """

    def getUnits(self, ids=None, name=None, type=None):
        """
        getUnits()
        * Pass nothing - returns a list of all units objects
        * Pass a list of UnitsID - returns a single units object
        * Pass UnitsName - returns a single units object
        """

        q = self._session.query(Units)
        if ids: q = q.filter(Units.UnitsID.in_(ids))
        if name: q = q.filter(Units.UnitsName.ilike(name))
        if type: q = q.filter(Units.UnitsTypeCV.ilike(type))
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Organization
    """

    def getOrganizations(self, ids=None, codes=None):
        """
        getOrganizations()
        * Pass nothing - returns a list of all organization objects
        * Pass a list of OrganizationID - returns a single organization object
        * Pass a list of OrganizationCode - returns a single organization object
        """
        q = self._session.query(Organizations)
        if ids: q = q.filter(Organizations.OrganizationID.in_(ids))
        if codes: q = q.filter(Organizations.OrganizationCode.in_(codes))
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    """
    Person
    """

    def getPeople(self, ids=None, firstname=None, lastname=None):
        """
        getPeople()
        * Pass nothing - returns a list of all People objects
        * Pass a list of PeopleID - returns a single People object
        * Pass a First Name - returns a single People object
        * Pass a Last Name - returns a single People object
        """
        q = self._session.query(People)
        if ids: q = q.filter(People.PersonID.in_(ids))
        if firstname: q = q.filter(People.PersonFirstName.ilike(firstname))
        if lastname: q = q.filter(People.PersonLastName.ilike(lastname))
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    def getAffiliations(self, ids=None, personfirst=None, personlast=None, orgcode=None):
        """
        getAffiliations()
        * Pass nothing - returns a list of all Affiliation objects
        * Pass a list of AffiliationID - returns a single Affiliation object
        * Pass a First Name - returns a single Affiliation object
        * Pass a Last Name - returns a single Affiliation object
        * Pass an OrganizationCode - returns a Affiliation object
        """
        q = self._session.query(Affiliations)

        if ids: q = q.filter(Affiliations.AffiliationID.in_(ids))
        if orgcode: q = q.filter(Organizations.OrganizationCode.ilike(orgcode))
        if personfirst: q = q.filter(People.PersonFirstName.ilike(personfirst))
        if personlast: q = q.filter(People.PersonLastName.ilike(personlast))

        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s"%e)
            return None

    """
    Results
    """

    def getResults(self, ids=None, uuids= None,  actionid=None, simulationid = None):

        # TODO what if user sends in both type and actionid vs just actionid
        """
        getResults()
        * Pass nothing - returns a list of all Results objects
        * Pass a list of ResultID - returns a single Results object
        * Pass an ActionID - returns a single Results object
        """

        query = self._session.query(Results)

        if actionid: query = query.join(FeatureActions).filter_by(ActionID=actionid)
        if simulationid: query = query.join(FeatureActions)\
            .join(Actions)\
            .join(Simulations)\
            .filter_by(SimulationID = simulationid)
        if ids: query = query.filter(Results.ResultID.in_(ids))
        if uuids: query =query.filter(Results.ResultUUID.in_(uuids))

        try:
            return query.all()
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
    #     except Exception as e:
    #         print("Error running Query %s"%e)
    #         return None
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
    #     except Exception as e:
    #         print("Error running Query %s"%e)
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
    #     except Exception as e:
    #         print("Error running Query"%e)
    #         return None

    """
    Datasets
    """

    def getDataSets(self, codes=None, uuids=None):
        """
        getDataSets()
        * Pass nothing - returns a list of all DataSet objects
        * Pass a list of DataSetCode - returns a single DataSet object for each code

        """
        q = self._session.query(DataSets)
        if codes:
            q = q.filter(DataSets.DataSetCode.in_(codes))
        if uuids:
            q.q.filter(DataSets.DataSetUUID.in_(uuids))
        try:
            return q.all()
        except Exception as e:
            print("Error running Query %s"%e)
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

    # TODO DataQuality Schema Queries
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

    # TODO Equipment Schema Queries
    def getEquipment(self, codes=None, type=None, sfid=None, actionid=None):
        """
        getEquipment()
        * Pass nothing - returns a list of all Equipment objects
        * Pass a EquipmentType - returns a single Equipment object
        * Pass a SamplingFeatureID - returns a single Equipment object
        * Pass an ActionID - returns a single Equipment object
        """
        e = self._session.query(Equipment)
        if sfid: e = e.join(EquipmentUsed) \
            .join(Actions) \
            .join(FeatureActions) \
            .filter(FeatureActions.SamplingFeatureID == sfid)
        if codes: e = e.filter(Equipment.EquipmentCode.in_(codes))
        if actionid: e = e.join(EquipmentUsed).join(Actions) \
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
        i = self._session.query(InstrumentOutputVariables)
        if modelid: i = i.filter_by(ModelID=modelid)
        if variableid: i = i.filter_by(VariableID=variableid)
        return i.all()

    def RelatedEquipment(self, code=None):
        r = self._session.query(RelatedEquipment)
        if code: r = r.filter_by(EquipmentCode=code)
        return r.all()

    # ################################################################################
    # Extension Properties
    # ################################################################################

    def getExtensionProperties(self, type=None):
        # Todo what values to use for extensionproperties type
        e = ExtensionProperties
        if type == "action":
            e = ActionExtensionPropertyValues
        elif type == "citation":
            e = CitationExtensionPropertyValues
        elif type == "method":
            e = MethodExtensionPropertyValues
        elif type == "result":
            e = ResultExtensionPropertyValues
        elif type == "samplingfeature":
            e = SamplingFeatureExtensionPropertyValues
        elif type == "variable":
            e = VariableExtensionPropertyValues
        try:
            return self._session.query(e).all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    # ################################################################################
    # External Identifiers
    # ################################################################################
    def getExternalIdentifiers(self, type=None):
        e = ExternalIdentifierSystems
        if type.lowercase == "citation":
            e = CitationExternalIdentifiers
        elif type == "method":
            e = MethodExternalIdentifiers
        elif type == "person":
            e = PersonExternalIdentifiers
        elif type == "referencematerial":
            e = ReferenceMaterialExternalIdentifiers
        elif type == "samplingfeature":
            e = SamplingFeatureExternalIdentifiers
        elif type == "spatialreference":
            e = SpatialReferenceExternalIdentifiers
        elif type == "taxonomicclassifier":
            e = TaxonomicClassifierExternalIdentifiers
        elif type == "variable":
            e = VariableExternalIdentifiers
        try:
            return self._session.query(e).all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    # ################################################################################
    # Lab Analyses
    # ################################################################################
    # TODO functions for Lab Analyses
    def getDirectives(self):
        return self._session.query(Directives).all()

    def getActionDirectives(self):
        return self._session.query(ActionDirectives).all()

    def getSpecimenBatchPositions(self):
        return self._session.query(SpecimenBatchPositions).all()

    # ################################################################################
    # Provenance
    # ################################################################################

    # TODO functions for Provenance
    def getAuthorLists(self):
        self._session.query(AuthorLists).all()

    def getDatasetCitations(self):
        self._session.query(DataSetCitations).all()

    def getDerivationEquations(self):
        self._session.query(DerivationEquations).all()

    def getMethodCitations(self):
        self._session.query(MethodCitations).all()

    def getRelatedAnnotations(self):
        # q= read._session.query(Actions).select_from(RelatedActions).join(RelatedActions.RelatedActionObj)
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

    def getResultValues(self, resultid, starttime=None, endtime=None):

        """Select all on TimeSeriesResults
        getResultValues()
        * Pass a ResultID - Returns a result values object of type that is specific to the result type
        * Pass a ResultID and a date range - returns a result values object of type that is specific to the result type with values between the input date range
        """
        type= self._session.query(Results).filter_by(ResultID=resultid).first().ResultTypeCV
        Result = TimeSeriesResults
        if "categorical" in type.lower():Result = CategoricalResultValues
        elif "measurement" in type.lower():Result = MeasurementResultValues
        elif "point" in type.lower():Result = PointCoverageResultValues
        elif "profile" in type.lower():Result = ProfileResultValues
        elif "section" in type.lower():Result = SectionResults
        elif "spectra" in type.lower():Result = SpectraResultValues
        elif "time" in type.lower():Result = TimeSeriesResultValues
        elif "trajectory" in type.lower():Result = TrajectoryResultValues
        elif "transect" in type.lower():Result = TransectResultValues

        q = self._session.query(Result).filter_by(ResultID=resultid)
        if starttime: q = q.filter(Result.ValueDateTime >= starttime)
        if endtime: q = q.filter(Result.ValueDateTime <= endtime)
        try:
            vals = q.order_by(Result.ValueDateTime)
            df = pd.DataFrame([dv.list_repr() for dv in vals.all()])
            df.columns = vals[0].get_columns()
            return df
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    # ################################################################################
    # SamplingFeatures
    # ################################################################################

    """
    Site
    """

    def getSpatialReferences(self, srsCodes=None):
        """
        getSpatialReference()
        * Pass a ResultID - Returns a result values object of type that is specific to the result type
        * Pass a ResultID and a date range - returns a result values object of type that is specific to the result type with values between the input date range
        """
        q = self._session.query(SpatialReferences)
        if srsCodes: q.filter(SpatialReferences.SRSCode.in_(srsCodes))
        try:
            return q.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None


    # ################################################################################
    # Simulation
    # ################################################################################

    def getSimulations(self, name=None, actionid=None):
        """
        getSimulations()
        * Pass nothing - get a list of all model simuation objects
        * Pass a SimulationName - get a single simulation object
        * Pass an ActionID - get a single simulation object

        """
        s = self._session.query(Simulations)
        if name: s = s.filter(Simulations.SimulationName.ilike(name))
        if actionid: s = s.filter_by(ActionID=actionid)
        try:
            return s.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None



    def getModels(self, codes=None):
        m = self._session.query(Models)
        if codes: m = m.filter(Models.ModelCode.in_(codes))
        try:
            return m.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None

    def getRelatedModels(self, id=None, code=None):
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
# cdoe from master
#+            # note this was RelatedModels.RelatedModelID == Models.ModelID which would return all Parent models of  RelatedModelID
# +            self._session.query(RelatedModels).filter_by(ModelID=modelid).all()
# +            self._session.query(RelatedModels).join(Models, RelatedModels.ModelID == Models.ModelID).filter(Models.ModelCode == modelcode).all()

        m = self._session.query(Models).select_from(RelatedModels).join(RelatedModels.ModelObj)
        if id: m = m.filter(RelatedModels.ModelID == id)
        if code: m = m.filter(Models.ModelCode == code)

#previous version of code
        # m = self._session.query(Models).select_from(RelatedModels).join(RelatedModels.RelatedModelObj)
        # if id: m = m.filter(RelatedModels.ModelID == id)
        # if code: m = m.filter(RelatedModels.ModelCode == code)

        try:
            return m.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None


