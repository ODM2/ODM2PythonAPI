from __future__ import (absolute_import, division, print_function)

from odm2api.ODM2 import serviceBase
from odm2api.ODM2.models import (
    ActionAnnotations, ActionDirectives, ActionExtensionPropertyValues, Actions,
    Affiliations, Annotations, AuthorLists, CVActionType, CVAggregationStatistic,
    CVAnnotationType, CVCensorCode, CVDataQualityType, CVDataSetType, CVDirectiveType,
    CVElevationDatum, CVEquipmentType, CVMediumType, CVMethodType, CVOrganizationType,
    CVPropertyDataType, CVQualityCode, CVRelationshipType, CVResultType, CVSamplingFeatureGeoType,
    CVSamplingFeatureType, CVSiteType, CVSpatialOffsetType, CVSpeciation, CVSpecimenType,
    CVStatus, CVTaxonomicClassifierType, CVUnitsType, CVVariableName, CVVariableType,
    CalibrationActions, CalibrationReferenceEquipment, CalibrationStandards,
    CategoricalResultValueAnnotations, CategoricalResultValues, CitationExtensionPropertyValues,
    CitationExternalIdentifiers, DataLoggerFileColumns, DataLoggerFiles, DataLoggerProgramFiles,
    DataQuality, DataSetCitations, DataSets, DataSetsResults, DerivationEquations, Directives, Equipment,
    EquipmentActions, EquipmentAnnotations, EquipmentModels, EquipmentUsed, ExtensionProperties,
    ExternalIdentifierSystems, FeatureActions, InstrumentOutputVariables, MaintenanceActions,
    MeasurementResultValueAnnotations, MeasurementResultValues, MethodAnnotations,
    MethodCitations, MethodExtensionPropertyValues, MethodExternalIdentifiers,
    Methods, Models, Organizations, People, PersonExternalIdentifiers,
    PointCoverageResultValueAnnotations, PointCoverageResultValues, ProcessingLevels,
    ProfileResultValueAnnotations, ProfileResultValues, ReferenceMaterialExternalIdentifiers,
    ReferenceMaterialValues, ReferenceMaterials, RelatedActions, RelatedAnnotations,
    RelatedCitations, RelatedDataSets, RelatedEquipment, RelatedFeatures, RelatedModels,
    RelatedResults, ResultAnnotations, ResultDerivationEquations, ResultExtensionPropertyValues,
    ResultNormalizationValues, Results, ResultsDataQuality, SamplingFeatureAnnotations,
    SamplingFeatureExtensionPropertyValues, SamplingFeatureExternalIdentifiers,
    SamplingFeatures, SectionResultValueAnnotations, SectionResults, Simulations,
    SpatialReferenceExternalIdentifiers, SpatialReferences, SpecimenBatchPositions,
    SpectraResultValueAnnotations, SpectraResultValues, TaxonomicClassifierExternalIdentifiers,
    TaxonomicClassifiers, TimeSeriesResultValueAnnotations, TimeSeriesResultValues,
    TimeSeriesResults, TrajectoryResultValueAnnotations, TrajectoryResultValues,
    TransectResultValueAnnotations, TransectResultValues, Units, VariableExtensionPropertyValues,
    VariableExternalIdentifiers, Variables,
)

import pandas as pd

from sqlalchemy import distinct, exists

__author__ = 'sreeder'


class DetailedResult:
    def __init__(self, action, result,
                 sc, sn,
                 method, variable,
                 processingLevel,
                 unit):
        # result.result_id etc.
        self.ResultID = result.ResultID
        self.SamplingFeatureCode = sc
        self.MethodCode = method.MethodCode
        self.VariableCode = variable.VariableCode
        self.ProcessingLevelCode = processingLevel.ProcessingLevelCode
        self.UnitsName = unit.UnitsName

        self.SamplingFeatureName = sn
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
        self.Name = person.PersonFirstName + ' ' + person.PersonLastName
        self.Organization = '(' + org.OrganizationCode + ') ' + org.OrganizationName


class SamplingFeatureDataSet():
    datasets={}
    related_features={}
    def __init__(self, samplingfeature, datasetresults, relatedfeatures):
        sf = samplingfeature

        self.SamplingFeature = sf
        self.SamplingFeatureID = sf.SamplingFeatureID
        self.SamplingFeatureUUID = sf.SamplingFeatureUUID
        self.SamplingFeatureTypeCV = sf.SamplingFeatureTypeCV
        self.SamplingFeatureCode = sf.SamplingFeatureCode
        self.SamplingFeatureName = sf.SamplingFeatureName
        self.SamplingFeatureDescription = sf.SamplingFeatureDescription
        self.SamplingFeatureGeotypeCV = sf.SamplingFeatureGeotypeCV
        self.Elevation_m = sf.Elevation_m
        self.ElevationDatumCV = sf.ElevationDatumCV
        self.FeatureGeometryWKT = sf.FeatureGeometryWKT
        self.assignDatasets(datasetresults)
        self.assignRelatedFeatures(relatedfeatures)


        print(self.datasets)

    def assignDatasets(self, datasetresults):
        self.datasets = {}
        for dsr in datasetresults:
            if dsr.DataSetObj not in self.datasets:
                #if the dataset is not in the dictionary, add it and the first result
                self.datasets[dsr.DataSetObj]=[]
                res = dsr.ResultObj
                # res.FeatureActionObj = None
                self.datasets[dsr.DataSetObj].append(res)
            else:
                #if the dataset is in the dictionary, append the result object to the list
                res = dsr.ResultObj
                # res.FeatureActionObj = None
                self.datasets[dsr.DataSetObj].append(res)


    def assignRelatedFeatures(self, relatedfeatures):
        self.related_features = {}
        for related in relatedfeatures:
            if related.SamplingFeatureTypeCV == 'Site':
                self.related_features = related





