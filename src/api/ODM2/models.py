from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship


# Should not be importing anything from a specific dialect
# from sqlalchemy.dialects.mssql.base import BIT

from apiCustomType import Geometry
'''
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
'''


#from base import modelBase as Base

from base import modelBase
Base = modelBase.Base
from base import Schema



# ################################################################################
# CV
# ################################################################################


class CVActionType(Base):
    __tablename__ = 'cv_actiontype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CVActionType('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVAggregationStatistic(Base):
    __tablename__ = 'cv_aggregationstatistic'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CVAggregationStatisticsType('%s', '%s', '%s', '%s')>" % (
        self.Term, self.name, self.Definition, self.Category)


class CVAnnotationType(Base):
    __tablename__ = 'cv_annotationtype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CVAnnotationType('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVCensorCode(Base):
    __tablename__ = 'cv_censorcode'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CVActionType('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVDatasetType(Base):
    __tablename__ = 'cv_datasettypecv'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVDirectiveType(Base):
    __tablename__ = 'cv_directivetype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVElevationDatum(Base):
    __tablename__ = 'cv_elevationdatum'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVEquipmentType(Base):
    __tablename__ = 'cv_equipmenttype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVMethodType(Base):
    __tablename__ = 'cv_methodtype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVOrganizationType(Base):
    __tablename__ = 'cv_organizationtype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVPropertyDataType(Base):
    __tablename__ = 'cv_propertydatatype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVQualityCode(Base):
    __tablename__ = 'cv_qualitycode'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVResultType(Base):
    __tablename__ = 'cv_resulttype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVRelationshipType(Base):
    __tablename__ = 'cv_relationshiptype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSampledMedium(Base):
    __tablename__ = 'cv_sampledmedium'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSamplingFeatureGeoType(Base):
    __tablename__ = 'cv_samplingfeaturegeotype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSamplingFeatureType(Base):
    __tablename__ = 'cv_samplingfeaturetype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSpatialOffsetType(Base):
    __tablename__ = 'cv_spatialoffsettype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSpeciation(Base):
    __tablename__ = 'cv_speciation'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSpecimenMedium(Base):
    __tablename__ = 'cv_specimenmedium'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSpecimenType(Base):
    __tablename__ = 'cv_specimentype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVSiteType(Base):
    __tablename__ = 'cv_sitetype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVReferenceMaterialMedium(Base):
    __tablename__ = 'cv_referencematerialmedium'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVStatus(Base):
    __tablename__ = 'cv_status'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVTaxonomicClassifierType(Base):
    __tablename__ = 'cv_taxonomicclassifiertype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVUnitsType(Base):
    __tablename__ = 'cv_unitstype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVVariableName(Base):
    __tablename__ = 'cv_variablename'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


class CVVariableType(Base):
    __tablename__ = 'cv_variabletype'
    __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)


# ################################################################################
# Core
# ################################################################################
class People(Base):
    __tablename__ = u'people'
    __table_args__ = {u'schema': Schema.getSchema()}

    PersonID = Column('personid', Integer, primary_key=True, nullable=False)
    PersonFirstName = Column('personfirstname', String(255), nullable=False)
    PersonMiddleName = Column('personmiddlename', String(255))
    PersonLastName = Column('personlastname', String(255), nullable=False)

    def __repr__(self):
        return "<Person('%s', '%s', '%s')>" % (self.PersonID, self.PersonFirstName,
                                               self.PersonLastName)


class Organizations(Base):
    __tablename__ = u'organizations'
    __table_args__ = {u'schema': Schema.getSchema()}

    OrganizationID = Column('organizationid', Integer, primary_key=True, nullable=False)
    OrganizationTypeCV = Column('organizationtypecv', ForeignKey(Schema.getSchema()+'.cv_organizationtype.name'), nullable=False,
                                index=True)
    OrganizationCode = Column('organizationcode', String(50), nullable=False)
    OrganizationName = Column('organizationname', String(255), nullable=False)
    OrganizationDescription = Column('organizationdescription', String(500))
    OrganizationLink = Column('organizationlink', String(255))
    ParentOrganizationID = Column('parentorganizationid', ForeignKey(Schema.getSchema()+'.organizations.organizationid'))

    OrganizationObj = relationship(u'Organizations', remote_side=[OrganizationID])

    def __repr__(self):
        return "<Organizations('%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.OrganizationID, self.OrganizationTypeCV, self.OrganizationCode,
            self.OrganizationName, self.OrganizationDescription, self.OrganizationLink
        )


