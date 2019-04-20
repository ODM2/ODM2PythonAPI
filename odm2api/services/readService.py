from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api import serviceBase
from odm2api.models import (
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
    TrajectoryResultValueAnnotations, TrajectoryResultValues,
    TransectResultValueAnnotations, TransectResultValues, Units, VariableExtensionPropertyValues,
    VariableExternalIdentifiers, Variables,
)

import pandas as pd

from sqlalchemy import distinct, exists
from sqlalchemy.orm import contains_eager

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
    datasets = {}
    related_features = {}

    def __init__(self, samplingfeature, datasetresults, relatedfeatures):
        sf = samplingfeature

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
        if datasetresults:
            for dsr in datasetresults:
                if dsr.DataSetObj not in self.datasets:
                    # if the dataset is not in the dictionary, add it and the first result
                    self.datasets[dsr.DataSetObj] = []
                    res = dsr.ResultObj
                    # res.FeatureActionObj = None
                    self.datasets[dsr.DataSetObj].append(res)
                else:
                    # if the dataset is in the dictionary, append the result object to the list
                    res = dsr.ResultObj
                    # res.FeatureActionObj = None
                    self.datasets[dsr.DataSetObj].append(res)

    def assignRelatedFeatures(self, relatedfeatures):
        self.related_features = {}
        if relatedfeatures:
            for related in relatedfeatures:
                if related.SamplingFeatureTypeCV == 'Site':
                    self.related_features = related