class ReadODM2(serviceBase):
    # Exists functions
    def resultExists(self, result):
        """
        Check to see if a Result Object exists
        * Pass Result Object - return a boolean value of wether the given object exists

        """
        try:

            ret = self._session.query(exists().where(Results.ResultTypeCV == result.ResultTypeCV)
                                      .where(Results.VariableID == result.VariableID)
                                      .where(Results.UnitsID == result.UnitsID)
                                      .where(Results.ProcessingLevelID == result.ProcessingLevelID)
                                      .where(Results.SampledMediumCV == result.SampledMediumCV)
                                      )
            return ret.scalar()

        except:
            return None

    # Annotations
    def getAnnotations(self, type=None, codes=None, ids=None):
        """
        * Pass Nothing - return a list of all objects
        * Pass AnnotationTypeCV - return a list of all objects of the fiven type
        * Pass a list of codes - return a list of objects, one for each of the given codes
        * Pass a list of ids -return a list of objects, one for each of the given ids

        """
        # TODO What keywords do I use for type.
        a = Annotations
        if type:
            if type == 'action':
                a = ActionAnnotations
            elif type == 'categoricalresultvalue':
                a = CategoricalResultValueAnnotations
            elif type == 'equipmentannotation':
                a = EquipmentAnnotations
            elif type == 'measurementresultvalue':
                a = MeasurementResultValueAnnotations
            elif type == 'method':
                a = MethodAnnotations
            elif type == 'pointcoverageresultvalue':
                a = PointCoverageResultValueAnnotations
            elif type == 'profileresultvalue':
                a = ProfileResultValueAnnotations
            elif type == 'result':
                a = ResultAnnotations
            elif type == 'samplingfeature':
                a = SamplingFeatureAnnotations
            elif type == 'sectionresultvalue':
                a = SectionResultValueAnnotations
            elif type == 'spectraresultvalue':
                a = SpectraResultValueAnnotations
            elif type == 'timeseriesresultvalue':
                a = TimeSeriesResultValueAnnotations
            elif type == 'trajectoryresultvalue':
                a = TrajectoryResultValueAnnotations
            elif type == 'transectresultvalue':
                a = TransectResultValueAnnotations
        try:
            query = self._session.query(a)
            if codes:
                query = query.filter(Annotations.AnnotationCode.in_(codes))
            if ids:
                query = query.filter(Annotations.AnnotationID.in_(ids))
            return query.all()

        except:
            return None

    # CV
    def getCVs(self, type):
        """
        getCVs(self, type):
        * Pass CVType - return a list of all objects of the given type

        """
        CV = CVActionType
        if type == 'actiontype':
            CV = CVActionType
        elif type == 'aggregationstatistic':
            CV = CVAggregationStatistic
        elif type == 'annotationtype':
            CV = CVAnnotationType
        elif type == 'censorcode':
            CV = CVCensorCode
        elif type == 'dataqualitytype':
            CV = CVDataQualityType
        elif type == 'dataset type':
            CV = CVDataSetType
        elif type == 'Directive Type':
            CV = CVDirectiveType
        elif type == 'Elevation Datum':
            CV = CVElevationDatum
        elif type == 'Equipment Type':
            CV = CVEquipmentType
        elif type == 'Medium':
            CV = CVMediumType
        elif type == 'Method Type':
            CV = CVMethodType
        elif type == 'Organization Type':
            CV = CVOrganizationType
        elif type == 'Property Data Type':
            CV = CVPropertyDataType
        elif type == 'Quality Code':
            CV = CVQualityCode
        elif type == 'Relationship Type':
            CV = CVRelationshipType
        elif type == 'Result Type':
            CV = CVResultType
        elif type == 'Sampling Feature Geo-type':
            CV = CVSamplingFeatureGeoType
        elif type == 'Sampling Feature Type':
            CV = CVSamplingFeatureType
        elif type == 'Site Type':
            CV = CVSiteType
        elif type == 'Spatial Offset Type':
            CV = CVSpatialOffsetType
        elif type == 'Speciation':
            CV = CVSpeciation
        elif type == 'Specimen Type':
            CV = CVSpecimenType
        elif type == 'Status':
            CV = CVStatus
        elif type == 'Taxonomic Classifier Type':
            CV = CVTaxonomicClassifierType
        elif type == 'Units Type':
            CV = CVUnitsType
        elif type == 'Variable Name':
            CV = CVVariableName
        elif type == 'Variable Type':
            CV = CVVariableType
        else:
            return None
        try:
            return self._session.query(CV).all()
        except Exception as e:
            print('Error running Query: {}'.format(e))

    # Core
    def getDetailedAffiliationInfo(self):
        """
        * Pass Nothing - Return a list of all Affiliations with detailed information,
        including Affiliation, People and Organization

        """
        q = self._session.query(Affiliations, People, Organizations) \
            .filter(Affiliations.PersonID == People.PersonID) \
            .filter(Affiliations.OrganizationID == Organizations.OrganizationID)
        affiliationList = []
        for a, p, o in q.all():
            detailedAffiliation = DetailedAffiliation(a, p, o)
            affiliationList.append(detailedAffiliation)
        return affiliationList

    def getDetailedResultInfo(self, resultTypeCV=None, resultID=None, sfID=None):
        # TODO can this be done by just getting the result object and drilling down?
        # What is the performance comparison.
        """
        Get detailed information for all selected Results including , unit info, site info,
        method info , ProcessingLevel info.
        * Pass nothing - return a list of all objects
        * Pass resultTypeCV - All objects of given type
        * Pass a result ID - single object with the given result ID
        * Pass a SamplingFeatureID - All objects associated with the given sampling feature.

        """
        q = self._session.query(
            Actions,
            Results,
            SamplingFeatures.SamplingFeatureCode,
            SamplingFeatures.SamplingFeatureName,
            Methods,
            Variables,
            ProcessingLevels,
            Units).filter(Results.VariableID == Variables.VariableID) \
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
            q = q.filter(Results.ResultID == resultID)

        for a, r, sc, sn, m, v, p, u in q.all():
            detailedResult = DetailedResult(
                a, r, sc, sn, m, v, p, u
            )
            resultList.append(detailedResult)
        return resultList

    # Taxonomic Classifiers
    def getTaxonomicClassifiers(self):
        """
        getTaxonomicClassifiers(self):
        * Pass nothing - return a list of all objects

        """
        return self._session.query(TaxonomicClassifiers).all()

    # Variable
    def getVariables(self, ids=None, codes=None, sitecode=None, results=False):
        """
        * Pass nothing - returns full list of variable objects
        * Pass a list of VariableID - returns a single variable object
        * Pass a list of VariableCode - returns a single variable object
        * Pass a SiteCode - returns a list of Variable objects that are collected at the given site.
        * Pass whether or not you want to return the sampling features that have results associated with them

        """
        if sitecode:
            try:
                variables = [
                    x[0] for x in
                    self._session.query(distinct(Results.VariableID))
                    .filter(Results.FeatureActionID == FeatureActions.FeatureActionID)
                    .filter(FeatureActions.SamplingFeatureID == SamplingFeatures.SamplingFeatureID)
                    .filter(SamplingFeatures.SamplingFeatureCode == sitecode).all()
                ]
                if ids:
                    ids = list(set(ids).intersection(variables))
                else:
                    ids = variables
            except:
                pass

        if results:
            try:
                variables = [x[0] for x in self._session.query(distinct(Results.VariableID)).all()]
                if ids:
                    ids = list(set(ids).intersection(variables))
                else:
                    ids = variables
            except:
                pass

        query = self._session.query(Variables)
        if ids:
            query = query.filter(Variables.VariableID.in_(ids))
        if codes:
            query = query.filter(Variables.VariableCode.in_(codes))
        try:
            return query.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Method
    def getMethods(self, ids=None, codes=None, type=None):
        """
        * Pass nothing - returns full list of method objects
        * Pass a list of MethodIDs - returns a single method object for each given id
        * Pass a list of MethodCode - returns a single method object for each given code
        * Pass a MethodType - returns a list of method objects of the given MethodType

        """
        q = self._session.query(Methods)
        if ids:
            q = q.filter(Methods.MethodID.in_(ids))
        if codes:
            q = q.filter(Methods.MethodCode.in_(codes))
        if type:
            q = q.filter_by(MethodTypeCV=type)

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # ProcessingLevel
    def getProcessingLevels(self, ids=None, codes=None):
        """
        getProcessingLevels(self, ids=None, codes=None)
        * Pass nothing - returns full list of ProcessingLevel objects
        * Pass a list of ProcessingLevelID - returns a single processingLevel object for each given id
        * Pass a list of ProcessingLevelCode - returns a single processingLevel object for each given code

        """
        q = self._session.query(ProcessingLevels)
        if ids:
            q = q.filter(ProcessingLevels.ProcessingLevelsID.in_(ids))
        if codes:
            q = q.filter(ProcessingLevels.ProcessingLevelCode.in_(codes))

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Sampling Feature
    def getSamplingFeatures(self, ids=None, codes=None, uuids=None, type=None, wkt=None, results=False):
        """Retrieve a list of Sampling Feature objects.

        If no arguments are passed to the function, or their values are None,
        all Sampling Feature objects in the database will be returned.

        Args:
            ids (list, optional): List of SamplingFeatureIDs.
            codes (list, optional): List of SamplingFeature Codes.
            uuids (list, optional): List of UUIDs string.
            type (str, optional): Type of Sampling Feature from
                `controlled vocabulary name <http://vocabulary.odm2.org/samplingfeaturetype/>`_.
            wkt (str, optional): SamplingFeature Well Known Text.
            results (bool, optional): Whether or not you want to return only the
                sampling features that have results associated with them.

        Returns:
            list: List of Sampling Feature objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getSamplingFeatures(ids=[39, 40])
            >>> READ.getSamplingFeatures(codes=['HOME', 'FIELD'])
            >>> READ.getSamplingFeatures(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getSamplingFeatures(type='Site')
            >>> READ.getSamplingFeatures(wkt='POINT (30 10)')
            >>> READ.getSamplingFeatures(results=True)
            >>> READ.getSamplingFeatures(type='Site', results=True)

        """
        if results:
            try:
                fas = [x[0] for x in self._session.query(distinct(Results.FeatureActionID)).all()]
            except:
                return None
            sf = [x[0] for x in self._session.query(distinct(FeatureActions.SamplingFeatureID))
                                    .filter(FeatureActions.FeatureActionID.in_(fas)).all()]
            if ids:
                ids = list(set(ids).intersection(sf))
            else:
                ids = sf

        q = self._session.query(SamplingFeatures)

        if type:
            q = q.filter_by(SamplingFeatureTypeCV=type)
        if ids:
            q = q.filter(SamplingFeatures.SamplingFeatureID.in_(ids))
        if codes:
            q = q.filter(SamplingFeatures.SamplingFeatureCode.in_(codes))
        if uuids:
            q = q.filter(SamplingFeatures.SamplingFeatureUUID.in_(uuids))
        if wkt:
            q = q.filter_by(FeatureGeometryWKT=wkt)
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    def getRelatedSamplingFeatures(self, sfid=None, rfid=None, relationshiptype=None):
        # TODO: add functionality to filter by code
        """
        * Pass a SamplingFeatureID - get a list of sampling feature objects
          related to the input sampling feature
        * Pass a RelatedFeatureID - get a list of Sampling features objects through the related feature
        * Pass a RelationshipTypeCV - get a list of sampling feature objects with the given type

        """

        sf = self._session.query(distinct(SamplingFeatures.SamplingFeatureID))\
                 .select_from(RelatedFeatures)

        if sfid:
            sf = sf.join(RelatedFeatures.RelatedFeatureObj).filter(RelatedFeatures.SamplingFeatureID == sfid)
        if rfid:
            sf = sf.join(RelatedFeatures.SamplingFeatureObj).filter(RelatedFeatures.RelatedFeatureID == rfid)
        if relationshiptype:
            sf = sf.filter(RelatedFeatures.RelationshipTypeCV == relationshiptype)
        try:
            sfids = [x[0] for x in sf.all()]
            if len(sfids) > 0:
                sflist = self.getSamplingFeatures(ids=sfids)
                return sflist

        except Exception as e:
            print('Error running Query: {}'.format(e))
        return None



    # Action
    def getActions(self, ids=None, type=None, sfid=None):
        """
        * Pass nothing - returns a list of all Actions
        * Pass a list of Action ids - returns a list of Action objects
        * Pass a ActionTypeCV - returns a list of Action objects of that type
        * Pass a SamplingFeature ID - returns a list of Action objects
          associated with that Sampling feature ID, Found through featureAction table

        """
        a = Actions
        if type == 'equipment':
            a = EquipmentActions
        elif type == 'calibration':
            a = CalibrationActions
        elif type == 'maintenance':
            a = MaintenanceActions

        q = self._session.query(a)
        if ids:
            q = q.filter(a.ActionID.in_(ids))
        if sfid:
            q = q.join(FeatureActions).filter(FeatureActions.SamplingFeatureID == sfid)

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    def getRelatedActions(self, actionid=None):
        """
        * Pass an ActionID - get a list of Action objects related to the input
          action along with the relationship type

        """

        q = self._session.query(Actions).select_from(RelatedActions).join(RelatedActions.RelatedActionObj)
        if actionid:
            q = q.filter(RelatedActions.ActionID == actionid)
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Unit
    def getUnits(self, ids=None, name=None, type=None):
        """
        * Pass nothing - returns a list of all units objects
        * Pass a list of UnitsID - returns a single units object for the given id
        * Pass UnitsName - returns a single units object
        * Pass a type- returns a list of all objects of the given type

        """
        q = self._session.query(Units)
        if ids:
            q = q.filter(Units.UnitsID.in_(ids))
        if name:
            q = q.filter(Units.UnitsName.ilike(name))
        if type:
            q = q.filter(Units.UnitsTypeCV.ilike(type))
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None


    # Organization
    def getOrganizations(self, ids=None, codes=None):
        """
        * Pass nothing - returns a list of all organization objects
        * Pass a list of OrganizationID - returns a single organization object
        * Pass a list of OrganizationCode - returns a single organization object

        """
        q = self._session.query(Organizations)
        if ids:
            q = q.filter(Organizations.OrganizationID.in_(ids))
        if codes:
            q = q.filter(Organizations.OrganizationCode.in_(codes))
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Person
    def getPeople(self, ids=None, firstname=None, lastname=None):
        """
        * Pass nothing - returns a list of all People objects
        * Pass a list of PeopleID - returns a single People object
        * Pass a First Name - returns a single People object
        * Pass a Last Name - returns a single People object

        """
        q = self._session.query(People)
        if ids:
            q = q.filter(People.PersonID.in_(ids))
        if firstname:
            q = q.filter(People.PersonFirstName.ilike(firstname))
        if lastname:
            q = q.filter(People.PersonLastName.ilike(lastname))
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    def getAffiliations(self, ids=None, personfirst=None, personlast=None, orgcode=None):
        """Retrieve a list of Affiliation objects.

        If no arguments are passed to the function, or their values are None,
        all Affiliation objects in the database will be returned.

        Args:
            ids (list, optional): List of AffiliationIDs.
            personfirst (str, optional): Person First Name.
            personlast (str, optional): Person Last Name.
            orgcode (str, optional): Organization Code.

        Returns:
            list: List of Affiliation objects

        Examples:
            >>> ReadODM2.getAffiliations(ids=[39,40])
            >>> ReadODM2.getAffiliations(personfirst='John',
            ...                      personlast='Smith')
            >>> ReadODM2.getAffiliations(orgcode='Acme')

        """
        q = self._session.query(Affiliations)

        if ids:
            q = q.filter(Affiliations.AffiliationID.in_(ids))
        if orgcode:
            q = q.join(Affiliations.OrganizationObj).filter(Organizations.OrganizationCode.ilike(orgcode))
        if personfirst:
            q = q.join(Affiliations.PersonObj).filter(People.PersonFirstName.ilike(personfirst))
        if personlast:
            q = q.join(Affiliations.PersonObj).filter(People.PersonLastName.ilike(personlast))

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Results
    def getResults(self, ids=None, type=None, restype = None, uuids=None, actionid=None, simulationid=None, sfid=None,
                   variableid=None, siteid=None, sfids=None, sfuuids=None, sfcodes=None):

        # TODO what if user sends in both type and actionid vs just actionid
        """Retrieve a list of Result objects.

        If no arguments are passed to the function, or their values are None,
        all Result objects in the database will be returned.

        Args:
            ids (list, optional): List of ResultIDs.
            restype (str, optional): Type of Result from
                `controlled vocabulary name <http://vocabulary.odm2.org/resulttype/>`_.
            uuids (list, optional): List of UUIDs string.
            actionid (int, optional): ActionID.
            simulationid (int, optional): SimulationID.
            sfid (int, optional): SamplingFeatureID.
            variableid (int, optional): VariableID.
            siteid (int, optional): SiteID. - goes through related features table and finds all of results
                    recorded at the given site
            sfids(list, optional): List of Sampling Feature IDs integer.
            sfuuids(list, optional): List of Sampling Feature UUIDs string.
            sfcodes=(list, optional): List of Sampling Feature codes string.

        Returns:
            list: List of Result objects

        Examples:
            >>> ReadODM2.getResults(ids=[39,40])
            >>> ReadODM2.getResults(restype='Time series coverage')
            >>> ReadODM2.getResults(sfids=[65])
            >>> ReadODM2.getResults(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                            '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> ReadODM2.getResults(simulationid=50)
            >>> ReadODM2.getResults(siteid=6)
            >>> ReadODM2.getResults(variableid=7)
            >>> ReadODM2.getResults(actionid=20)

        """
        query = self._session.query(Results)

        if type:
            import warnings
            warnings.warn(
                "The parameter 'type' is no longer be supported. Please use the restype parameter instead.")
            query = query.filter_by(ResultTypeCV=type)
        if restype:
            query = query.filter_by(ResultTypeCV=restype)
        if variableid:
            query = query.filter_by(VariableID=variableid)
        if ids:
            query = query.filter(Results.ResultID.in_(ids))
        if uuids:
            query = query.filter(Results.ResultUUID.in_(uuids))
        if simulationid:
            query = query.join(FeatureActions)\
                    .join(Actions)\
                    .join(Simulations)\
                    .filter_by(SimulationID=simulationid)
        if actionid:
            query = query.join(FeatureActions).filter_by(ActionID=actionid)
        if sfid:
            import warnings
            warnings.warn("The parameter 'sfid' is no longer be supported. Please use the sfids parameter and send in a list.")
            query = query.join(FeatureActions).filter_by(SamplingFeatureID=sfid)
        if sfids or sfcodes or sfuuids:
            sf_list = self.getSamplingFeatures(ids=sfids, codes=sfcodes, uuids=sfuuids)
            sfids = []
            for sf in sf_list:
                sfids.append(sf.SamplingFeatureID)
            query = query.join(FeatureActions).filter(FeatureActions.SamplingFeatureID.in_(sfids))

        if siteid:

            sfids = [x[0] for x in self._session.query(
                distinct(SamplingFeatures.SamplingFeatureID))
                .select_from(RelatedFeatures)
                .join(RelatedFeatures.SamplingFeatureObj)
                .filter(RelatedFeatures.RelatedFeatureID == siteid)
                .all()
            ]

            #TODO does this code do the same thing as the code above?
            # sf_list = self.getRelatedSamplingFeatures(rfid=siteid)
            # sfids = []
            # for sf in sf_list:
            #     sfids.append(sf.SamplingFeatureID)

            query = query.join(FeatureActions).filter(FeatureActions.SamplingFeatureID.in_(sfids))

        try:
            return query.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Datasets
    def getDataSets(self, ids= None, codes=None, uuids=None, dstype=None):
        """
        Retrieve a list of Datasets

        Args:
            ids (list, optional): List of DataSetsIDs.
            codes (list, optional): List of DataSet Codes.
            uuids (list, optional): List of Dataset UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.


        Returns:
            list: List of DataSets Objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getDataSets(ids=[39, 40])
            >>> READ.getDataSets(codes=['HOME', 'FIELD'])
            >>> READ.getDataSets(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getDataSets(dstype='singleTimeSeries')

        """
        q = self._session.query(DataSets)
        if ids:
            q = q.filter(DataSets.DataSetID.in_(ids))
        if codes:
            q = q.filter(DataSets.DataSetCode.in_(codes))
        if uuids:
            q.filter(DataSets.DataSetUUID.in_(uuids))
        if dstype:
            q = q.filter(DataSets.DataSetTypeCV == dstype)
        try:
            return q.all()
        except Exception as e:
            print('Error running Query {}'.format(e))
            return None

            # Datasets

    def getDataSetsResults(self, ids=None, codes=None, uuids=None, dstype=None):
        """
        Retrieve a detailed list of Datasets along with detailed metadata about the datasets
                and the results contained within them

        **Must specify either DataSetID OR DataSetUUID OR DataSetCode)**
        Args:
            ids (list, optional): List of DataSetsIDs.
            codes (list, optional): List of DataSet Codes.
            uuids (list, optional): List of Dataset UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.


        Returns:
            list: List of DataSetsResults Objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getDataSetsResults(ids=[39, 40])
            >>> READ.getDataSetsResults(codes=['HOME', 'FIELD'])
            >>> READ.getDataSetsResults(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getDataSetsResults(dstype='singleTimeSeries')

        """

        # make sure one of the three arguments has been sent in
        if all(v is None for v in [ids, codes, uuids]):
            raise ValueError('Expected DataSetID OR DataSetUUID OR DataSetCode argument')

        q = self._session.query(DataSetsResults)\
            .join(DataSets)
        if ids:
            q = q.filter(DataSets.DataSetID.in_(ids))
        if codes:
            q = q.filter(DataSets.DataSetCode.in_(codes))
        if uuids:
            q.filter(DataSets.DataSetUUID.in_(uuids))
        if dstype:
            q = q.filter(DataSets.DataSetTypeCV == dstype)
        try:
            return q.all()
        except Exception as e:
            print('Error running Query {}'.format(e))
        return None

    def getDataSetsValues(self, ids=None, codes=None, uuids=None, dstype=None):
        """
        Retrieve a list of datavalues associated with the given dataset info

        **Must specify either DataSetID OR DataSetUUID OR DataSetCode)**
        Args:
            ids (list, optional): List of DataSetsIDs.
            codes (list, optional): List of DataSet Codes.
            uuids (list, optional): List of Dataset UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.


        Returns:
            list: List of Result Values Objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getDataSetsValues(ids=[39, 40])
            >>> READ.getDataSetsValues(codes=['HOME', 'FIELD'])
            >>> READ.getDataSetsValues(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getDataSetsValues(dstype='singleTimeSeries')

        """

        dsr = self.getDataSetsResults(ids, codes, uuids, dstype)

        resids = []
        for ds in dsr:
            resids.append(ds.ResultID)

        try:
            return self.getResultValues(resultids = resids)
        except Exception as e:
            print('Error running Query {}'.format(e))
        return None


    def getSamplingFeatureDatasets(self, ids=None, codes=None, uuids=None, dstype=None, type=None):
        """
        Retrieve a list of Datasets associated with the given sampling feature data.

            **Must specify either samplingFeatureID OR samplingFeatureUUID OR samplingFeatureCode)**

        Args:
            ids (list, optional): List of SamplingFeatureIDs.
            codes (list, optional): List of SamplingFeature Codes.
            uuids (list, optional): List of UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.


        Returns:
            list: List of DataSetsResults Objects associated with the given sampling feature

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getSamplingFeatureDatasets(ids=[39, 40])
            >>> READ.getSamplingFeatureDatasets(codes=['HOME', 'FIELD'])
            >>> READ.getSamplingFeatureDatasets(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getSamplingFeatureDatasets(dstype='singleTimeSeries')

        """


        # make sure one of the three arguments has been sent in
        # if all(v is None for v in [ids, codes, uuids, type]):
        #     raise ValueError('Expected samplingFeatureID OR samplingFeatureUUID OR samplingFeatureCode OR samplingFeatureType '
        #                      'argument')

        sf_query = self._session.query(SamplingFeatures)
        if type:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureTypeCV == type)
        if ids:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureID.in_(ids))
        if codes:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureCode.in_(codes))
        if uuids:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureUUID.in_(uuids))

        sf_list = []
        for sf in sf_query.all():
            sf_list.append(sf)

        sfds = None
        try:
            sfds=[]
            for sf in sf_list:

                q = self._session.query(DataSetsResults)\
                    .join(Results)\
                    .join(FeatureActions)\
                    .filter(FeatureActions.SamplingFeatureID == sf.SamplingFeatureID)

                if dstype:
                    q = q.filter_by(DatasetTypeCV=dstype)


                vals = q.all()

                related = self.getRelatedSamplingFeatures(sf.SamplingFeatureID)

                sfds.append(SamplingFeatureDataSet(sf, vals, related))
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None
        return sfds

    # Data Quality
    def getDataQuality(self):
        """
        * Pass nothing - return a list of all objects
        """
        return self._session.query(DataQuality).all()

    # TODO DataQuality Schema Queries
    def getReferenceMaterials(self):
        """
        * Pass nothing - return a list of all objects
        """
        return self._session.query(ReferenceMaterials).all()

    def getReferenceMaterialValues(self):
        """
        * Pass nothing - return a list of all objects
        """
        return self._session.query(ReferenceMaterialValues).all()

    def getResultNormalizationValues(self):
        """
        * Pass nothing - return a list of all objects
        """
        return self._session.query(ResultNormalizationValues).all()

    def getResultsDataQuality(self):
        """
        * Pass nothing - return a list of all objects
        """
        return self._session.query(ResultsDataQuality).all()

    # TODO Equipment Schema Queries
    # Equipment
    def getEquipment(self, codes=None, type=None, sfid=None, actionid=None):
        """
        * Pass nothing - returns a list of all Equipment objects
        * Pass a list of EquipmentCodes- return a list of all Equipment objects that match each of the codes
        * Pass a EquipmentType - returns a single Equipment object
        * Pass a SamplingFeatureID - returns a single Equipment object
        * Pass an ActionID - returns a single Equipment object

        """
        e = self._session.query(Equipment)
        if sfid:
            e = e.join(EquipmentUsed) \
                    .join(Actions) \
                    .join(FeatureActions) \
                    .filter(FeatureActions.SamplingFeatureID == sfid)
        if codes:
            e = e.filter(Equipment.EquipmentCode.in_(codes))
        if actionid:
            e = e.join(EquipmentUsed).join(Actions) \
                    .filter(Actions.ActionID == actionid)
        return e.all()

    def CalibrationReferenceEquipment(self):
        """
        * Pass nothing - return a list of all objects

        """
        return self._session.query(CalibrationReferenceEquipment).all()

    def CalibrationStandards(self):
        """
        * Pass nothing - return a list of all objects

        """
        return self._session.query(CalibrationStandards).all()

    def DataloggerFileColumns(self):
        """
        * Pass nothing - return a list of all objects

        """
        return self._session.query(DataLoggerFileColumns).all()

    def DataLoggerFiles(self):
        """
        * Pass nothing - return a list of all objects

        """
        return self._session.query(DataLoggerFiles).all()

    def DataloggerProgramFiles(self):
        """
        * Pass Nothing - return a list of all objects

        """
        return self._session.query(DataLoggerProgramFiles).all()

    def EquipmentModels(self):
        """
        * Pass Nothing - return a list of all objects

        """
        return self._session.query(EquipmentModels).all()

    def EquipmentUsed(self):
        """
        * Pass Nothing - return a list of all objects

        """
        return self._session.query(EquipmentUsed).all()

    def InstrumentOutputVariables(self, modelid=None, variableid=None):
        """
        * Pass Nothing - return a list of all objects
        * Pass ModelID
        * Pass VariableID

        """
        i = self._session.query(InstrumentOutputVariables)
        if modelid:
            i = i.filter_by(ModelID=modelid)
        if variableid:
            i = i.filter_by(VariableID=variableid)
        return i.all()

    def RelatedEquipment(self, code=None):
        """
        * Pass nothing - return a list of all objects
        * Pass code- return a single object with the given code

        """
        r = self._session.query(RelatedEquipment)
        if code:
            r = r.filter_by(EquipmentCode=code)
        return r.all()

    # Extension Properties
    def getExtensionProperties(self, type=None):
        """
        * Pass nothing - return a list of all objects
        * Pass type- return a list of all objects of the given type

        """
        # Todo what values to use for extensionproperties type
        e = ExtensionProperties
        if type == 'action':
            e = ActionExtensionPropertyValues
        elif type == 'citation':
            e = CitationExtensionPropertyValues
        elif type == 'method':
            e = MethodExtensionPropertyValues
        elif type == 'result':
            e = ResultExtensionPropertyValues
        elif type == 'samplingfeature':
            e = SamplingFeatureExtensionPropertyValues
        elif type == 'variable':
            e = VariableExtensionPropertyValues
        try:
            return self._session.query(e).all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # External Identifiers
    def getExternalIdentifiers(self, type=None):
        """
        * Pass nothing - return a list of all objects
        * Pass type- return a list of all objects of the given type

        """
        e = ExternalIdentifierSystems
        if type.lowercase == 'citation':
            e = CitationExternalIdentifiers
        elif type == 'method':
            e = MethodExternalIdentifiers
        elif type == 'person':
            e = PersonExternalIdentifiers
        elif type == 'referencematerial':
            e = ReferenceMaterialExternalIdentifiers
        elif type == 'samplingfeature':
            e = SamplingFeatureExternalIdentifiers
        elif type == 'spatialreference':
            e = SpatialReferenceExternalIdentifiers
        elif type == 'taxonomicclassifier':
            e = TaxonomicClassifierExternalIdentifiers
        elif type == 'variable':
            e = VariableExternalIdentifiers
        try:
            return self._session.query(e).all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # TODO functions for Lab Analyses
    # Lab Analyses
    def getDirectives(self):
        """
        getDirectives(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(Directives).all()

    def getActionDirectives(self):
        """
        getActionDirectives(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(ActionDirectives).all()

    def getSpecimenBatchPositions(self):
        """
        getSpecimenBatchPositions(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(SpecimenBatchPositions).all()

    # TODO functions for Provenance
    # Provenance
    def getAuthorLists(self):
        """
        getAuthorLists(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(AuthorLists).all()

    def getDatasetCitations(self):
        """
        getDatasetCitations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(DataSetCitations).all()

    def getDerivationEquations(self):
        """
        getDerivationEquations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(DerivationEquations).all()

    def getMethodCitations(self):
        """
        getMethodCitations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(MethodCitations).all()

    def getRelatedAnnotations(self):
        """
        getRelatedAnnotations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(RelatedAnnotations).all()

    def getRelatedCitations(self):
        """
        getRelatedCitations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(RelatedCitations).all()

    def getRelatedDatasets(self):
        """
        getRelatedDatasets(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(RelatedDataSets).all()

    def getRelatedResults(self):
        """
        getRelatedResults(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(RelatedResults).all()

    def getResultDerivationEquations(self):
        """
        getResultDerivationEquations(self)
        * Pass nothing - return a list of all objects

        """
        return self._session.query(ResultDerivationEquations).all()

    # Results
    # ResultValues
    def getResultValues(self, resultids, starttime=None, endtime=None):
        """
        getResultValues(self, resultids, starttime=None, endtime=None)
        * Pass in a list of ResultID - Returns a pandas dataframe object of type
          that is specific to the result type - The resultids must be associated
          with the same value type
        * Pass a ResultID and a date range - returns a pandas dataframe object
          of type that is specific to the result type with values between the input date range
        * Pass a starttime - Returns a dataframe with the values after the given start time
        * Pass an endtime - Returns a dataframe with the values before the given end time

        """
        type = self._session.query(Results).filter_by(ResultID=resultids[0]).first().ResultTypeCV
        ResultType = TimeSeriesResultValues
        if 'categorical' in type.lower():
            ResultType = CategoricalResultValues
        elif 'measurement' in type.lower():
            ResultType = MeasurementResultValues
        elif 'point' in type.lower():
            ResultType = PointCoverageResultValues
        elif 'profile' in type.lower():
            ResultType = ProfileResultValues
        elif 'section' in type.lower():
            ResultType = SectionResults
        elif 'spectra' in type.lower():
            ResultType = SpectraResultValues
        elif 'time' in type.lower():
            ResultType = TimeSeriesResultValues
        elif 'trajectory' in type.lower():
            ResultType = TrajectoryResultValues
        elif 'transect' in type.lower():
            ResultType = TransectResultValues

        q = self._session.query(ResultType).filter(ResultType.ResultID.in_(resultids))
        if starttime:
            q = q.filter(ResultType.ValueDateTime >= starttime)
        if endtime:
            q = q.filter(ResultType.ValueDateTime <= endtime)
        try:
            # F841 local variable 'vals' is assigned to but never used
            # vals = q.order_by(ResultType.ValueDateTime)
            query = q.statement.compile(dialect=self._session_factory.engine.dialect)
            df = pd.read_sql_query(
                sql=query,
                con=self._session_factory.engine,
                params=query.params
            )
            return df
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # SamplingFeatures
    # Site
    def getSpatialReferences(self, srsCodes=None):
        """
        getSpatialReferences(self, srsCodes=None)
        * Pass nothing - return a list of all Spatial References
        * Pass in a list of SRS Codes-

        """
        q = self._session.query(SpatialReferences)
        if srsCodes:
            q.filter(SpatialReferences.SRSCode.in_(srsCodes))
        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Simulation
    def getSimulations(self, name=None, actionid=None):
        """
        getSimulations(self, name=None, actionid=None)
        * Pass nothing - get a list of all converter simuation objects
        * Pass a SimulationName - get a single simulation object
        * Pass an ActionID - get a single simulation object

        """
        s = self._session.query(Simulations)
        if name:
            s = s.filter(Simulations.SimulationName.ilike(name))
        if actionid:
            s = s.filter_by(ActionID=actionid)
        try:
            return s.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    def getModels(self, codes=None):
        """
        getModels(self, codes=None)
        * Pass nothing - return a list of all Model Objects
        * Pass a list of ModelCodes - get a list of converter objects related to the converter having ModeCode

        """
        m = self._session.query(Models)
        if codes:
            m = m.filter(Models.ModelCode.in_(codes))
        try:
            return m.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    def getRelatedModels(self, id=None, code=None):
        """
        getRelatedModels(self, id=None, code=None)
        * Pass a ModelID - get a list of converter objects related to the converter having ModelID
        * Pass a ModelCode - get a list of converter objects related to the converter having ModeCode

        """
        m = self._session.query(Models).select_from(RelatedModels).join(RelatedModels.ModelObj)
        if id:
            m = m.filter(RelatedModels.ModelID == id)
        if code:
            m = m.filter(Models.ModelCode == code)

        try:
            return m.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None
