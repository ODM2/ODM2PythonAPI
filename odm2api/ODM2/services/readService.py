__author__ = 'sreeder'

from sqlalchemy import func ,not_, bindparam, distinct, exists
import pandas as pd

from odm2api.ODM2 import serviceBase
from odm2api.ODM2.models import *


class DetailedResult:
    def __init__(self, action, result,
                 sc, sn,
                 method, variable,
                 processingLevel,
                 unit):
        # result.result_id etc.
        self.ResultID = result.ResultID
        self.SamplingFeatureCode = sc#.SamplingFeatureCode
        self.MethodCode = method.MethodCode
        self.VariableCode = variable.VariableCode
        self.ProcessingLevelCode = processingLevel.ProcessingLevelCode
        self.UnitsName = unit.UnitsName

        self.SamplingFeatureName = sn#.SamplingFeatureName
        self.MethodName = method.MethodName
        self.VariableNameCV = variable.VariableNameCV
        self.ProcessingLevelDefinition = processingLevel.Definition
        self.ValueCount = result.ValueCount
        self.BeginDateTime = action.BeginDateTime
        self.EndDateTime = action.EndDateTime
        self.ResultObj = result


class DetailedAffiliation:
    def __init__(self, affiliation, person, org):
        self.AffiliationID = affiliation.AffiliationID
        self.Name = person.PersonFirstName + \
                    " " + \
                    person.PersonLastName
        self.Organization = "(" + org.OrganizationCode + ") " + \
                            org.OrganizationName

        # def __repr__(self):
        #    return str(self.name) + " " + str(self.organization)