class ReadODM2(serviceBase):
    def _get_columns(self, model):
        """Internal helper function to get a dictionary of a model column properties.

        Args:
            model (object): Sqlalchemy object, Ex. ODM2 model.

        Returns:
            dict: Dictionary of column properties Ex. {'resultid': 'ResultID'}

        """
        from sqlalchemy.orm.properties import ColumnProperty
        columns = [(prop.key.lower(), prop.key) for prop in model.__mapper__.iterate_properties if
                   isinstance(prop, ColumnProperty)]

        return dict(columns)

    def _check_kwargs(self, args, kwargs):
        """Internal helper function to check for unused keyword arguments

        Args:
            args (list): List of expected, valid arguments.
            kwargs (dict): Dictionary of keyword arguments from user
        Returns:
            None
        """
        invkwd = filter(lambda x: x not in args, kwargs.keys())
        if invkwd:
            warnings.warn('Got unexpected keyword argument(s) {}'.format(','.join(invkwd)), stacklevel=2)

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

        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Annotations
    def getAnnotations(self, annottype=None, codes=None, ids=None, **kwargs):
        """
        * Pass Nothing - return a list of all objects
        * Pass AnnotationTypeCV - return a list of all objects of the fiven type
        * Pass a list of codes - return a list of objects, one for each of the given codes
        * Pass a list of ids -return a list of objects, one for each of the given ids

        """
        # TODO What keywords do I use for type.
        a = Annotations
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the annottype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            annottype = kwargs['type']
        if annottype:
            if annottype == 'action':
                a = ActionAnnotations
            elif annottype == 'categoricalresultvalue':
                a = CategoricalResultValueAnnotations
            elif annottype == 'equipmentannotation':
                a = EquipmentAnnotations
            elif annottype == 'measurementresultvalue':
                a = MeasurementResultValueAnnotations
            elif annottype == 'method':
                a = MethodAnnotations
            elif annottype == 'pointcoverageresultvalue':
                a = PointCoverageResultValueAnnotations
            elif annottype == 'profileresultvalue':
                a = ProfileResultValueAnnotations
            elif annottype == 'result':
                a = ResultAnnotations
            elif annottype == 'samplingfeature':
                a = SamplingFeatureAnnotations
            elif annottype == 'sectionresultvalue':
                a = SectionResultValueAnnotations
            elif annottype == 'spectraresultvalue':
                a = SpectraResultValueAnnotations
            elif annottype == 'timeseriesresultvalue':
                a = TimeSeriesResultValueAnnotations
            elif annottype == 'trajectoryresultvalue':
                a = TrajectoryResultValueAnnotations
            elif annottype == 'transectresultvalue':
                a = TransectResultValueAnnotations
        try:
            query = self._session.query(a)
            if codes:
                query = query.filter(Annotations.AnnotationCode.in_(codes))
            if ids:
                query = query.filter(Annotations.AnnotationID.in_(ids))
            return query.all()

        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # CV
    def getCVs(self, cvtype, **kwargs):
        """
        getCVs(self, type):
        * Pass CVType - return a list of all objects of the given type

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the cvtype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            cvtype = kwargs['type']

        if cvtype == 'actiontype':
            CV = CVActionType
        elif cvtype == 'aggregationstatistic':
            CV = CVAggregationStatistic
        elif cvtype == 'annotationtype':
            CV = CVAnnotationType
        elif cvtype == 'censorcode':
            CV = CVCensorCode
        elif cvtype == 'dataqualitytype':
            CV = CVDataQualityType
        elif cvtype == 'dataset type':
            CV = CVDataSetType
        elif cvtype == 'Directive Type':
            CV = CVDirectiveType
        elif cvtype == 'Elevation Datum':
            CV = CVElevationDatum
        elif cvtype == 'Equipment Type':
            CV = CVEquipmentType
        elif cvtype == 'Medium':
            CV = CVMediumType
        elif cvtype == 'Method Type':
            CV = CVMethodType
        elif cvtype == 'Organization Type':
            CV = CVOrganizationType
        elif cvtype == 'Property Data Type':
            CV = CVPropertyDataType
        elif cvtype == 'Quality Code':
            CV = CVQualityCode
        elif cvtype == 'Relationship Type':
            CV = CVRelationshipType
        elif cvtype == 'Result Type':
            CV = CVResultType
        elif cvtype == 'Sampling Feature Geo-type':
            CV = CVSamplingFeatureGeoType
        elif cvtype == 'Sampling Feature Type':
            CV = CVSamplingFeatureType
        elif cvtype == 'Site Type':
            CV = CVSiteType
        elif cvtype == 'Spatial Offset Type':
            CV = CVSpatialOffsetType
        elif cvtype == 'Speciation':
            CV = CVSpeciation
        elif cvtype == 'Specimen Type':
            CV = CVSpecimenType
        elif cvtype == 'Status':
            CV = CVStatus
        elif cvtype == 'Taxonomic Classifier Type':
            CV = CVTaxonomicClassifierType
        elif cvtype == 'Units Type':
            CV = CVUnitsType
        elif cvtype == 'Variable Name':
            CV = CVVariableName
        elif cvtype == 'Variable Type':
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
            except Exception as e:
                print('Error running Query: {}'.format(e))
                pass

        if results:
            try:
                variables = [x[0] for x in self._session.query(distinct(Results.VariableID)).all()]
                if ids:
                    ids = list(set(ids).intersection(variables))
                else:
                    ids = variables
            except Exception as e:
                print('Error running Query: {}'.format(e))
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
    def getMethods(self, ids=None, codes=None, methodtype=None, **kwargs):
        """
        * Pass nothing - returns full list of method objects
        * Pass a list of MethodIDs - returns a single method object for each given id
        * Pass a list of MethodCode - returns a single method object for each given code
        * Pass a MethodType - returns a list of method objects of the given MethodType

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the medtype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            methodtype = kwargs['type']

        q = self._session.query(Methods)
        if ids:
            q = q.filter(Methods.MethodID.in_(ids))
        if codes:
            q = q.filter(Methods.MethodCode.in_(codes))
        if methodtype:
            q = q.filter_by(MethodTypeCV=methodtype)

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # ProcessingLevel
    def getProcessingLevels(self, ids=None, codes=None):
        """
        Retrieve a list of Processing Levels

        If no arguments are passed to the function, or their values are None,
        all Processing Levels objects in the database will be returned.

        Args:
            ids (list, optional): List of Processing Levels IDs.
            codes (list, optional): List of Processing Levels Codes.


        Returns:
            list: List of ProcessingLevels Objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getProcessingLevels(ids=[1, 3])
            >>> READ.getProcessingLevels(codes=['L1', 'L3'])

        """
        q = self._session.query(ProcessingLevels)
        if ids:
            q = q.filter(ProcessingLevels.ProcessingLevelID.in_(ids))
        if codes:
            q = q.filter(ProcessingLevels.ProcessingLevelCode.in_(codes))

        try:
            return q.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # Sampling Feature
    def getSamplingFeatures(self, ids=None, codes=None, uuids=None,
                            sftype=None, wkt=None, results=False, **kwargs):
        """Retrieve a list of Sampling Feature objects.

        If no arguments are passed to the function, or their values are None,
        all Sampling Feature objects in the database will be returned.

        Args:
            ids (list, optional): List of SamplingFeatureIDs.
            codes (list, optional): List of SamplingFeature Codes.
            uuids (list, optional): List of UUIDs string.
            sftype (str, optional): Type of Sampling Feature from
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
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the sftype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            sftype = kwargs['type']
        if results:
            try:
                fas = [x[0] for x in self._session.query(distinct(Results.FeatureActionID)).all()]
            except Exception as e:
                print('Error running Query: {}'.format(e))
                return None
            sf = [x[0] for x in self._session.query(distinct(FeatureActions.SamplingFeatureID)).filter(FeatureActions.FeatureActionID.in_(fas)).all()]  # noqa
            if ids:
                ids = list(set(ids).intersection(sf))
            else:
                ids = sf

        q = self._session.query(SamplingFeatures)

        if sftype:
            q = q.filter_by(SamplingFeatureTypeCV=sftype)
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

        sf = self._session.query(distinct(SamplingFeatures.SamplingFeatureID)) \
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
    def getActions(self, ids=None, acttype=None, sfid=None, **kwargs):
        """
        * Pass nothing - returns a list of all Actions
        * Pass a list of Action ids - returns a list of Action objects
        * Pass a ActionTypeCV - returns a list of Action objects of that type
        * Pass a SamplingFeature ID - returns a list of Action objects
          associated with that Sampling feature ID, Found through featureAction table

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the acttype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            acttype = kwargs['type']
        a = Actions
        if acttype == 'equipment':
            a = EquipmentActions
        elif acttype == 'calibration':
            a = CalibrationActions
        elif acttype == 'maintenance':
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
    def getUnits(self, ids=None, name=None, unittype=None, **kwargs):
        """
        * Pass nothing - returns a list of all units objects
        * Pass a list of UnitsID - returns a single units object for the given id
        * Pass UnitsName - returns a single units object
        * Pass a type- returns a list of all objects of the given type

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the unittype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            unittype = kwargs['type']
        q = self._session.query(Units)
        if ids:
            q = q.filter(Units.UnitsID.in_(ids))
        if name:
            q = q.filter(Units.UnitsName.ilike(name))
        if unittype:
            q = q.filter(Units.UnitsTypeCV.ilike(unittype))
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
    def getResults(self, ids=None, restype=None, uuids=None, actionid=None, simulationid=None,
                   variableid=None, siteid=None, sfids=None, sfuuids=None, sfcodes=None, **kwargs):

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
        self._check_kwargs(['type', 'sfid'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the restype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            restype = kwargs['type']
        if restype:
            query = query.filter_by(ResultTypeCV=restype)
        if variableid:
            query = query.filter_by(VariableID=variableid)
        if ids:
            query = query.filter(Results.ResultID.in_(ids))
        if uuids:
            query = query.filter(Results.ResultUUID.in_(uuids))
        if simulationid:
            query = query.join(FeatureActions) \
                .join(Actions) \
                .join(Simulations) \
                .filter_by(SimulationID=simulationid)
        if actionid:
            query = query.join(FeatureActions).filter_by(ActionID=actionid)
        if 'sfid' in kwargs:
            warnings.warn("The parameter 'sfid' is deprecated. " +
                          "Please use the sfids parameter instead and send in a list.",
                          DeprecationWarning, stacklevel=2)
            if kwargs['sfid']:
                query = query.join(FeatureActions).filter_by(SamplingFeatureID=kwargs['sfid'])
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

            # TODO does this code do the same thing as the code above?
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
    def getDataSets(self, ids=None, codes=None, uuids=None, dstype=None):
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

        q = self._session.query(DataSetsResults) \
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

    def getDataSetsValues(self, ids=None, codes=None, uuids=None, dstype=None, lowercols=True):
        """
        Retrieve a list of datavalues associated with the given dataset info

        **Must specify either DataSetID OR DataSetUUID OR DataSetCode)**
        Args:
            ids (list, optional): List of DataSetsIDs.
            codes (list, optional): List of DataSet Codes.
            uuids (list, optional): List of Dataset UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.
            lowercols (bool, optional): Make column names to be lowercase.
                                        Default to True.
                                        **Please start upgrading your code to rely on CamelCase column names,
                                        In a near-future release,
                                        the default will be changed to False,
                                        and later the parameter may be removed**.


        Returns:
            list: List of Result Values Objects

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getDataSetsValues(ids=[39, 40])
            >>> READ.getDataSetsValues(codes=['HOME', 'FIELD'])
            >>> READ.getDataSetsValues(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getDataSetsValues(dstype='singleTimeSeries', lowercols=False)

        """

        dsr = self.getDataSetsResults(ids, codes, uuids, dstype)

        resids = []
        for ds in dsr:
            resids.append(ds.ResultID)

        try:
            return self.getResultValues(resultids=resids, lowercols=lowercols)
        except Exception as e:
            print('Error running Query {}'.format(e))
        return None

    def getSamplingFeatureDatasets(self, ids=None, codes=None, uuids=None, dstype=None, sftype=None):
        """
        Retrieve a list of Datasets associated with the given sampling feature data.

            **Must specify either samplingFeatureID OR samplingFeatureUUID OR samplingFeatureCode)**

        Args:
            ids (list, optional): List of SamplingFeatureIDs.
            codes (list, optional): List of SamplingFeature Codes.
            uuids (list, optional): List of UUIDs string.
            dstype (str, optional): Type of Dataset from
                `controlled vocabulary name <http://vocabulary.odm2.org/datasettype/>`_.
            sftype (str, optional): Type of SamplingFeature from
                `controlled vocabulary name <http://vocabulary.odm2.org/samplingfeaturetype/>`_.

        Returns:
            list: List of DataSetsResults Objects associated with the given sampling feature

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getSamplingFeatureDatasets(ids=[39, 40])
            >>> READ.getSamplingFeatureDatasets(codes=['HOME', 'FIELD'])
            >>> READ.getSamplingFeatureDatasets(uuids=['a6f114f1-5416-4606-ae10-23be32dbc202',
            ...                                 '5396fdf3-ceb3-46b6-aaf9-454a37278bb4'])
            >>> READ.getSamplingFeatureDatasets(dstype='singleTimeSeries')
            >>> READ.getSamplingFeatureDatasets(sftype='Specimen')

        """

        # make sure one of the three arguments has been sent in
        if all(v is None for v in [ids, codes, uuids, sftype]):
            raise ValueError(
                'Expected samplingFeatureID OR samplingFeatureUUID '
                'OR samplingFeatureCode OR samplingFeatureType '
                'argument')

        sf_query = self._session.query(SamplingFeatures)
        if sftype:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureTypeCV == sftype)
        if ids:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureID.in_(ids))
        if codes:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureCode.in_(codes))
        if uuids:
            sf_query = sf_query.filter(SamplingFeatures.SamplingFeatureUUID.in_(uuids))

        sf_list = []
        for sf in sf_query.all():
            sf_list.append(sf)

        try:
            sfds = []
            for sf in sf_list:

                # Eager loading the data.
                q = self._session.query(DataSetsResults)\
                    .join(DataSetsResults.ResultObj)\
                    .join(Results.FeatureActionObj)\
                    .filter(FeatureActions.SamplingFeatureID == sf.SamplingFeatureID)\
                    .options(contains_eager(DataSetsResults.ResultObj)
                             .contains_eager(Results.FeatureActionObj)
                             .load_only(FeatureActions.SamplingFeatureID))

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
    def getEquipment(self, codes=None, equiptype=None, sfid=None, actionid=None, **kwargs):
        """
        * Pass nothing - returns a list of all Equipment objects
        * Pass a list of EquipmentCodes- return a list of all Equipment objects that match each of the codes
        * Pass a EquipmentType - returns a single Equipment object
        * Pass a SamplingFeatureID - returns a single Equipment object
        * Pass an ActionID - returns a single Equipment object

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the equiptype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            equiptype = kwargs['type']

        # NOTE: Equiptype currently unused!
        if equiptype:
            pass
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
    def getExtensionProperties(self, exptype=None, **kwargs):
        """
        * Pass nothing - return a list of all objects
        * Pass type- return a list of all objects of the given type

        """
        # Todo what values to use for extensionproperties type
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the exptype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            exptype = kwargs['type']
        e = ExtensionProperties
        if exptype == 'action':
            e = ActionExtensionPropertyValues
        elif exptype == 'citation':
            e = CitationExtensionPropertyValues
        elif exptype == 'method':
            e = MethodExtensionPropertyValues
        elif exptype == 'result':
            e = ResultExtensionPropertyValues
        elif exptype == 'samplingfeature':
            e = SamplingFeatureExtensionPropertyValues
        elif exptype == 'variable':
            e = VariableExtensionPropertyValues
        try:
            return self._session.query(e).all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None

    # External Identifiers
    def getExternalIdentifiers(self, eitype=None, **kwargs):
        """
        * Pass nothing - return a list of all objects
        * Pass type- return a list of all objects of the given type

        """
        self._check_kwargs(['type'], kwargs)
        if 'type' in kwargs:
            warnings.warn("The parameter 'type' is deprecated. Please use the eitype parameter instead.",
                          DeprecationWarning, stacklevel=2)
            eitype = kwargs['type']
        e = ExternalIdentifierSystems
        if eitype.lowercase == 'citation':
            e = CitationExternalIdentifiers
        elif eitype == 'method':
            e = MethodExternalIdentifiers
        elif eitype == 'person':
            e = PersonExternalIdentifiers
        elif eitype == 'referencematerial':
            e = ReferenceMaterialExternalIdentifiers
        elif eitype == 'samplingfeature':
            e = SamplingFeatureExternalIdentifiers
        elif eitype == 'spatialreference':
            e = SpatialReferenceExternalIdentifiers
        elif eitype == 'taxonomicclassifier':
            e = TaxonomicClassifierExternalIdentifiers
        elif eitype == 'variable':
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

    def getResultValues(self, resultids, starttime=None, endtime=None, lowercols=True):
        """
        Retrieve result values associated with the given result.

            **The resultids must be associated with the same result type**
        Args:
            resultids (list): List of SamplingFeatureIDs.
            starttime (object, optional): Start time to filter by as datetime object.
            endtime (object, optional): End time to filter by as datetime object.
            lowercols (bool, optional): Make column names to be lowercase.
                                        Default to True.
                                        **Please start upgrading your code to rely on CamelCase column names,
                                        In a near-future release,
                                        the default will be changed to False,
                                        and later the parameter may be removed**.

        Returns:
            DataFrame: Pandas dataframe of result values.

        Examples:
            >>> READ = ReadODM2(SESSION_FACTORY)
            >>> READ.getResultValues(resultids=[10, 11])
            >>> READ.getResultValues(resultids=[100, 20, 34], starttime=datetime.today())
            >>> READ.getResultValues(resultids=[1, 2, 3, 4],
            >>>     starttime=datetime(2000, 01, 01),
            >>>     endtime=datetime(2003, 02, 01), lowercols=False)

        """
        restype = self._session.query(Results).filter_by(ResultID=resultids[0]).first().ResultTypeCV
        ResultValues = TimeSeriesResultValues
        if 'categorical' in restype.lower():
            ResultValues = CategoricalResultValues
        elif 'measurement' in restype.lower():
            ResultValues = MeasurementResultValues
        elif 'point' in restype.lower():
            ResultValues = PointCoverageResultValues
        elif 'profile' in restype.lower():
            ResultValues = ProfileResultValues
        elif 'section' in restype.lower():
            ResultValues = SectionResults
        elif 'spectra' in restype.lower():
            ResultValues = SpectraResultValues
        elif 'time' in restype.lower():
            ResultValues = TimeSeriesResultValues
        elif 'trajectory' in restype.lower():
            ResultValues = TrajectoryResultValues
        elif 'transect' in restype.lower():
            ResultValues = TransectResultValues

        q = self._session.query(ResultValues).filter(ResultValues.ResultID.in_(resultids))
        if starttime:
            q = q.filter(ResultValues.ValueDateTime >= starttime)
        if endtime:
            q = q.filter(ResultValues.ValueDateTime <= endtime)
        try:
            # F841 local variable 'vals' is assigned to but never used
            # vals = q.order_by(ResultType.ValueDateTime)
            query = q.statement.compile(dialect=self._session_factory.engine.dialect)
            df = pd.read_sql_query(
                sql=query,
                con=self._session_factory.engine,
                params=query.params
            )
            if not lowercols:
                df.columns = [self._get_columns(ResultValues)[c] for c in df.columns]
            else:
                warnings.warn(
                    "In a near-future release, " +
                    "the parameter 'lowercols' default will be changed to False, " +
                    "and later the parameter may be removed.",
                    DeprecationWarning, stacklevel=2)
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

    def getRelatedModels(self, modid=None, code=None, **kwargs):
        """
        getRelatedModels(self, id=None, code=None)
        * Pass a ModelID - get a list of converter objects related to the converter having ModelID
        * Pass a ModelCode - get a list of converter objects related to the converter having ModeCode

        """
        self._check_kwargs(['id'], kwargs)
        if 'id' in kwargs:
            warnings.warn("The parameter 'id' is deprecated. Please use the modid parameter instead.",
                          DeprecationWarning, stacklevel=2)
            modid = kwargs['id']
        m = self._session.query(Models).select_from(RelatedModels).join(RelatedModels.ModelObj)
        if modid:
            m = m.filter(RelatedModels.ModelID == modid)
        if code:
            m = m.filter(Models.ModelCode == code)

        try:
            return m.all()
        except Exception as e:
            print('Error running Query: {}'.format(e))
            return None