class Affiliations(Base):
    __tablename__ = 'affiliations'
    __table_args__ = {u'schema': Schema.getSchema()}

    AffiliationID = Column('affiliationid', Integer, primary_key=True, nullable=False)
    PersonID = Column('personid', ForeignKey(Schema.getSchema()+'.people.personid'), nullable=False)
    OrganizationID = Column('organizationid', ForeignKey(Schema.getSchema()+'.organizations.organizationid'))
    IsPrimaryOrganizationContact = Column('isprimaryorganizationcontact', Boolean)
    AffiliationStartDate = Column('affiliationstartdate', Date, nullable=False)
    AffiliationEndDate = Column('affiliationenddate', Date)
    PrimaryPhone = Column('primaryphone', String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    PrimaryEmail = Column('primaryemail', String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PrimaryAddress = Column('primaryaddress', String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    PersonLink = Column('personlink', String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    OrganizationObj = relationship(Organizations)
    PersonObj = relationship(People)


class Methods(Base):
    __tablename__ = 'methods'
    __table_args__ = {u'schema': Schema.getSchema()}

    MethodID = Column('methodid', Integer, primary_key=True, nullable=False)
    MethodTypeCV = Column('methodtypecv', ForeignKey(Schema.getSchema()+'.cv_methodtype.name'), nullable=False, index=True)
    MethodCode = Column('methodcode', String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MethodName = Column('methodname', String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MethodDescription = Column('methoddescription', String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    MethodLink = Column('methodlink', String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    OrganizationID = Column('organizationid', Integer, ForeignKey(Schema.getSchema()+'.organizations.organizationid'))

    OrganizationObj = relationship(Organizations)

    def __repr__(self):
        return "<Methods('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.MethodID, self.MethodTypeCV, self.MethodCode, self.MethodName, self.MethodDescription,
                  self.MethodLink, self.OrganizationID)


class Actions(Base):
    __tablename__ = u'actions'
    __table_args__ = {u'schema': Schema.getSchema()}

    ActionID = Column('actionid', Integer, primary_key=True, nullable=False)
    ActionTypeCV = Column('actiontypecv', ForeignKey(Schema.getSchema()+'.cv_actiontype.name'), nullable=False, index=True)
    MethodID = Column('methodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    BeginDateTime = Column('begindatetime', DateTime, nullable=False)
    BeginDateTimeUTCOffset = Column('begindatetimeutcoffset', Integer, nullable=False)
    EndDateTime = Column('enddatetime', DateTime)
    EndDateTimeUTCOffset = Column('enddatetimeutcoffset', Integer)
    ActionDescription = Column('actiondescription', String(500))
    ActionFileLink = Column('actionfilelink', String(255))

    MethodObj = relationship(Methods)

    def __repr__(self):
        return "<Actions('%s', '%s', '%s', '%s')>" % (
            self.ActionID, self.ActionTypeCV, self.BeginDateTime, self.ActionDescription)


class ActionBy(Base):
    __tablename__ = u'actionby'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', Integer, ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    AffiliationID = Column('affiliationid', ForeignKey(Schema.getSchema()+'.affiliations.affiliationid'), nullable=False)
    IsActionLead = Column('isactionlead', Boolean, nullable=False)
    RoleDescription = Column('roledescription', String(500))

    ActionObj = relationship(Actions)
    AffiliationObj = relationship(Affiliations)


class SamplingFeatures(Base):
    __tablename__ = u'samplingfeatures'
    __table_args__ = {u'schema': Schema.getSchema()}

    SamplingFeatureID = Column('samplingfeatureid', Integer, primary_key=True, nullable=False)
    SamplingFeatureUUID = Column('samplingfeatureuuid', String(36), nullable=False)
    SamplingFeatureTypeCV = Column('samplingfeaturetypecv', ForeignKey(Schema.getSchema()+'.cv_samplingfeaturetype.name'),
                                   nullable=False, index=True)
    SamplingFeatureCode = Column('samplingfeaturecode', String(50), nullable=False)
    SamplingFeatureName = Column('samplingfeaturename', String(255))
    SamplingFeatureDescription = Column('samplingfeaturedescription', String(500))
    SamplingFeatureGeotypeCV = Column('samplingfeaturegeotypecv', ForeignKey(Schema.getSchema()+'.cv_samplingfeaturegeotype.name'),
                                      index=True)
    Elevation_m = Column('elevation_m', Float(53))
    ElevationDatumCV = Column('elevationdatumcv', ForeignKey(Schema.getSchema()+'.cv_elevationdatum.name'), index=True)
    FeatureGeometry = Column('featuregeometry', Geometry)

    def __repr__(self):
        return "<SamplingFeatures('%s', '%s', '%s', '%s')>" % (
            self.SamplingFeatureCode, self.SamplingFeatureName, self.SamplingFeatureDescription,
            self.Elevation_m)  # self.FeatureGeometry)


class FeatureActions(Base):
    __tablename__ = u'featureactions'
    __table_args__ = {u'schema': Schema.getSchema()}

    FeatureActionID = Column('featureactionid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)

    ActionObj = relationship(Actions)
    SamplingFeatureObj = relationship(SamplingFeatures)

    def __repr__(self):
        return "<FeatureActions('%s', '%s', '%s', )>" % (self.FeatureActionID, self.SamplingFeatureID, self.ActionID)


class Datasets(Base):
    __tablename__ = u'datasets'
    __table_args__ = {u'schema': Schema.getSchema()}

    DatasetID = Column('datasetid', Integer, primary_key=True, nullable=False)

    # This has been changed to String to support multiple database uuid types
    DatasetUUID = Column('datasetuuid', String(255), nullable=False)
    DatasetTypeCV = Column('datasettypecv', ForeignKey(Schema.getSchema()+'.cv_datasettypecv.name'), nullable=False, index=True)
    DatasetCode = Column('datasetcode', String(50), nullable=False)
    DatasetTitle = Column('datasettitle', String(255), nullable=False)
    DatasetAbstract = Column('datasetabstract', String(500), nullable=False)

    def __repr__(self):
        return "<Datasets('%s', '%s', '%s', '%s', '%s')>" % (
            self.DatasetID, self.DatasetTypeCV, self.DatasetCode, self.DatasetTitle, self.DatasetAbstract)


class ProcessingLevels(Base):
    __tablename__ = u'processinglevels'
    __table_args__ = {u'schema': Schema.getSchema()}

    ProcessingLevelID = Column('processinglevelid', Integer, primary_key=True, nullable=False)
    ProcessingLevelCode = Column('processinglevelcode', String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Definition = Column('definition', String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    Explanation = Column('explanation', String(500, u'SQL_Latin1_General_CP1_CI_AS'))

    def __repr__(self):
        return "<ProcessingLevels('%s', '%s', '%s', '%s')>" \
               % (self.ProcessingLevelID, self.ProcessingLevelCode, self.Definition, self.Explanation)


class RelatedActions(Base):
    __tablename__ = u'relatedactions'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedActionID = Column('relatedactionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)

    ActionObj = relationship(Actions, primaryjoin='RelatedActions.ActionID == Actions.ActionID')
    RelatedActionObj = relationship(Actions, primaryjoin='RelatedActions.RelatedActionID == Actions.ActionID')


class TaxonomicClassifiers(Base):
    __tablename__ = u'taxonomicclassifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    TaxonomicClassifierID = Column('taxonomicclassifierid', Integer, primary_key=True, nullable=False)
    TaxonomicClassifierTypeCV = Column('taxonomicclassifiertypcv', ForeignKey(Schema.getSchema()+'.cv_taxonomicclassifiertype.name'),
                                       nullable=False, index=True)
    TaxonomicClassifierName = Column('taxonomicclassifiername', String(255, u'SQL_Latin1_General_CP1_CI_AS'),
                                     nullable=False)
    TaxonomicClassifierCommonName = Column('taxonomicclassifiercommonname',
                                           String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    TaxonomicClassifierDescription = Column('taxonomicclassifierdescription',
                                            String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    ParentTaxonomicClassifierID = Column('parenttaxonomicclassifierid',
                                         ForeignKey(Schema.getSchema()+'.taxonomicclassifiers.taxonomicclassifierid'))

    parent = relationship(u'TaxonomicClassifiers', remote_side=[TaxonomicClassifierID])


class Units(Base):
    __tablename__ = u'units'
    __table_args__ = {u'schema': Schema.getSchema()}

    UnitsID = Column('unitsid', Integer, primary_key=True, nullable=False)
    UnitsTypeCV = Column('unitstypecv', ForeignKey(Schema.getSchema()+'.cv_unitstype.name'), nullable=False, index=True)
    UnitsAbbreviation = Column('unitsabbreviation', String(255), nullable=False)
    UnitsName = Column('unitsname', String, nullable=False)
    UnitsLink = Column('unitslink', String(255))

    def __repr__(self):
        return "<Units('%s', '%s', '%s', '%s')>" % (
        self.UnitsID, self.UnitsTypeCV, self.UnitsAbbreviation, self.UnitsName)


class Variables(Base):
    __tablename__ = u'variables'
    __table_args__ = {u'schema': Schema.getSchema()}

    VariableID = Column('variableid', Integer, primary_key=True, nullable=False)
    VariableTypeCV = Column('variabletypecv', ForeignKey(Schema.getSchema()+'.cv_variabletype.name'), nullable=False, index=True)
    VariableCode = Column('variablecode', String(50), nullable=False)
    VariableNameCV = Column('variablenamecv', ForeignKey(Schema.getSchema()+'.cv_variablename.name'), nullable=False, index=True)
    VariableDefinition = Column('variabledefinition', String(500))
    SpeciationCV = Column('speciationcv', ForeignKey(Schema.getSchema()+'.cv_speciation.name'), index=True)
    NoDataValue = Column('nodatavalue', Float(asdecimal=True), nullable=False)

    def __repr__(self):
        return "<Variables('%s', '%s', '%s')>" % (self.VariableID, self.VariableCode, self.VariableNameCV)


'''
class ResultTypeCV(Base):
    __tablename__ = u'ResultTypeCV'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultTypeCV = Column(String(255), primary_key=True)
    ResultTypeCategory = Column(String(255), nullable=False)
    DataType = Column(String(255), nullable=False)
    ResultTypeDefinition = Column(String(500), nullable=False)
    FixedDimensions = Column(String(255), nullable=False)
    VaryingDimensions = Column(String(255), nullable=False)
    SpaceMeasurementFramework = Column(String(255), nullable=False)
    TimeMeasurementFramework = Column(String(255), nullable=False)
    VariableMeasurementFramework = Column(String(255), nullable=False)
'''


class Results(Base):
    __tablename__ = u'results'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', BigInteger, primary_key=True)

    # This has been changed to String to support multiple database uuid types
    # ResultUUID = Column(UNIQUEIDENTIFIER, nullable=False)
    ResultUUID = Column('resultuuid', String(36), nullable=False)
    FeatureActionID = Column('featureactionid', ForeignKey(Schema.getSchema()+'.featureactions.featureactionid'), nullable=False)
    ResultTypeCV = Column(ForeignKey(Schema.getSchema()+'.cv_resulttypecv.name'), nullable=False, index=True)
    VariableID = Column('variableid', ForeignKey(Schema.getSchema()+'.variables.variableid'), nullable=False)
    UnitsID = Column('unitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(Schema.getSchema()+'.taxonomicclassifiers.taxonomicclassifierid'))
    ProcessingLevelID = Column('processinglevelid', ForeignKey(Schema.getSchema()+'.processinglevels.processinglevelid'),
                               nullable=False)
    ResultDateTime = Column('resultdatetime', DateTime)
    ResultDateTimeUTCOffset = Column('resultdatetimeutcoffset', BigInteger)
    ValidDateTime = Column('validdatetime', DateTime)
    ValidDateTimeUTCOffset = Column('validdatetimeutcoffset', BigInteger)
    StatusCV = Column('statuscv', ForeignKey(Schema.getSchema()+'.cv_status.name'), index=True)
    SampledMediumCV = Column('sampledmediumcv', ForeignKey(Schema.getSchema()+'.cv_sampledmedium.name'), nullable=False, index=True)
    ValueCount = Column('valuecount', Integer, nullable=False)

    # IntendedObservationSpacing = Column(String(255))

    FeatureActionObj = relationship(FeatureActions)
    ProcessingLevelObj = relationship(ProcessingLevels)

    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)
    UnitsObj = relationship(Units)
    VariableObj = relationship(Variables)

    def __repr__(self):
        return "<Results('%s', '%s', '%s', '%s', '%s')>" % (
            self.ResultID, self.ResultUUID, self.ResultTypeCV, self.ProcessingLevelID, self.ValueCount)


# ################################################################################
# Equipment
# ################################################################################
class EquipmentModels(Base):
    __tablename__ = u'equipmentmodels'
    __table_args__ = {u'schema': Schema.getSchema()}

    ModelID = Column('modelid', Integer, primary_key=True, nullable=False)
    ModelManufacturerID = Column('modelmanufacturerid', ForeignKey(Schema.getSchema()+'.organizations.organizationid'), nullable=False)
    ModelPartNumber = Column('modelpartnumber', String(50))
    ModelName = Column('modelname', String(255), nullable=False)
    ModelDescription = Column('modeldescription', String(500))
    ModelSpecificationsFileLink = Column('modelspecificationsfilelink', String(255))
    ModelLink = Column('modellink', String(255))
    IsInstrument = Column('isinstrument', Boolean, nullable=False)

    OrganizationObj = relationship(Organizations)


class Equipment(Base):
    __tablename__ = u'equipment'
    __table_args__ = {u'schema': Schema.getSchema()}

    EquipmentID = Column('equipmentid', Integer, primary_key=True, nullable=False)
    EquipmentCode = Column('equipmentcode', String(50), nullable=False)
    EquipmentName = Column('equipmentname', String(255), nullable=False)
    EquipmentTypeCV = Column('equipmenttypecv', ForeignKey(Schema.getSchema()+'.cv_equipmenttype.name'), nullable=False, index=True)
    ModelID = Column('modelid', ForeignKey(Schema.getSchema()+'.equipmentmodels.modelid'), nullable=False)
    EquipmentSerialNumber = Column('equipmentseriealnumber', String(50), nullable=False)
    EquipmentInventoryNumber = Column('equipmentinventorynumber', String(50))
    EquipmentOwnerID = Column('equipmentownerid', ForeignKey(Schema.getSchema()+'.people.personid'), nullable=False)
    EquipmentVendorID = Column('equipmentvendorid', ForeignKey(Schema.getSchema()+'.organizations.organizationid'), nullable=False)
    EquipmentPurchaseDate = Column('equipmentpurchasedate', DateTime, nullable=False)
    EquipmentPurchaseOrderNumber = Column('equipmentpurchaseordernumber', String(50))
    EquipmentPhotoFileLink = Column('equipmentphotofilelink', String(255))
    EquipmentDescription = Column('equipmentdescription', String(500))
    ParentEquipmentID = Column('parentequipmentid', ForeignKey(Schema.getSchema()+'.equipment.equipmentid'))

    PersonObj = relationship(People)
    OrganizationObj = relationship(Organizations)
    EquipmentModelObj = relationship(EquipmentModels)

    parent = relationship(u'Equipment', remote_side=[EquipmentID])


class EquipmentActions(Base):
    __tablename__ = u'equipmentactions'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    EquipmentID = Column('equipmentid', ForeignKey(Schema.getSchema()+'.equipment.equipmentid'), nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)

    ActionObj = relationship(Actions)
    EquipmentObj = relationship(Equipment)


class InstrumentOutputVariables(Base):
    __tablename__ = u'instrumentoutputvariables'
    __table_args__ = {u'schema': Schema.getSchema()}

    InstrumentOutputVariableID = Column('instrumentoutputvariableid', Integer, primary_key=True, nullable=False)
    ModelID = Column('modelid', ForeignKey(Schema.getSchema()+'.equipmentmodels.modelid'), nullable=False)
    VariableID = Column('variableid', ForeignKey(Schema.getSchema()+'.variables.variableid'), nullable=False)
    InstrumentMethodID = Column('instrumentmethodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    InstrumentResolution = Column('instrumentresolution', String(255))
    InstrumentAccuracy = Column('instrumentaccuracy', String(255))
    InstrumentRawOutputUnitsID = Column('instrumentrawoutputunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)

    MethodObj = relationship(Methods)
    OutputUnitObj = relationship(Units)
    EquipmentModelObj = relationship(EquipmentModels)
    VariableObj = relationship(Variables)


# ################################################################################
# Lab Analyses
# ################################################################################
class Directives(Base):
    __tablename__ = u'directives'
    __table_args__ = {u'schema': Schema.getSchema()}

    DirectiveID = Column('directiveid', Integer, primary_key=True, nullable=False)
    DirectiveTypeCV = Column('directivetypecv', ForeignKey(Schema.getSchema()+'.cv_directivetype.name'), nullable=False, index=True)
    DirectiveDescription = Column('directivedescription', String(500), nullable=False)


class ActionDirectives(Base):
    __tablename__ = u'actiondirectives'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    DirectiveID = Column('directiveid', ForeignKey(Schema.getSchema()+'.directives.directiveid'), nullable=False)

    ActionObj = relationship(Actions)
    DirectiveObj = relationship(Directives)


# ################################################################################
# Sampling Features
# ################################################################################
class SpatialReferences(Base):
    __tablename__ = u'spatialreferences'
    __table_args__ = {u'schema': Schema.getSchema()}

    SpatialReferenceID = Column('spatialreferenceid', Integer, primary_key=True, nullable=False)
    SRSCode = Column('srscode', String(50))
    SRSName = Column('srsname', String(255), nullable=False)
    SRSDescription = Column('srsdescription', String(500))
    SRSLink = Column('srslink', String(255))

    def __repr__(self):
        return "<SpatialReferences('%s', '%s', '%s', '%s', '%s')>" \
               % (self.SpatialReferenceID, self.SRSCode, self.SRSName, self.SRSDescription, self.SRSLink)


class Specimens(Base):
    __tablename__ = u'specimens'
    __table_args__ = {u'schema': Schema.getSchema()}

    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               primary_key=True)
    SpecimenTypeCV = Column('specimentypecv', ForeignKey(Schema.getSchema()+'.cv_specimentype.name'), nullable=False, index=True)
    SpecimenMediumCV = Column('specimenmediumcv', ForeignKey(Schema.getSchema()+'.cv_specimenmedium.name'), nullable=False, index=True)
    IsFieldSpecimen = Column('isfieldspecimen', Boolean, nullable=False)

    SamplingFeatureObj = relationship(SamplingFeatures)


class SpatialOffsets(Base):
    __tablename__ = u'spatialoffsets'
    __table_args__ = {u'schema': Schema.getSchema()}

    SpatialOffsetID = Column('spatialoffsetid', Integer, primary_key=True, nullable=False)
    SpatialOffsetTypeCV = Column('spatialoffsettypecv', ForeignKey(Schema.getSchema()+'.cv_spatialoffsettype.name'), nullable=False,
                                 index=True)
    Offset1Value = Column('offset1value', Float(53), nullable=False)
    Offset1UnitID = Column('offset1unitid', Integer, nullable=False)
    Offset2Value = Column('offset2value', Float(53))
    Offset2UnitID = Column('offset2unitid', Integer)
    Offset3Value = Column('offset3value', Float(53))
    Offset3UnitID = Column('offset3unitid', Integer)


class Sites(Base):
    __tablename__ = u'sites'
    __table_args__ = {u'schema': Schema.getSchema()}

    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               primary_key=True)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'),
                                nullable=False)
    SiteTypeCV = Column('sitetypecv', ForeignKey(Schema.getSchema()+'.cv_sitetype.name'), nullable=False, index=True)
    Latitude = Column('latitude', Float(53), nullable=False)
    Longitude = Column('longitude', Float(53), nullable=False)

    SpatialReferenceObj = relationship(SpatialReferences)
    SamplingFeatureObj = relationship(SamplingFeatures)

    def __repr__(self):
        return "<Sites('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.SamplingFeatureID, self.SpatialReferenceID, self.SiteTypeCV, self.Latitude, self.Longitude,
                  self.SpatialReferenceObj, self.SamplingFeatureObj)


class RelatedFeatures(Base):
    __tablename__ = u'relatedfeatures'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedFeatureID = Column('relatedfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'), nullable=False)
    SpatialOffsetID = Column('spatialoffsetid', ForeignKey(Schema.getSchema()+'.spatialoffsets.spatialoffsetid'))

    SamplingFeatureObj = relationship(SamplingFeatures,
                                      primaryjoin='RelatedFeatures.RelatedFeatureID == SamplingFeatures.SamplingFeatureID')
    RelatedFeatureObj = relationship(SamplingFeatures,
                                     primaryjoin='RelatedFeatures.SamplingFeatureID == SamplingFeatures.SamplingFeatureID')
    SpatialOffsetObj = relationship(SpatialOffsets)


class SpecimenTaxonomicClassifiers(Base):
    __tablename__ = u'specimentaxonomicclassifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.specimens.samplingfeatureid'), nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(Schema.getSchema()+'.taxonomicclassifiers.taxonomicclassifierid'), nullable=False)
    CitationID = Column('citationid', Integer)

    SpecimenObj = relationship(Specimens)
    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)


# ################################################################################
# Sensors
# ################################################################################
class DeploymentActions(Base):
    __tablename__ = u'deploymentactions'
    __table_args__ = {u'schema': Schema.getSchema()}

    DeploymentActionID = Column('deploymentactionid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    DeploymentTypeCV = Column('deploymenttypecv', ForeignKey(Schema.getSchema()+'.cv_deploymenttype.name'), nullable=False, index=True)
    DeploymentDescription = Column('deploymentdescription', String(500))
    ConfigurationActionID = Column('configurationactionid', Integer, nullable=False)
    CalibrationActionID = Column('calibrationactionid', Integer, nullable=False)
    SpatialOffsetID = Column('spatialoffsetid', Integer)
    DeploymentSchematicLink = Column('deploymentschematiclink', String(255))

    ActionObj = relationship(Actions)


class DataLoggerFiles(Base):
    __tablename__ = u'dataloggerfiles'
    __table_args__ = {u'schema': Schema.getSchema()}

    DataLoggerFileID = Column('dataloggerfileid', Integer, primary_key=True, nullable=False)
    DeploymentActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.deploymentactions.deploymentactionid'), nullable=False)
    DataLoggerOutputFileLink = Column('dataloggeroutputfilelink', String(255), nullable=False)
    DataLoggerOutputFileDescription = Column('dataloggeroutputfiledescription', String(500))

    DeploymentActionObj = relationship(DeploymentActions)


class Photos(Base):
    __tablename__ = u'photos'
    __table_args__ = {u'schema': Schema.getSchema()}

    PhotoID = Column('photoid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    PhotoFileLink = Column('photofilelink', String(255), nullable=False)
    PhotoDescription = Column('photodescription', String(500))

    ActionObj = relationship(Actions)


# ################################################################################
# Simulation
# ################################################################################
class Models(Base):
    __tablename__ = 'models'
    __table_args__ ={u'schema': Schema.getSchema()}

    ModelID = Column('modelid', Integer, primary_key=True, nullable=False)
    ModelCode = Column('modelcode', String(255), nullable=False)
    ModelName = Column('modelname', String(255), nullable=False)
    ModelDescription = Column('modeldescription', String(500))


class RelatedModels(Base):
    __tablename__ = 'relatedmodels'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    ModelID = Column('modelid', ForeignKey(Schema.getSchema()+'.models.modelid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedModelID = Column('relatedmodelid', ForeignKey(Schema.getSchema()+'.models.modelid'), nullable=False)

    ModelObj = relationship(Models, primaryjoin='RelatedModels.ModelID == Models.ModelID')
    RelatedModelObj = relationship(Models, primaryjoin='RelatedModels.RelatedModelID == Models.ModelID')


class Simulations(Base):
    __tablename__ = 'simulations'
    __table_args__ = {u'schema': Schema.getSchema()}

    SimulationID = Column('simulationid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    SimulationName = Column('simulationname', String(255), nullable=False)
    SimulationDescription = Column('simulationdescription', String(500))
    SimulationStartDateTime = Column('simulationstartdatetime', Date, nullable=False)
    SimulationStartDateTimeUTCOffset = Column('simulationstartdatetimeutcoffset', Integer, nullable=False)
    SimulationEndDateTime = Column('simulationenddatetime', Date, nullable=False)
    SimulationEndDateTimeUTCOffset = Column('simulationenddatetimeutcoffset', Integer, nullable=False)
    TimeStepValue = Column('timestepvalue', Float(53), nullable=False)
    TimeStepUnitsID = Column('timestepunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    InputDatasetID = Column('inputdatasetid', ForeignKey(Schema.getSchema()+'.datasets.datasetid'))
    OutputDatasetID = Column('outputdatasetid', Integer)
    ModelID = Column('modelid', ForeignKey(Schema.getSchema()+'.models.modelid'), nullable=False)

    Action = relationship(Actions)
    Dataset = relationship(Datasets)
    Model = relationship(Models)
    Unit = relationship(Units)


# Part of the Provenance table, needed here to meet dependancies
class Citations(Base):
    __tablename__ = u'citations'
    __table_args__ = {u'schema': Schema.getSchema()}

    CitationID = Column('citationid', Integer, primary_key=True, nullable=False)
    Title = Column('title', String(255), nullable=False)
    Publisher = Column('publisher', String(255), nullable=False)
    PublicationYear = Column('publicationyear', Integer, nullable=False)
    CitationLink = Column('citationlink', String(255))

    def __repr__(self):
        return "<Citations('%s', '%s', '%s', '%s', '%s')>" % (
        self.CitationID, self.Title, self.Publisher, self.PublicationYear, self.CitationLink)


# ################################################################################
# Annotations
# ################################################################################
class Annotations(Base):
    __tablename__ = u'annotations'

    __table_args__ = {u'schema': Schema.getSchema()}

    AnnotationID = Column('annotationid', Integer, primary_key=True, nullable=False)
    AnnotationTypeCV = Column('annotationtypecv', ForeignKey(Schema.getSchema()+'.cv_annotationtype.name'), nullable=False, index=True)
    AnnotationCode = Column('annotationcode', String(50))
    AnnotationText = Column('annotationtext', String(500), nullable=False)
    AnnotationDateTime = Column('annotationdatetime', DateTime)
    AnnotationUTCOffset = Column('annotationutcoffset', Integer)
    AnnotationLink = Column('annotationlink', String(255))
    AnnotatorID = Column('annotatorid', ForeignKey(Schema.getSchema()+'.people.personid'))
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'))

    PersonObj = relationship(People)
    CitationObj = relationship(Citations)


class ActionAnnotations(Base):
    __tablename__ = u'actionannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)

    ActionObj = relationship(Actions)
    AnnotationObj = relationship(Annotations)


class MethodAnnotations(Base):
    __tablename__ = u'methodannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)

    AnnotationObj = relationship(Annotations)
    MethodObj = relationship(Methods)


class ResultAnnotations(Base):
    __tablename__ = u'resultannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)
    BeginDateTime = Column('begindatetime', DateTime, nullable=False)
    EndDateTime = Column('enddatetime', DateTime, nullable=False)

    AnnotationObj = relationship(Annotations)
    ResultObj = relationship(Results)


class ResultValueAnnotations(Base):
    __tablename__ = u'resultvalueannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)

    AnnotationObj = relationship(Annotations)


class SamplingFeatureAnnotations(Base):
    __tablename__ = u'samplingfeatureannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)

    AnnotationObj = relationship(Annotations)
    SamplingFeatureObj = relationship(SamplingFeatures)


# ################################################################################
# Data Quality
# ################################################################################
class DatasetsResults(Base):
    __tablename__ = u'datasetsresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    DatasetID = Column('datasetid', ForeignKey(Schema.getSchema()+'.datasets.datasetid'), nullable=False)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)

    DatasetObj = relationship(Datasets)
    ResultObj = relationship(Results)


class DataQuality(Base):
    __tablename__ = 'dataquality'
    __table_args__ = {u'schema': Schema.getSchema()}

    DataQualityID = Column('dataqualityid', Integer, primary_key=True, nullable=False)
    DataQualityTypeCV = Column('dataqualitytypecv', ForeignKey(Schema.getSchema()+'.cv_dataqualitytype.name'), nullable=False,
                               index=True)
    DataQualityCode = Column('dataqualitycode', String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    DataQualityValue = Column('dataqualityvalue', Float(53))
    DataQualityValueUnitsID = Column('dataqualityvalueunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    DataQualityDescription = Column('dataqualitydescription', String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    DataQualityLink = Column('dataqualitylink', String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    UnitObj = relationship(Units)


class ReferenceMaterials(Base):
    __tablename__ = 'referencematerials'
    __table_args__ = {u'schema': Schema.getSchema()}

    ReferenceMaterialID = Column('referencematerialid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialMediumCV = Column('referencematerialmediumcv', ForeignKey('cv_referencematerialmedium.name'), nullable=False, index=True)
    ReferenceMaterialOrganizationID = Column('referencematerialoranizationid',
                                             ForeignKey(Schema.getSchema()+'.organizations.organizationid'), nullable=False)
    ReferenceMaterialCode = Column('referencematerialcode', String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ReferenceMaterialLotCode = Column('referencemateriallotcode', String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ReferenceMaterialPurchaseDate = Column('referencematerialpurchasedate', DateTime)
    ReferenceMaterialExpirationDate = Column('referencematerialexpirationdate', DateTime)
    ReferenceMaterialCertificateLink = Column('referencematerialcertificatelink',
                                              String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'))

    OrganizationObj = relationship(Organizations)
    SamplingFeatureObj = relationship(SamplingFeatures)


ResultNormalizationValues = Table(
    u'resultnormalizationvalues', Base.metadata,
    Column(u'resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True),
    Column(u'normalizedbyreferencematerialvalueid', ForeignKey(Schema.getSchema()+'.referencematerialvalues.referencematerialvalueid'),
           nullable=False),
    schema='odm2'
)


class ReferenceMaterialValue(Base):
    __tablename__ = u'referencematerialvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ReferenceMaterialValueID = Column('referencematerialvalueid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialID = Column('referencematerialid', ForeignKey(Schema.getSchema()+'.referencematerials.referencematerialid'),
                                 nullable=False)
    ReferenceMaterialValue = Column('referencematerialvalue', Float(53), nullable=False)
    ReferenceMaterialAccuracy = Column('referencematerialaccuracy', Float(53))
    VariableID = Column('variableid', ForeignKey(Schema.getSchema()+'.variables.variableid'), nullable=False)
    UnitsID = Column('unitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)

    CitationObj = relationship(Citations)
    ReferenceMaterialObj = relationship(ReferenceMaterials)
    UnitObj = relationship(Units)
    VariableObj = relationship(Variables)
    ResultsObj = relationship(Results, secondary=ResultNormalizationValues)


class ResultsDataQuality(Base):
    __tablename__ = 'resultsdataquality'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)
    DataQualityID = Column('dataqualityid', ForeignKey(Schema.getSchema()+'.dataquality.dataqualityid'), nullable=False)

    DataQualityObj = relationship(DataQuality)
    ResultObj = relationship(Results)


# ################################################################################
# Extension Properties
# ################################################################################
class ExtensionProperties(Base):
    __tablename__ = u'extensionproperties'
    __table_args__ = {u'schema': Schema.getSchema()}

    PropertyID = Column('propertyid', Integer, primary_key=True, nullable=False)
    PropertyName = Column('propertyname', String(255), nullable=False)
    PropertyDescription = Column('propertydescription', String(500))
    PropertyDataTypeCV = Column('propertydatatypecv', ForeignKey(Schema.getSchema()+'.cv_propertydatatype.name'), nullable=False,
                                index=True)
    PropertyUnitsID = Column('propertyunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))

    UnitObj = relationship(Units)


class ActionExtensionPropertyValues(Base):
    __tablename__ = u'actionextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Schema.getSchema()+'.actions.actionid'), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ActionObj = relationship(Actions)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class CitationExtensionPropertyValues(Base):
    __tablename__ = u'citationextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    CitationObj = relationship(Citations)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class MethodExtensionPropertyValues(Base):
    __tablename__ = u'methodextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    MethodObj = relationship(Methods)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class ResultExtensionPropertyValues(Base):
    __tablename__ = u'resultextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    ResultObj = relationship(Results)


class SamplingFeatureExtensionPropertyValues(Base):
    __tablename__ = u'samplingfeatureextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    SamplingFeatureObj = relationship(SamplingFeatures)


class VariableExtensionPropertyValues(Base):
    __tablename__ = u'variableextensionpropertyvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    VariableID = Column('variableid', ForeignKey(Schema.getSchema()+'.variables.variableid'), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(Schema.getSchema()+'.extensionproperties.propertyid'), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    VariableObj = relationship(Variables)


# ################################################################################
# Extension Identifiers
# ################################################################################
class ExternalIdentifierSystems(Base):
    __tablename__ = u'externalidentifiersystems'
    __table_args__ = {u'schema': Schema.getSchema()}

    ExternalIdentifierSystemID = Column('externalidentifiersystemid', Integer, primary_key=True, nullable=False)
    ExternalIdentifierSystemName = Column('externalidentifiersystemname', String(255), nullable=False)
    IdentifierSystemOrganizationID = Column('identifiersystemorganizationid',
                                            ForeignKey(Schema.getSchema()+'.organizations.organizationid'), nullable=False)
    ExternalIdentifierSystemDescription = Column('externalidentifiersystemdescription', String(500))
    ExternalIdentifierSystemURL = Column('externalidentifiersystemurl', String(255))

    IdentifierSystemOrganizationObj = relationship(Organizations)

    def __repr__(self):
        return "<ExternalIdentifierSystems('%s', '%s', '%s', '%s', '%s')>" % (
            self.ExternalIdentifierSystemID, self.ExternalIdentifierSystemName,
            self.IdentifierSystemOrganizationID, self.ExternalIdentifierSystemDescription,
            self.ExternalIdentifierSystemURL)


class CitationExternalIdentifiers(Base):
    __tablename__ = u'citationexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    CitationExternalIdentifier = Column('citationexternaldentifier', String(255), nullable=False)
    CitationExternalIdentifierURI = Column('citationexternaldentifieruri', String(255))

    CitationObj = relationship(Citations)
    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)


class MethodExternalIdentifiers(Base):
    __tablename__ = u'methodexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    MethodExternalIdentifier = Column('methodexternalidentifier', String(255), nullable=False)
    MethodExternalIdentifierURI = Column('methodexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    MethodObj = relationship(Methods)


class PersonExternalIdentifiers(Base):
    __tablename__ = u'personexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    PersonID = Column('personid', ForeignKey(Schema.getSchema()+'.people.personid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    PersonExternalIdentifier = Column('personexternalidentifier', String(255), nullable=False)
    PersonExternalIdentifierURI = Column('personexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    PersonObj = relationship(People)


class ReferenceMaterialExternalIdentifiers(Base):
    __tablename__ = u'referencematerialexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialID = Column(ForeignKey(Schema.getSchema()+'.referencematerials.referencematerialid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    ReferenceMaterialExternalIdentifier = Column('referencematerialexternalidentifier', String(255), nullable=False)
    ReferenceMaterialExternalIdentifierURI = Column('referencematerialexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    ReferenceMaterialObj = relationship(ReferenceMaterials)


class SamplingFeatureExternalIdentifiers(Base):
    __tablename__ = u'samplingfeatureexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Schema.getSchema()+'.samplingfeatures.samplingfeatureid'),
                               nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    SamplingFeatureExternalIdentifier = Column('samplingfeatureexternalidentifier', String(255), nullable=False)
    SamplingFeatureExternalIdentifierURI = Column('samplingfeatureexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    SamplingFeatureObj = relationship(SamplingFeatures)


class SpatialReferenceExternalIdentifiers(Base):
    __tablename__ = u'spatialreferenceexternaledentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'),
                                nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    SpatialReferenceExternalIdentifier = Column('spatialreferenceexternalidentifier', String(255), nullable=False)
    SpatialReferenceExternalIdentifierURI = Column('spatialreferenceexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    SpatialReferenceObj = relationship(SpatialReferences)


class TaxonomicClassifierExternalIdentifiers(Base):
    __tablename__ = u'taxonomicclassifierexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(Schema.getSchema()+'.taxonomicclassifiers.taxonomicclassifierid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    TaxonomicClassifierExternalIdentifier = Column('taxonomicclassifierexternalidentifier', String(255), nullable=False)
    TaxonomicClassifierExternalIdentifierURI = Column('taxonomicclassifierexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)


class VariableExternalIdentifiers(Base):
    __tablename__ = u'variableexternalidentifiers'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    VariableID = Column('variableid', ForeignKey(Schema.getSchema()+'.variables.variableid'), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(Schema.getSchema()+'.externalidentifiersystems.externalidentifiersystemid'),
                                        nullable=False)
    VariableExternalIdentifier = Column('variableexternalidentifer', String(255), nullable=False)
    VariableExternalIdentifierURI = Column('variableexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    VariableObj = relationship(Variables)


# ################################################################################
# Provenance
# ################################################################################

class AuthorLists(Base):
    __tablename__ = u'authorlists'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)
    PersonID = Column('personid', ForeignKey(Schema.getSchema()+'.people.personid'), nullable=False)
    AuthorOrder = Column('authororder', Integer, nullable=False)

    CitationObj = relationship(Citations, primaryjoin='AuthorLists.CitationID == Citations.CitationID')
    PersonObj = relationship(People, primaryjoin='AuthorLists.PersonID == People.PersonID')

    def __repr__(self):
        return "<AuthorLists('%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.BridgeID, self.CitationID, self.PersonID, self.AuthorOrder, self.CitationObj, self.PersonObj)


class DatasetCitations(Base):
    __tablename__ = u'datasetcitations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    DatasetID = Column('datasetid', ForeignKey(Schema.getSchema()+'.datasets.datasetid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)

    CitationObj = relationship(Citations)
    DatasetObj = relationship(Datasets)


ResultDerivationEquations = Table(
    u'resultderivationequations', Base.metadata,
    Column(u'resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True),
    Column(u'derivationequationid', ForeignKey(Schema.getSchema()+'.derivationequations.derivationequationid'), nullable=False),
    schema=Schema.getSchema()
)


class DerivationEquations(Base):
    __tablename__ = u'derivationequations'
    __table_args__ = {u'schema': Schema.getSchema()}

    DerivationEquationID = Column('derivationequationid', Integer, primary_key=True, nullable=False)
    DerivationEquation = Column('derivationequation', String(255), nullable=False)

    ResultsObj = relationship(Results, secondary=ResultDerivationEquations)


class MethodCitations(Base):
    __tablename__ = u'methodcitations'
    __table_args__ = {u'schema': Schema.getSchema()}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Schema.getSchema()+'.methods.methodid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)

    CitationObj = relationship(Citations)
    MethodObj = relationship(Methods)


# from odm2.Annotations.model import Annotation
class RelatedAnnotations(Base):
    __tablename__ = u'relatedannotations'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedAnnotationID = Column('relatedannotationid', ForeignKey(Schema.getSchema()+'.annotations.annotationid'), nullable=False)

    AnnotationObj = relationship(Annotations, primaryjoin='RelatedAnnotations.AnnotationID == Annotations.AnnotationID')
    RelatedAnnotationObj = relationship(Annotations,
                                        primaryjoin='RelatedAnnotations.RelatedAnnotationID == Annotations.AnnotationID')


class RelatedCitations(Base):
    __tablename__ = u'relatedcitations'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedCitationID = Column('relatedcitationid', ForeignKey(Schema.getSchema()+'.citations.citationid'), nullable=False)

    CitationObj = relationship(Citations, primaryjoin='RelatedCitations.CitationID == Citations.CitationID')
    RelatedCitationObj = relationship(Citations,
                                      primaryjoin='RelatedCitations.RelatedCitationID == Citations.CitationID')


class RelatedDatasets(Base):
    __tablename__ = u'relateddatasets'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    DatasetID = Column('datasetid', ForeignKey(Schema.getSchema()+'.datasets.datasetid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedDatasetID = Column('relateddatasetid', ForeignKey(Schema.getSchema()+'.datasets.datasetid'), nullable=False)
    VersionCode = Column('versioncode', String(50))

    DatasetObj = relationship(Datasets, primaryjoin='RelatedDatasets.DatasetID == Datasets.DatasetID')
    RelatedDatasetObj = relationship(Datasets, primaryjoin='RelatedDatasets.RelatedDatasetID == Datasets.DatasetID')


class RelatedResults(Base):
    __tablename__ = u'relatedresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(Schema.getSchema()+'.cv_relationshiptype.name'), nullable=False,
                                index=True)
    RelatedResultID = Column('relatedresultid', ForeignKey(Schema.getSchema()+'.results.resultid'), nullable=False)
    VersionCode = Column('versioncode', String(50))
    RelatedResultSequenceNumber = Column('relatedresultsequencenumber', Integer)

    ResultObj = relationship(Results, primaryjoin='RelatedResults.RelatedResultID == Results.ResultID')
    RelatedResultObj = relationship(Results, primaryjoin='RelatedResults.ResultID == Results.ResultID')


# ################################################################################
# Results
# ################################################################################


class PointCoverageResults(Base):
    __tablename__ = u'pointcoverageresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedXSpacing = Column('intendedxspacing', Float(53))
    IntendedXSpacingUnitsID = Column('intendedxspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedYSpacing = Column('intendedyspacing', Float(53))
    IntendedYSpacingUnitsID = Column('intendedyspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', Integer, nullable=False)

    XUnitObj = relationship(Units, primaryjoin='PointCoverageResults.IntendedXSpacingUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='PointCoverageResults.IntendedYSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    ZUnitObj = relationship(Units, primaryjoin='PointCoverageResults.ZLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='PointCoverageResults.ResultID == Results.ResultID')


class ProfileResults(Base):
    __tablename__ = u'profileresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedZSpacing = Column('intendedzspacing', Float(53))
    IntendedZSpacingUnitsID = Column('intendedzspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    TimeUnitObj = relationship(Units, primaryjoin='ProfileResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='ProfileResults.IntendedZSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XUnitObj = relationship(Units, primaryjoin='ProfileResults.XLocationUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='ProfileResults.YLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='ProfileResults.ResultID == Results.ResultID')


class CategoricalResults(Base):
    __tablename__ = u'categoricalresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', Integer)
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', Integer)
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', Integer)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)

    SpatialReferenceObj = relationship(SpatialReferences)
    ResultObj = relationship(Results, primaryjoin='CategoricalResults.ResultID == Results.ResultID')


class TransectResults(Base):
    __tablename__ = u'transectresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedTransectSpacing = Column('intendedtransectspacing', Float(53))
    IntendedTransectSpacingUnitsID = Column('intendedtransectspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    TimeUnitObj = relationship(Units, primaryjoin='TransectResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    TransectUnitObj = relationship(Units, primaryjoin='TransectResults.IntendedTransectSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    ZUnitObj = relationship(Units, primaryjoin='TransectResults.ZLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='TransectResults.ResultID == Results.ResultID')


class SpectraResults(Base):
    __tablename__ = u'spectraresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedWavelengthSpacing = Column('intendedwavelengthspacing', Float(53))
    IntendedWavelengthSpacingUnitsID = Column('intendedwavelengthspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    WaveUnitObj = relationship(Units, primaryjoin='SpectraResults.IntendedWavelengthSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XUnitObj = relationship(Units, primaryjoin='SpectraResults.XLocationUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='SpectraResults.YLocationUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='SpectraResults.ZLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='SpectraResults.ResultID == Results.ResultID')


class TimeSeriesResults(Base):
    __tablename__ = u'timeseriesresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    IntendedTimeSpacingUnitsObj = relationship(Units,
                                               primaryjoin='TimeSeriesResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.ZLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='TimeSeriesResults.ResultID == Results.ResultID')

    def __repr__(self):
        return "<TimeSeriesResults('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
               (self.ResultID, self.XLocation, self.YLocation, self.XLocation,
                self.ResultObj, self.XLocationUnitsObj, self.SpatialReferenceObj,
                self.IntendedTimeSpacing, self.AggregationStatisticCV)


class SectionResults(Base):
    __tablename__ = u'sectionresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedXSpacing = Column('intendedxspacing', Float(53))
    IntendedXSpacingUnitsID = Column('intendedxpacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedZSpacing = Column('intendedzspacing', Float(53))
    IntendedZSpacingUnitsID = Column('intendedzspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    TimeUnitObj = relationship(Units, primaryjoin='SectionResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    XUnitObj = relationship(Units, primaryjoin='SectionResults.IntendedXSpacingUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='SectionResults.IntendedZSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    YUnitObj = relationship(Units, primaryjoin='SectionResults.YLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='SectionResults.ResultID == Results.ResultID')


class TrajectoryResults(Base):
    __tablename__ = u'trajectoryresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    IntendedTrajectorySpacing = Column('intendedtrajectoryspacing', Float(53))
    IntendedTrajectorySpacingUnitsID = Column('intendedtrajectoryspacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)

    TimeUnitObj = relationship(Units, primaryjoin='TrajectoryResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    TrajectoryUnitObj = relationship(Units,
                                     primaryjoin='TrajectoryResults.IntendedTrajectorySpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    ResultObj = relationship(Results, primaryjoin='TrajectoryResults.ResultID == Results.ResultID')


class MeasurementResults(Base):
    __tablename__ = u'measurementresults'
    __table_args__ = {u'schema': Schema.getSchema()}

    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.results.resultid'), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(Schema.getSchema()+'.spatialreferences.spatialreferenceid'))
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    SpatialReferenceObj = relationship(SpatialReferences)
    TimeUnitObj = relationship(Units, primaryjoin='MeasurementResults.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XUnitObjObj = relationship(Units, primaryjoin='MeasurementResults.XLocationUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='MeasurementResults.YLocationUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='MeasurementResults.ZLocationUnitsID == Units.UnitsID')
    ResultObj = relationship(Results, primaryjoin='MeasurementResults.ResultID == Results.ResultID')


class CategoricalResultValues(Base):
    __tablename__ = u'categoricalresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.categoricalresults.resultid'), nullable=False)
    DataValue = Column('datavalue', String(255), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)

    CategoricalResultObj = relationship(CategoricalResults)


class MeasurementResultValues(Base):
    __tablename__ = u'measurementresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.measurementresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)

    MeasurementResultObj = relationship(MeasurementResults)


class PointCoverageResultValues(Base):
    __tablename__ = u'pointcoverageresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.pointcoverageresults.resultid'), nullable=False)
    DataValue = Column('datavalue', BigInteger, nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)

    PointCoverageResultObj = relationship(PointCoverageResults)
    XUnitObj = relationship(Units, primaryjoin='PointCoverageResultValues.XLocationUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='PointCoverageResultValues.YLocationUnitsID == Units.UnitsID')


class ProfileResultValues(Base):
    __tablename__ = u'profileresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.profileresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    ZLocation = Column('zlocation', Float(53), nullable=False)
    ZAggregationInterval = Column('zaggregationinterval', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    ProfileResultObj = relationship(ProfileResults)
    TimeUnitObj = relationship(Units, primaryjoin='ProfileResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='ProfileResultValues.ZLocationUnitsID == Units.UnitsID')


class SectionResultValues(Base):
    __tablename__ = u'sectionresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.sectionresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', BigInteger, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', BigInteger, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XAggregationInterval = Column('xaggregationinterval', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    ZLocation = Column('zlocation', BigInteger, nullable=False)
    ZAggregationInterval = Column('zaggregationinterval', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    SectionResultObj = relationship(SectionResults)
    TimeUnitObj = relationship(Units, primaryjoin='SectionResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XUnitObj = relationship(Units, primaryjoin='SectionResultValues.XLocationUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='SectionResultValues.ZLocationUnitsID == Units.UnitsID')


class SpectraResultValues(Base):
    __tablename__ = u'spectraresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.spectraresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    ExcitationWavelength = Column('excitationwavelength', Float(53), nullable=False)
    EmissionWavelength = Column('emmistionwavelength', Float(53), nullable=False)
    WavelengthUnitsID = Column('wavelengthunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    SpectraResultObj = relationship(SpectraResults)
    TimeUnitObj = relationship(Units, primaryjoin='SpectraResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    WavelengthUnitObj = relationship(Units, primaryjoin='SpectraResultValues.WavelengthUnitsID == Units.UnitsID')


class TimeSeriesResultValues(Base):
    __tablename__ = u'timeseriesresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.timeseriesresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    TimeSeriesResultObj = relationship(TimeSeriesResults)
    TimeUnitObj = relationship(Units)

    def get_columns(self):
        return ["ValueID", "ResultID", "DataValue", "ValueDateTime", "ValueDateTimeUTCOffset",
                "CensorCodeCV", "QualityCodeCV", "TimeAggregationInterval", "TimeAggregationIntervalUnitsID"]

    def list_repr(self):
        return [self.ValueID, self.ResultID, self.DataValue, self.ValueDateTime, self.ValueDateTimeUTCOffset,
                self.CensorCodeCV, self.QualityCodeCV, self.TimeAggregationInterval,
                self.TimeAggregationIntervalUnitsID]

    def __repr__(self):
        return "<DataValue('%s', '%s', '%s')>" % (self.DataValue, self.ValueDateTime, self.TimeAggregationInterval)


class TrajectoryResultValues(Base):
    __tablename__ = u'trajectoryresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.trajectoryresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    ZLocation = Column('zlocation', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'), nullable=False)
    TrajectoryDistance = Column('trajectorydistance', Float(53), nullable=False)
    TrajectoryDistanceAggregationInterval = Column('trajectorydistanceaggregationinterval', Float(53), nullable=False)
    TrajectoryDistanceUnitsID = Column('trajectorydistanceunitsid', Integer, nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Schema.getSchema()+'.units.unitsid'),
                                            nullable=False)

    TrajectoryResultObj = relationship(TrajectoryResults)
    TimeUnitObj = relationship(Units,
                               primaryjoin='TrajectoryResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XUnitObj = relationship(Units, primaryjoin='TrajectoryResultValues.XLocationUnitsID == Units.UnitsID')
    YUnitObj = relationship(Units, primaryjoin='TrajectoryResultValues.YLocationUnitsID == Units.UnitsID')
    ZUnitObj = relationship(Units, primaryjoin='TrajectoryResultValues.ZLocationUnitsID == Units.UnitsID')


class TransectResultValues(Base):
    __tablename__ = u'transectresultvalues'
    __table_args__ = {u'schema': Schema.getSchema()}

    ValueID = Column('valueid', BigInteger, primary_key=True)
    ResultID = Column('resultid', ForeignKey(Schema.getSchema()+'.transectresults.resultid'), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', DateTime, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', Integer, nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', Integer, nullable=False)
    TransectDistance = Column('transectdistance', Float(53), nullable=False)
    TransectDistanceAggregationInterval = Column('transectdistanceaggregationinterval', Float(53), nullable=False)
    TransectDistanceUnitsID = Column('transectdistanceunitsid', Integer, nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(Schema.getSchema()+'.cv_censorcode.name'), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(Schema.getSchema()+'.cv_qualitycode.name'), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(Schema.getSchema()+'.cv_aggregationstatistic.name'),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', Integer, nullable=False)

    TransectResultObj = relationship(TransectResults)