class ReadODM2(serviceBase):
    '''
    def __init__(self, session):
        self._session = session
    '''


    # ################################################################################
    # Exists functions
    # ################################################################################

    def resultExists(self, result):
        """

        :param result
        :return: Series
        """
        # unique Result
        # FeatureActionID, ResultTypeCV, VariableID, UnitsID, ProcessingLevelID, SampledMediumCV

        try:

            ret = self._session.query(exists().where(Results.ResultTypeCV == result.ResultTypeCV)
                                      .where(Results.VariableID == result.VariableID)
                                      .where(Results.UnitsID == result.UnitsID)
                                      .where(Results.ProcessingLevelID == result.ProcessingLevelID)
                                      .where(Results.SampledMediumCV == result.SampledMediumCV)
                                      )
            # where(Results.FeatureActionID == result.FeatureActionID).
            return ret.scalar()

        except:
            return None

    # ################################################################################
    # Annotations
    # ################################################################################

    def getAnnotations(self, type=None, codes = None, ids = None):

        # TODO What keywords do I use for type
        a = Annotations
        if type:
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
            elif type == "timeseriesresultvalue":
                a = TimeSeriesResultValueAnnotations
            elif type == "trajectoryresultvalue":
                a = TrajectoryResultValueAnnotations
            elif type == "transectresultvalue":
                a = TransectResultValueAnnotations
        try:
            query=self._session.query(a)
            if codes:
                query = query.filter(Annotations.AnnotationCode.in_(codes))
            if ids:
                query = query.filter(Annotations.AnnotationID.in_(ids))
            return query.all()

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

    def getDetailedResultInfo(self, resultTypeCV=None, resultID=None, sfID=None):
        #TODO can this be done by just getting the result object and drilling down? what is the performance comparison
        q = self._session.query(Actions, Results, SamplingFeatures.SamplingFeatureCode, SamplingFeatures.SamplingFeatureName, Methods, Variables,
                                ProcessingLevels, Units).filter(Results.VariableID == Variables.VariableID) \
            .filter(Results.UnitsID == Units.UnitsID) \
            .filter(Results.FeatureActionID == FeatureActions.FeatureActionID) \
            .filter(FeatureActions.SamplingFeatureID == SamplingFeatures.SamplingFeatureID) \
            .filter(FeatureActions.ActionID == Actions.ActionID) \
            .filter(Actions.MethodID == Methods.MethodID) \
            .filter(Results.ProcessingLevelID == ProcessingLevels.ProcessingLevelID) \
            .filter(Results.ResultTypeCV == resultTypeCV) \
            .order_by(Results.ResultID)
        resultList = []
        if sfID:
            q = q.filter(SamplingFeatures.SamplingFeatureID == sfID)
        if resultID:
            q = q.filter(Results.ResultID==resultID)

        for a, r, sc, sn, m, v, p, u in q.all():
            detailedResult = DetailedResult( \
                a, r, sc, sn, m, v, p, u)
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

    def getVariables(self, ids=None, codes=None, sitecode=None, results= False):
        """
        getVariables()
        * Pass nothing - returns full list of variable objects
        * Pass a list of VariableID - returns a single variable object
        * Pass a list of VariableCode - returns a single variable object
        * Pass a SiteCode - returns a list of Variable objects that are collected at the given site.
        * Pass whether or not you want to return the sampling features that have results associated with them
        """

        if sitecode:
            try:
                ids = [x[0] for x in
                           self._session.query(distinct(Results.VariableID))
                               .filter(Results.FeatureActionID == FeatureActions.FeatureActionID)
                               .filter(FeatureActions.SamplingFeatureID == SamplingFeatures.SamplingFeatureID)
                               .filter(SamplingFeatures.SamplingFeatureCode == sitecode).all()
                           ]
            except:
                ids = None


        if results:
            try:
                ids = [x[0] for x in self._session.query(distinct(Results.VariableID)).all()]
            except:
                ids = None

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
            return q.all()
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

    def getSamplingFeatures(self, ids=None, codes=None, uuids=None, type=None, wkt=None, results=False):
        """
        getSamplingFeatures
        * Pass nothing - returns a list of all sampling feature objects with each object of type specific to that sampling feature
        * Pass a list of SamplingFeatureID - returns a single sampling feature object
        * Pass a list of SamplingFeatureCode - returns a single sampling feature object
        * Pass a SamplingFeatureType - returns a list of sampling feature objects of the type passed in
        * Pass a SamplingFeatureGeometry(TYPE????) - return a list of sampling feature objects
        * Pass whether or not you want to return the sampling features that have results associated with them
        """
        if results:
            try:
                fas = [x[0] for x in self._session.query(distinct(Results.FeatureActionID)).all()]
            except:
                return None

            sf = [x[0] for x in self._session.query(distinct(FeatureActions.SamplingFeatureID))
                                                    .filter(FeatureActions.FeatureActionID.in_(fas)).all()]

            ids = sf
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

    def getRelatedSamplingFeatures(self, sfid=None, rfid = None, relationshiptype=None):
        #TODO: add functionality to filter by code
        """

        getRelatedSamplingFeatures()
        * Pass a SamplingFeatureID - get a list of sampling feature objects related to the input sampling feature along with the relationship type
        * Pass a SamplingFeatureCode
        """
        # q = session.query(Address).select_from(User). \
        #     join(User.addresses). \
        #     filter(User.name == 'ed')
        #throws an error when joining entire samplingfeature, works fine when just getting an element. this is being caused by the sampling feature inheritance

        sf = self._session.query(distinct(SamplingFeatures.SamplingFeatureID))\
                                .select_from(RelatedFeatures)


        if sfid: sf = sf.join(RelatedFeatures.RelatedFeatureObj).filter(RelatedFeatures.SamplingFeatureID == sfid)
        if rfid: sf = sf.join(RelatedFeatures.SamplingFeatureObj).filter(RelatedFeatures.RelatedFeatureID == rfid)
        if relationshiptype: sf = sf.filter(RelatedFeatures.RelationshipTypeCV == relationshiptype)
        try:
            sfids =[x[0] for x in sf.all()]
            if len(sfids)>0:
                sflist= self.getSamplingFeatures(ids=sfids)
                return sflist

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

    def getResults(self, ids=None, type=None, uuids=None, actionid=None, simulationid=None, sfid=None,
                   variableid=None, siteid=None):

        # TODO what if user sends in both type and actionid vs just actionid
        """
        getResults()
        * Pass nothing - returns a list of all Results objects
        * Pass a list of ResultID - returns a single Results object
        * Pass an ActionID - returns a single Results object
        * Pass a Sampling Feature ID- returns a list of objects with that Sampling Feature ID
        * Pass a Variable ID - returns a list of results with that Variable ID
        * Pass a Simulation ID - return a list of results that were generated by that simulation
        * Pass a Site ID - return a list of results from that site location, through the related features table.
        """

        query = self._session.query(Results)


        if type: query = query.filter_by(ResultTypeCV=type)
        if variableid: query = query.filter_by(VariableID=variableid)
        if ids: query = query.filter(Results.ResultID.in_(ids))
        if uuids: query = query.filter(Results.ResultUUID.in_(uuids))
        if simulationid: query = query.join(FeatureActions)\
            .join(Actions)\
            .join(Simulations)\
            .filter_by(SimulationID=simulationid)
        if actionid: query = query.join(FeatureActions).filter_by(ActionID=actionid)
        if sfid: query = query.join(FeatureActions).filter_by(SamplingFeatureID=sfid)

        if siteid:
            sfids = [x[0] for x in self._session.query(distinct(SamplingFeatures.SamplingFeatureID))
                                                    .select_from(RelatedFeatures)
                                                    .join(RelatedFeatures.SamplingFeatureObj)
                                                    .filter(RelatedFeatures.RelatedFeatureID == siteid)
                                                    #.filter(RelatedFeatures.RelationshipTypeCV == "Was Collected at")
                                                    .all()]
            query = query.join(FeatureActions).filter(SamplingFeatures.SamplingFeatureID.in_(sfids))

        try:
            return query.all()
        except Exception as e:
            print("Error running Query: %s" % e)
            return None


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

    def getResultValues(self, resultids, starttime=None, endtime=None):

        """Select all on TimeSeriesResults
        getResultValues()
        * Pass in a list of ResultID - Returns a pandas dataframe object of type that is specific to the result type -
                The resultids must be associated with the same value type
        * Pass a ResultID and a date range - returns a pandas dataframe object of type that is specific to the result type with values between the input date range
        """

        type= self._session.query(Results).filter_by(ResultID=resultids[0]).first().ResultTypeCV
        ResultType = TimeSeriesResults
        if "categorical" in type.lower():ResultType = CategoricalResultValues
        elif "measurement" in type.lower():ResultType = MeasurementResultValues
        elif "point" in type.lower():ResultType = PointCoverageResultValues
        elif "profile" in type.lower():ResultType = ProfileResultValues
        elif "section" in type.lower():ResultType = SectionResults
        elif "spectra" in type.lower():ResultType = SpectraResultValues
        elif "time" in type.lower():ResultType = TimeSeriesResultValues
        elif "trajectory" in type.lower():ResultType = TrajectoryResultValues
        elif "transect" in type.lower():ResultType = TransectResultValues

        # q.filter(Affiliations.AffiliationID.in_(ids))

        q = self._session.query(ResultType).filter(ResultType.ResultID.in_(resultids))
        if starttime: q = q.filter(ResultType.ValueDateTime >= starttime)
        if endtime: q = q.filter(ResultType.ValueDateTime <= endtime)
        try:
            vals = q.order_by(ResultType.ValueDateTime)
            # df = pd.DataFrame([dv.list_repr() for dv in vals.all()])
            # df.columns = vals[0].get_columns()

            query = q.statement.compile(dialect=self._session_factory.engine.dialect)
            df = pd.read_sql_query(sql=query,
                                     con=self._session_factory.engine,
                                     params=query.params)
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
        * Pass nothing - get a list of all converter simuation objects
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
        * Pass a ModelID - get a list of converter objects related to the converter having ModelID
        * Pass a ModelCode - get a list of converter objects related to the converter having ModeCode
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


