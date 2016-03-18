# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import BIT, UNIQUEIDENTIFIER
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ActionAnnotation(Base):
    __tablename__ = 'ActionAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Action = relationship(u'Action')
    Annotation = relationship(u'Annotation')


class ActionBy(Base):
    __tablename__ = 'ActionBy'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    AffiliationID = Column(ForeignKey(u'ODM2.Affiliations.AffiliationID'), nullable=False)
    IsActionLead = Column(BIT, nullable=False)
    RoleDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))

    Action = relationship(u'Action')
    Affiliation = relationship(u'Affiliation')


class ActionDirective(Base):
    __tablename__ = 'ActionDirectives'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    DirectiveID = Column(ForeignKey(u'ODM2.Directives.DirectiveID'), nullable=False)

    Action = relationship(u'Action')
    Directive = relationship(u'Directive')


class ActionExtensionPropertyValue(Base):
    __tablename__ = 'ActionExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    Action = relationship(u'Action')
    ExtensionProperty = relationship(u'ExtensionProperty')


class Action(Base):
    __tablename__ = 'Actions'
    __table_args__ = {u'schema': 'ODM2'}

    ActionID = Column(Integer, primary_key=True)
    ActionTypeCV = Column(ForeignKey(u'ODM2.CV_ActionType.Name'), nullable=False)
    MethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    BeginDateTime = Column(DateTime, nullable=False)
    BeginDateTimeUTCOffset = Column(Integer, nullable=False)
    EndDateTime = Column(DateTime)
    EndDateTimeUTCOffset = Column(Integer)
    ActionDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    ActionFileLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    CV_ActionType = relationship(u'CVActionType')
    Method = relationship(u'Method')


class MaintenanceAction(Action):
    __tablename__ = 'MaintenanceActions'
    __table_args__ = {u'schema': 'ODM2'}

    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), primary_key=True)
    IsFactoryService = Column(BIT, nullable=False)
    MaintenanceCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    MaintenanceReason = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))


class CalibrationAction(Action):
    __tablename__ = 'CalibrationActions'
    __table_args__ = {u'schema': 'ODM2'}

    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), primary_key=True)
    CalibrationCheckValue = Column(Float(53))
    InstrumentOutputVariableID = Column(ForeignKey(u'ODM2.InstrumentOutputVariables.InstrumentOutputVariableID'), nullable=False)
    CalibrationEquation = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    InstrumentOutputVariable = relationship(u'InstrumentOutputVariable')


class Affiliation(Base):
    __tablename__ = 'Affiliations'
    __table_args__ = {u'schema': 'ODM2'}

    AffiliationID = Column(Integer, primary_key=True)
    PersonID = Column(ForeignKey(u'ODM2.People.PersonID'), nullable=False)
    OrganizationID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'))
    IsPrimaryOrganizationContact = Column(BIT)
    AffiliationStartDate = Column(Date, nullable=False)
    AffiliationEndDate = Column(Date)
    PrimaryPhone = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    PrimaryEmail = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PrimaryAddress = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    PersonLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    Organization = relationship(u'Organization')
    Person = relationship(u'Person')


class Annotation(Base):
    __tablename__ = 'Annotations'
    __table_args__ = {u'schema': 'ODM2'}

    AnnotationID = Column(Integer, primary_key=True)
    AnnotationTypeCV = Column(ForeignKey(u'ODM2.CV_AnnotationType.Name'), nullable=False)
    AnnotationCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    AnnotationText = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    AnnotationDateTime = Column(DateTime)
    AnnotationUTCOffset = Column(Integer)
    AnnotationLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    AnnotatorID = Column(ForeignKey(u'ODM2.People.PersonID'))
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'))

    CV_AnnotationType = relationship(u'CVAnnotationType')
    Person = relationship(u'Person')
    Citation = relationship(u'Citation')


class AuthorList(Base):
    __tablename__ = 'AuthorLists'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)
    PersonID = Column(ForeignKey(u'ODM2.People.PersonID'), nullable=False)
    AuthorOrder = Column(Integer, nullable=False)

    Citation = relationship(u'Citation')
    Person = relationship(u'Person')


class CVActionType(Base):
    __tablename__ = 'CV_ActionType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVAggregationStatistic(Base):
    __tablename__ = 'CV_AggregationStatistic'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVAnnotationType(Base):
    __tablename__ = 'CV_AnnotationType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVCensorCode(Base):
    __tablename__ = 'CV_CensorCode'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVDataQualityType(Base):
    __tablename__ = 'CV_DataQualityType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVDatasetType(Base):
    __tablename__ = 'CV_DatasetType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVDirectiveType(Base):
    __tablename__ = 'CV_DirectiveType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVElevationDatum(Base):
    __tablename__ = 'CV_ElevationDatum'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVEquipmentType(Base):
    __tablename__ = 'CV_EquipmentType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVMedium(Base):
    __tablename__ = 'CV_Medium'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVMethodType(Base):
    __tablename__ = 'CV_MethodType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVOrganizationType(Base):
    __tablename__ = 'CV_OrganizationType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVPropertyDataType(Base):
    __tablename__ = 'CV_PropertyDataType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVQualityCode(Base):
    __tablename__ = 'CV_QualityCode'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVRelationshipType(Base):
    __tablename__ = 'CV_RelationshipType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVResultType(Base):
    __tablename__ = 'CV_ResultType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSamplingFeatureGeoType(Base):
    __tablename__ = 'CV_SamplingFeatureGeoType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSamplingFeatureType(Base):
    __tablename__ = 'CV_SamplingFeatureType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSiteType(Base):
    __tablename__ = 'CV_SiteType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSpatialOffsetType(Base):
    __tablename__ = 'CV_SpatialOffsetType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSpeciation(Base):
    __tablename__ = 'CV_Speciation'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVSpecimenType(Base):
    __tablename__ = 'CV_SpecimenType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVStatu(Base):
    __tablename__ = 'CV_Status'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVTaxonomicClassifierType(Base):
    __tablename__ = 'CV_TaxonomicClassifierType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVUnitsType(Base):
    __tablename__ = 'CV_UnitsType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVVariableName(Base):
    __tablename__ = 'CV_VariableName'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CVVariableType(Base):
    __tablename__ = 'CV_VariableType'
    __table_args__ = {u'schema': 'ODM2'}

    Term = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Definition = Column(String(5000, u'SQL_Latin1_General_CP1_CI_AS'))
    Category = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SourceVocabularyURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class CalibrationReferenceEquipment(Base):
    __tablename__ = 'CalibrationReferenceEquipment'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.CalibrationActions.ActionID'), nullable=False)
    EquipmentID = Column(ForeignKey(u'ODM2.Equipment.EquipmentID'), nullable=False)

    CalibrationAction = relationship(u'CalibrationAction')
    Equipment = relationship(u'Equipment')


class CalibrationStandard(Base):
    __tablename__ = 'CalibrationStandards'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.CalibrationActions.ActionID'), nullable=False)
    ReferenceMaterialID = Column(ForeignKey(u'ODM2.ReferenceMaterials.ReferenceMaterialID'), nullable=False)

    CalibrationAction = relationship(u'CalibrationAction')
    ReferenceMaterial = relationship(u'ReferenceMaterial')


class CategoricalResultValueAnnotation(Base):
    __tablename__ = 'CategoricalResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.CategoricalResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    CategoricalResultValue = relationship(u'CategoricalResultValue')


class CategoricalResultValue(Base):
    __tablename__ = 'CategoricalResultValues'
    __table_args__ = (
        Index('uc_CategoricalResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.CategoricalResults.ResultID'), nullable=False)
    DataValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)

    CategoricalResult = relationship(u'CategoricalResult')


class CitationExtensionPropertyValue(Base):
    __tablename__ = 'CitationExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    Citation = relationship(u'Citation')
    ExtensionProperty = relationship(u'ExtensionProperty')


class CitationExternalIdentifier(Base):
    __tablename__ = 'CitationExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    CitationExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CitationExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    Citation = relationship(u'Citation')
    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')


class Citation(Base):
    __tablename__ = 'Citations'
    __table_args__ = {u'schema': 'ODM2'}

    CitationID = Column(Integer, primary_key=True)
    Title = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Publisher = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PublicationYear = Column(Integer, nullable=False)
    CitationLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class DataLoggerFile(Base):
    __tablename__ = 'DataLoggerFiles'
    __table_args__ = {u'schema': 'ODM2'}

    DataLoggerFileID = Column(Integer, primary_key=True)
    ProgramID = Column(ForeignKey(u'ODM2.DataloggerProgramFiles.ProgramID'), nullable=False)
    DataLoggerFileName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    DataLoggerFileDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    DataLoggerFileLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    DataloggerProgramFile = relationship(u'DataloggerProgramFile')


class DataQuality(Base):
    __tablename__ = 'DataQuality'
    __table_args__ = {u'schema': 'ODM2'}

    DataQualityID = Column(Integer, primary_key=True)
    DataQualityTypeCV = Column(ForeignKey(u'ODM2.CV_DataQualityType.Name'), nullable=False)
    DataQualityCode = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    DataQualityValue = Column(Float(53))
    DataQualityValueUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    DataQualityDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    DataQualityLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    CV_DataQualityType = relationship(u'CVDataQualityType')
    Unit = relationship(u'Unit')


class DataloggerFileColumn(Base):
    __tablename__ = 'DataloggerFileColumns'
    __table_args__ = {u'schema': 'ODM2'}

    DataloggerFileColumnID = Column(Integer, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'))
    DataLoggerFileID = Column(ForeignKey(u'ODM2.DataLoggerFiles.DataLoggerFileID'), nullable=False)
    InstrumentOutputVariableID = Column(ForeignKey(u'ODM2.InstrumentOutputVariables.InstrumentOutputVariableID'), nullable=False)
    ColumnLabel = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ColumnDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    MeasurementEquation = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ScanInterval = Column(Float(53))
    ScanIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    RecordingInterval = Column(Float(53))
    RecordingIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'))

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    DataLoggerFile = relationship(u'DataLoggerFile')
    InstrumentOutputVariable = relationship(u'InstrumentOutputVariable')
    Unit = relationship(u'Unit', primaryjoin='DataloggerFileColumn.RecordingIntervalUnitsID == Unit.UnitsID')
    Result = relationship(u'Result')
    Unit1 = relationship(u'Unit', primaryjoin='DataloggerFileColumn.ScanIntervalUnitsID == Unit.UnitsID')


class DataloggerProgramFile(Base):
    __tablename__ = 'DataloggerProgramFiles'
    __table_args__ = {u'schema': 'ODM2'}

    ProgramID = Column(Integer, primary_key=True)
    AffiliationID = Column(ForeignKey(u'ODM2.Affiliations.AffiliationID'), nullable=False)
    ProgramName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ProgramDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    ProgramVersion = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    ProgramFileLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    Affiliation = relationship(u'Affiliation')


class DatasetCitation(Base):
    __tablename__ = 'DatasetCitations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    DataSetID = Column(ForeignKey(u'ODM2.Datasets.DatasetID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)

    Citation = relationship(u'Citation')
    Dataset = relationship(u'Dataset')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class Dataset(Base):
    __tablename__ = 'Datasets'
    __table_args__ = {u'schema': 'ODM2'}

    DatasetID = Column(Integer, primary_key=True)
    DatasetUUID = Column(UNIQUEIDENTIFIER, nullable=False)
    DatasetTypeCV = Column(ForeignKey(u'ODM2.CV_DatasetType.Name'), nullable=False)
    DatasetCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    DatasetTitle = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    DatasetAbstract = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CV_DatasetType = relationship(u'CVDatasetType')


class DatasetsResult(Base):
    __tablename__ = 'DatasetsResults'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    DatasetID = Column(ForeignKey(u'ODM2.Datasets.DatasetID'), nullable=False)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)

    Dataset = relationship(u'Dataset')
    Result = relationship(u'Result')


class DerivationEquation(Base):
    __tablename__ = 'DerivationEquations'
    __table_args__ = {u'schema': 'ODM2'}

    DerivationEquationID = Column(Integer, primary_key=True)
    DerivationEquation = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    Results = relationship(u'Result', secondary='ResultDerivationEquations')


class Directive(Base):
    __tablename__ = 'Directives'
    __table_args__ = {u'schema': 'ODM2'}

    DirectiveID = Column(Integer, primary_key=True)
    DirectiveTypeCV = Column(ForeignKey(u'ODM2.CV_DirectiveType.Name'), nullable=False)
    DirectiveDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CV_DirectiveType = relationship(u'CVDirectiveType')


class Equipment(Base):
    __tablename__ = 'Equipment'
    __table_args__ = {u'schema': 'ODM2'}

    EquipmentID = Column(Integer, primary_key=True)
    EquipmentCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    EquipmentName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EquipmentTypeCV = Column(ForeignKey(u'ODM2.CV_EquipmentType.Name'), nullable=False)
    EquipmentModelID = Column(ForeignKey(u'ODM2.EquipmentModels.EquipmentModelID'), nullable=False)
    EquipmentSerialNumber = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EquipmentOwnerID = Column(ForeignKey(u'ODM2.People.PersonID'), nullable=False)
    EquipmentVendorID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'), nullable=False)
    EquipmentPurchaseDate = Column(DateTime, nullable=False)
    EquipmentPurchaseOrderNumber = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    EquipmentDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    EquipmentDocumentationLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    EquipmentModel = relationship(u'EquipmentModel')
    Person = relationship(u'Person')
    CV_EquipmentType = relationship(u'CVEquipmentType')
    Organization = relationship(u'Organization')


class EquipmentAnnotation(Base):
    __tablename__ = 'EquipmentAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    EquipmentID = Column(ForeignKey(u'ODM2.Equipment.EquipmentID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    Equipment = relationship(u'Equipment')


class EquipmentModel(Base):
    __tablename__ = 'EquipmentModels'
    __table_args__ = {u'schema': 'ODM2'}

    EquipmentModelID = Column(Integer, primary_key=True)
    ModelManufacturerID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'), nullable=False)
    ModelPartNumber = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    ModelName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ModelDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    IsInstrument = Column(BIT, nullable=False)
    ModelSpecificationsFileLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ModelLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    Organization = relationship(u'Organization')


class EquipmentUsed(Base):
    __tablename__ = 'EquipmentUsed'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    EquipmentID = Column(ForeignKey(u'ODM2.Equipment.EquipmentID'), nullable=False)

    Action = relationship(u'Action')
    Equipment = relationship(u'Equipment')


class ExtensionProperty(Base):
    __tablename__ = 'ExtensionProperties'
    __table_args__ = {u'schema': 'ODM2'}

    PropertyID = Column(Integer, primary_key=True)
    PropertyName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PropertyDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    PropertyDataTypeCV = Column(ForeignKey(u'ODM2.CV_PropertyDataType.Name'), nullable=False)
    PropertyUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))

    CV_PropertyDataType = relationship(u'CVPropertyDataType')
    Unit = relationship(u'Unit')


class ExternalIdentifierSystem(Base):
    __tablename__ = 'ExternalIdentifierSystems'
    __table_args__ = {u'schema': 'ODM2'}

    ExternalIdentifierSystemID = Column(Integer, primary_key=True)
    ExternalIdentifierSystemName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdentifierSystemOrganizationID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'), nullable=False)
    ExternalIdentifierSystemDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    ExternalIdentifierSystemURL = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    Organization = relationship(u'Organization')


class FeatureAction(Base):
    __tablename__ = 'FeatureActions'
    __table_args__ = {u'schema': 'ODM2'}

    FeatureActionID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)

    Action = relationship(u'Action')
    SamplingFeature = relationship(u'SamplingFeature')


class SpecimenBatchPostion(FeatureAction):
    __tablename__ = 'SpecimenBatchPostions'
    __table_args__ = {u'schema': 'ODM2'}

    FeatureActionID = Column(ForeignKey(u'ODM2.FeatureActions.FeatureActionID'), primary_key=True)
    BatchPositionNumber = Column(Integer, nullable=False)
    BatchPositionLabel = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class InstrumentOutputVariable(Base):
    __tablename__ = 'InstrumentOutputVariables'
    __table_args__ = {u'schema': 'ODM2'}

    InstrumentOutputVariableID = Column(Integer, primary_key=True)
    ModelID = Column(ForeignKey(u'ODM2.EquipmentModels.EquipmentModelID'), nullable=False)
    VariableID = Column(ForeignKey(u'ODM2.Variables.VariableID'), nullable=False)
    InstrumentMethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    InstrumentResolution = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    InstrumentAccuracy = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    InstrumentRawOutputUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    Method = relationship(u'Method')
    Unit = relationship(u'Unit')
    EquipmentModel = relationship(u'EquipmentModel')
    Variable = relationship(u'Variable')


class MeasurementResultValueAnnotation(Base):
    __tablename__ = 'MeasurementResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.MeasurementResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    MeasurementResultValue = relationship(u'MeasurementResultValue')


class MeasurementResultValue(Base):
    __tablename__ = 'MeasurementResultValues'
    __table_args__ = (
        Index('uc_MeasurementResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.MeasurementResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)

    MeasurementResult = relationship(u'MeasurementResult')


class MethodAnnotation(Base):
    __tablename__ = 'MethodAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    MethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    Method = relationship(u'Method')


class MethodCitation(Base):
    __tablename__ = 'MethodCitations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    MethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)

    Citation = relationship(u'Citation')
    Method = relationship(u'Method')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class MethodExtensionPropertyValue(Base):
    __tablename__ = 'MethodExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    MethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    Method = relationship(u'Method')
    ExtensionProperty = relationship(u'ExtensionProperty')


class MethodExternalIdentifier(Base):
    __tablename__ = 'MethodExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    MethodID = Column(ForeignKey(u'ODM2.Methods.MethodID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    MethodExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MethodExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    Method = relationship(u'Method')


class Method(Base):
    __tablename__ = 'Methods'
    __table_args__ = {u'schema': 'ODM2'}

    MethodID = Column(Integer, primary_key=True)
    MethodTypeCV = Column(ForeignKey(u'ODM2.CV_MethodType.Name'), nullable=False)
    MethodCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    MethodName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    MethodDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    MethodLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    OrganizationID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'))

    CV_MethodType = relationship(u'CVMethodType')
    Organization = relationship(u'Organization')


class ModelAffiliation(Base):
    __tablename__ = 'ModelAffiliations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ModelID = Column(ForeignKey(u'ODM2.Models.ModelID'), nullable=False)
    AffiliationID = Column(ForeignKey(u'ODM2.Affiliations.AffiliationID'), nullable=False)
    IsPrimary = Column(BIT, nullable=False)
    RoleDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))

    Affiliation = relationship(u'Affiliation')
    Model = relationship(u'Model')


class Model(Base):
    __tablename__ = 'Models'
    __table_args__ = {u'schema': 'ODM2'}

    ModelID = Column(Integer, primary_key=True)
    ModelCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    ModelName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ModelDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    Version = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ModelLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class Organization(Base):
    __tablename__ = 'Organizations'
    __table_args__ = {u'schema': 'ODM2'}

    OrganizationID = Column(Integer, primary_key=True)
    OrganizationTypeCV = Column(ForeignKey(u'ODM2.CV_OrganizationType.Name'), nullable=False)
    OrganizationCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    OrganizationName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    OrganizationDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    OrganizationLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ParentOrganizationID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'))

    CV_OrganizationType = relationship(u'CVOrganizationType')
    parent = relationship(u'Organization', remote_side=[OrganizationID])


class Person(Base):
    __tablename__ = 'People'
    __table_args__ = {u'schema': 'ODM2'}

    PersonID = Column(Integer, primary_key=True)
    PersonFirstName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PersonMiddleName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    PersonLastName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class PersonExternalIdentifier(Base):
    __tablename__ = 'PersonExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    PersonID = Column(ForeignKey(u'ODM2.People.PersonID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    PersonExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PersonExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    Person = relationship(u'Person')


class PointCoverageResultValueAnnotation(Base):
    __tablename__ = 'PointCoverageResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(BigInteger, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.PointCoverageResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    PointCoverageResultValue = relationship(u'PointCoverageResultValue')


class PointCoverageResultValue(Base):
    __tablename__ = 'PointCoverageResultValues'
    __table_args__ = (
        Index('uc_PointCoverageResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'XLocation', 'XLocationUnitsID', 'YLocation', 'YLocationUnitsID', 'CensorCodeCV', 'QualityCodeCV', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.PointCoverageResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    XLocation = Column(Float(53), nullable=False)
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    YLocation = Column(Float(53), nullable=False)
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)

    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    PointCoverageResult = relationship(u'PointCoverageResult')
    Unit = relationship(u'Unit', primaryjoin='PointCoverageResultValue.XLocationUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='PointCoverageResultValue.YLocationUnitsID == Unit.UnitsID')


class ProcessingLevel(Base):
    __tablename__ = 'ProcessingLevels'
    __table_args__ = {u'schema': 'ODM2'}

    ProcessingLevelID = Column(Integer, primary_key=True)
    ProcessingLevelCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Definition = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    Explanation = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))


class ProfileResultValueAnnotation(Base):
    __tablename__ = 'ProfileResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.ProfileResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    ProfileResultValue = relationship(u'ProfileResultValue')


class ProfileResultValue(Base):
    __tablename__ = 'ProfileResultValues'
    __table_args__ = (
        Index('uc_ProfileResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'ZLocation', 'ZAggregationInterval', 'ZLocationUnitsID', 'CensorCodeCV', 'QualityCodeCV', 'TimeAggregationInterval', 'TimeAggregationIntervalUnitsID', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.ProfileResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    ZLocation = Column(Float(53), nullable=False)
    ZAggregationInterval = Column(Float(53), nullable=False)
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    ProfileResult = relationship(u'ProfileResult')
    Unit = relationship(u'Unit', primaryjoin='ProfileResultValue.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='ProfileResultValue.ZLocationUnitsID == Unit.UnitsID')


class ReferenceMaterialExternalIdentifier(Base):
    __tablename__ = 'ReferenceMaterialExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ReferenceMaterialID = Column(ForeignKey(u'ODM2.ReferenceMaterials.ReferenceMaterialID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    ReferenceMaterialExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ReferenceMaterialExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    ReferenceMaterial = relationship(u'ReferenceMaterial')


class ReferenceMaterialValue(Base):
    __tablename__ = 'ReferenceMaterialValues'
    __table_args__ = {u'schema': 'ODM2'}

    ReferenceMaterialValueID = Column(Integer, primary_key=True)
    ReferenceMaterialID = Column(ForeignKey(u'ODM2.ReferenceMaterials.ReferenceMaterialID'), nullable=False)
    ReferenceMaterialValue = Column(Float(53), nullable=False)
    ReferenceMaterialAccuracy = Column(Float(53))
    VariableID = Column(ForeignKey(u'ODM2.Variables.VariableID'), nullable=False)
    UnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'))

    Citation = relationship(u'Citation')
    ReferenceMaterial = relationship(u'ReferenceMaterial')
    Unit = relationship(u'Unit')
    Variable = relationship(u'Variable')
    Results = relationship(u'Result', secondary='ResultNormalizationValues')


class ReferenceMaterial(Base):
    __tablename__ = 'ReferenceMaterials'
    __table_args__ = {u'schema': 'ODM2'}

    ReferenceMaterialID = Column(Integer, primary_key=True)
    ReferenceMaterialMediumCV = Column(ForeignKey(u'ODM2.CV_Medium.Name'), nullable=False)
    ReferenceMaterialOrganizationID = Column(ForeignKey(u'ODM2.Organizations.OrganizationID'), nullable=False)
    ReferenceMaterialCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    ReferenceMaterialLotCode = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    ReferenceMaterialPurchaseDate = Column(DateTime)
    ReferenceMaterialExpirationDate = Column(DateTime)
    ReferenceMaterialCertificateLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'))

    CV_Medium = relationship(u'CVMedium')
    Organization = relationship(u'Organization')
    SamplingFeature = relationship(u'SamplingFeature')


class RelatedAction(Base):
    __tablename__ = 'RelatedActions'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)

    Action = relationship(u'Action', primaryjoin='RelatedAction.ActionID == Action.ActionID')
    Action1 = relationship(u'Action', primaryjoin='RelatedAction.RelatedActionID == Action.ActionID')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedAnnotation(Base):
    __tablename__ = 'RelatedAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedAnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation', primaryjoin='RelatedAnnotation.AnnotationID == Annotation.AnnotationID')
    Annotation1 = relationship(u'Annotation', primaryjoin='RelatedAnnotation.RelatedAnnotationID == Annotation.AnnotationID')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedCitation(Base):
    __tablename__ = 'RelatedCitations'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedCitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'), nullable=False)

    Citation = relationship(u'Citation', primaryjoin='RelatedCitation.CitationID == Citation.CitationID')
    Citation1 = relationship(u'Citation', primaryjoin='RelatedCitation.RelatedCitationID == Citation.CitationID')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedDataset(Base):
    __tablename__ = 'RelatedDatasets'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    DataSetID = Column(ForeignKey(u'ODM2.Datasets.DatasetID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedDatasetID = Column(ForeignKey(u'ODM2.Datasets.DatasetID'), nullable=False)
    VersionCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))

    Dataset = relationship(u'Dataset', primaryjoin='RelatedDataset.DataSetID == Dataset.DatasetID')
    Dataset1 = relationship(u'Dataset', primaryjoin='RelatedDataset.RelatedDatasetID == Dataset.DatasetID')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedEquipment(Base):
    __tablename__ = 'RelatedEquipment'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    EquipmentID = Column(ForeignKey(u'ODM2.Equipment.EquipmentID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedEquipmentID = Column(ForeignKey(u'ODM2.Equipment.EquipmentID'), nullable=False)
    RelationshipStartDateTime = Column(DateTime, nullable=False)
    RelationshipStartDateTimeUTCOffset = Column(Integer, nullable=False)
    RelationshipEndDateTime = Column(DateTime)
    RelationshipEndDateTimeUTCOffset = Column(Integer)

    Equipment = relationship(u'Equipment', primaryjoin='RelatedEquipment.EquipmentID == Equipment.EquipmentID')
    Equipment1 = relationship(u'Equipment', primaryjoin='RelatedEquipment.RelatedEquipmentID == Equipment.EquipmentID')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedFeature(Base):
    __tablename__ = 'RelatedFeatures'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    SpatialOffsetID = Column(ForeignKey(u'ODM2.SpatialOffsets.SpatialOffsetID'))

    SamplingFeature = relationship(u'SamplingFeature', primaryjoin='RelatedFeature.RelatedFeatureID == SamplingFeature.SamplingFeatureID')
    CV_RelationshipType = relationship(u'CVRelationshipType')
    SamplingFeature1 = relationship(u'SamplingFeature', primaryjoin='RelatedFeature.SamplingFeatureID == SamplingFeature.SamplingFeatureID')
    SpatialOffset = relationship(u'SpatialOffset')


class RelatedModel(Base):
    __tablename__ = 'RelatedModels'
    __table_args__ = {u'schema': 'ODM2'}

    RelatedID = Column(Integer, primary_key=True)
    ModelID = Column(ForeignKey(u'ODM2.Models.ModelID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedModelID = Column(Integer, nullable=False)

    Model = relationship(u'Model')
    CV_RelationshipType = relationship(u'CVRelationshipType')


class RelatedResult(Base):
    __tablename__ = 'RelatedResults'
    __table_args__ = {u'schema': 'ODM2'}

    RelationID = Column(Integer, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)
    RelationshipTypeCV = Column(ForeignKey(u'ODM2.CV_RelationshipType.Name'), nullable=False)
    RelatedResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)
    VersionCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    RelatedResultSequenceNumber = Column(Integer)

    Result = relationship(u'Result', primaryjoin='RelatedResult.RelatedResultID == Result.ResultID')
    CV_RelationshipType = relationship(u'CVRelationshipType')
    Result1 = relationship(u'Result', primaryjoin='RelatedResult.ResultID == Result.ResultID')


class ResultAnnotation(Base):
    __tablename__ = 'ResultAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)
    BeginDateTime = Column(DateTime, nullable=False)
    EndDateTime = Column(DateTime, nullable=False)

    Annotation = relationship(u'Annotation')
    Result = relationship(u'Result')


t_ResultDerivationEquations = Table(
    'ResultDerivationEquations', metadata,
    Column('ResultID', ForeignKey(u'ODM2.Results.ResultID'), primary_key=True),
    Column('DerivationEquationID', ForeignKey(u'ODM2.DerivationEquations.DerivationEquationID'), nullable=False),
    schema='ODM2'
)


class ResultExtensionPropertyValue(Base):
    __tablename__ = 'ResultExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    ExtensionProperty = relationship(u'ExtensionProperty')
    Result = relationship(u'Result')


t_ResultNormalizationValues = Table(
    'ResultNormalizationValues', metadata,
    Column('ResultID', ForeignKey(u'ODM2.Results.ResultID'), primary_key=True),
    Column('NormalizedByReferenceMaterialValueID', ForeignKey(u'ODM2.ReferenceMaterialValues.ReferenceMaterialValueID'), nullable=False),
    schema='ODM2'
)


class Result(Base):
    __tablename__ = 'Results'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(BigInteger, primary_key=True)
    ResultUUID = Column(UNIQUEIDENTIFIER, nullable=False)
    FeatureActionID = Column(ForeignKey(u'ODM2.FeatureActions.FeatureActionID'), nullable=False)
    ResultTypeCV = Column(ForeignKey(u'ODM2.CV_ResultType.Name'), nullable=False)
    VariableID = Column(ForeignKey(u'ODM2.Variables.VariableID'), nullable=False)
    UnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    TaxonomicClassifierID = Column(ForeignKey(u'ODM2.TaxonomicClassifiers.TaxonomicClassifierID'))
    ProcessingLevelID = Column(ForeignKey(u'ODM2.ProcessingLevels.ProcessingLevelID'), nullable=False)
    ResultDateTime = Column(DateTime)
    ResultDateTimeUTCOffset = Column(BigInteger)
    ValidDateTime = Column(DateTime)
    ValidDateTimeUTCOffset = Column(BigInteger)
    StatusCV = Column(ForeignKey(u'ODM2.CV_Status.Name'))
    SampledMediumCV = Column(ForeignKey(u'ODM2.CV_Medium.Name'), nullable=False)
    ValueCount = Column(Integer, nullable=False)

    FeatureAction = relationship(u'FeatureAction')
    ProcessingLevel = relationship(u'ProcessingLevel')
    CV_ResultType = relationship(u'CVResultType')
    CV_Medium = relationship(u'CVMedium')
    CV_Statu = relationship(u'CVStatu')
    TaxonomicClassifier = relationship(u'TaxonomicClassifier')
    Unit = relationship(u'Unit')
    Variable = relationship(u'Variable')


class TimeSeriesResult(Result):
    __tablename__ = 'TimeSeriesResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    XLocation = Column(Float(53))
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedTimeSpacing = Column(Float(53))
    IntendedTimeSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='TimeSeriesResult.IntendedTimeSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit1 = relationship(u'Unit', primaryjoin='TimeSeriesResult.XLocationUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='TimeSeriesResult.YLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='TimeSeriesResult.ZLocationUnitsID == Unit.UnitsID')


class SectionResult(Result):
    __tablename__ = 'SectionResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedXSpacing = Column(Float(53))
    IntendedXSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedZSpacing = Column(Float(53))
    IntendedZSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedTimeSpacing = Column(Float(53))
    IntendedTimeSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='SectionResult.IntendedTimeSpacingUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='SectionResult.IntendedXSpacingUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='SectionResult.IntendedZSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit3 = relationship(u'Unit', primaryjoin='SectionResult.YLocationUnitsID == Unit.UnitsID')


class CategoricalResult(Result):
    __tablename__ = 'CategoricalResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    XLocation = Column(Float(53))
    XLocationUnitsID = Column(Integer)
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(Integer)
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(Integer)
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)

    CV_QualityCode = relationship(u'CVQualityCode')
    SpatialReference = relationship(u'SpatialReference')


class PointCoverageResult(Result):
    __tablename__ = 'PointCoverageResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedXSpacing = Column(Float(53))
    IntendedXSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedYSpacing = Column(Float(53))
    IntendedYSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(Integer, nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='PointCoverageResult.IntendedXSpacingUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='PointCoverageResult.IntendedYSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit2 = relationship(u'Unit', primaryjoin='PointCoverageResult.ZLocationUnitsID == Unit.UnitsID')


class MeasurementResult(Result):
    __tablename__ = 'MeasurementResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    XLocation = Column(Float(53))
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    SpatialReference = relationship(u'SpatialReference')
    Unit = relationship(u'Unit', primaryjoin='MeasurementResult.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='MeasurementResult.XLocationUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='MeasurementResult.YLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='MeasurementResult.ZLocationUnitsID == Unit.UnitsID')


class TrajectoryResult(Result):
    __tablename__ = 'TrajectoryResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedTrajectorySpacing = Column(Float(53))
    IntendedTrajectorySpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedTimeSpacing = Column(Float(53))
    IntendedTimeSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='TrajectoryResult.IntendedTimeSpacingUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='TrajectoryResult.IntendedTrajectorySpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')


class SpectraResult(Result):
    __tablename__ = 'SpectraResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    XLocation = Column(Float(53))
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedWavelengthSpacing = Column(Float(53))
    IntendedWavelengthSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='SpectraResult.IntendedWavelengthSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit1 = relationship(u'Unit', primaryjoin='SpectraResult.XLocationUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='SpectraResult.YLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='SpectraResult.ZLocationUnitsID == Unit.UnitsID')


class ProfileResult(Result):
    __tablename__ = 'ProfileResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    XLocation = Column(Float(53))
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    YLocation = Column(Float(53))
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedZSpacing = Column(Float(53))
    IntendedZSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedTimeSpacing = Column(Float(53))
    IntendedTimeSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='ProfileResult.IntendedTimeSpacingUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='ProfileResult.IntendedZSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit2 = relationship(u'Unit', primaryjoin='ProfileResult.XLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='ProfileResult.YLocationUnitsID == Unit.UnitsID')


class TransectResult(Result):
    __tablename__ = 'TransectResults'
    __table_args__ = {u'schema': 'ODM2'}

    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), primary_key=True)
    ZLocation = Column(Float(53))
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'))
    IntendedTransectSpacing = Column(Float(53))
    IntendedTransectSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    IntendedTimeSpacing = Column(Float(53))
    IntendedTimeSpacingUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    Unit = relationship(u'Unit', primaryjoin='TransectResult.IntendedTimeSpacingUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='TransectResult.IntendedTransectSpacingUnitsID == Unit.UnitsID')
    SpatialReference = relationship(u'SpatialReference')
    Unit2 = relationship(u'Unit', primaryjoin='TransectResult.ZLocationUnitsID == Unit.UnitsID')


class ResultsDataQuality(Base):
    __tablename__ = 'ResultsDataQuality'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.Results.ResultID'), nullable=False)
    DataQualityID = Column(ForeignKey(u'ODM2.DataQuality.DataQualityID'), nullable=False)

    DataQuality = relationship(u'DataQuality')
    Result = relationship(u'Result')


class SamplingFeatureAnnotation(Base):
    __tablename__ = 'SamplingFeatureAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    SamplingFeature = relationship(u'SamplingFeature')


class SamplingFeatureExtensionPropertyValue(Base):
    __tablename__ = 'SamplingFeatureExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    ExtensionProperty = relationship(u'ExtensionProperty')
    SamplingFeature = relationship(u'SamplingFeature')


class SamplingFeatureExternalIdentifier(Base):
    __tablename__ = 'SamplingFeatureExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    SamplingFeatureExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SamplingFeatureExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    SamplingFeature = relationship(u'SamplingFeature')


class SamplingFeature(Base):
    __tablename__ = 'SamplingFeatures'
    __table_args__ = {u'schema': 'ODM2'}

    SamplingFeatureID = Column(Integer, primary_key=True)
    SamplingFeatureUUID = Column(UNIQUEIDENTIFIER, nullable=False)
    SamplingFeatureTypeCV = Column(ForeignKey(u'ODM2.CV_SamplingFeatureType.Name'), nullable=False)
    SamplingFeatureCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    SamplingFeatureName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    SamplingFeatureDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    SamplingFeatureGeotypeCV = Column(ForeignKey(u'ODM2.CV_SamplingFeatureGeoType.Name'))
    FeatureGeometry = Column(NullType)
    Elevation_m = Column(Float(53))
    ElevationDatumCV = Column(ForeignKey(u'ODM2.CV_ElevationDatum.Name'))

    CV_ElevationDatum = relationship(u'CVElevationDatum')
    CV_SamplingFeatureGeoType = relationship(u'CVSamplingFeatureGeoType')
    CV_SamplingFeatureType = relationship(u'CVSamplingFeatureType')


class Specimen(SamplingFeature):
    __tablename__ = 'Specimens'
    __table_args__ = {u'schema': 'ODM2'}

    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), primary_key=True)
    SpecimenTypeCV = Column(ForeignKey(u'ODM2.CV_SpecimenType.Name'), nullable=False)
    SpecimenMediumCV = Column(ForeignKey(u'ODM2.CV_Medium.Name'), nullable=False)
    IsFieldSpecimen = Column(BIT, nullable=False)

    CV_Medium = relationship(u'CVMedium')
    CV_SpecimenType = relationship(u'CVSpecimenType')


class Site(SamplingFeature):
    __tablename__ = 'Sites'
    __table_args__ = {u'schema': 'ODM2'}

    SamplingFeatureID = Column(ForeignKey(u'ODM2.SamplingFeatures.SamplingFeatureID'), primary_key=True)
    SiteTypeCV = Column(ForeignKey(u'ODM2.CV_SiteType.Name'), nullable=False)
    Latitude = Column(Float(53), nullable=False)
    Longitude = Column(Float(53), nullable=False)
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'), nullable=False)

    CV_SiteType = relationship(u'CVSiteType')
    SpatialReference = relationship(u'SpatialReference')


class SectionResultValueAnnotation(Base):
    __tablename__ = 'SectionResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.SectionResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    SectionResultValue = relationship(u'SectionResultValue')


class SectionResultValue(Base):
    __tablename__ = 'SectionResultValues'
    __table_args__ = (
        Index('uc_SectionResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'XLocation', 'XAggregationInterval', 'XLocationUnitsID', 'ZLocation', 'ZAggregationInterval', 'ZLocationUnitsID', 'CensorCodeCV', 'QualityCodeCV', 'AggregationStatisticCV', 'TimeAggregationInterval', 'TimeAggregationIntervalUnitsID', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.SectionResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    XLocation = Column(Float(53), nullable=False)
    XAggregationInterval = Column(Float(53), nullable=False)
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    ZLocation = Column(BigInteger, nullable=False)
    ZAggregationInterval = Column(Float(53), nullable=False)
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    SectionResult = relationship(u'SectionResult')
    Unit = relationship(u'Unit', primaryjoin='SectionResultValue.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='SectionResultValue.XLocationUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='SectionResultValue.ZLocationUnitsID == Unit.UnitsID')


class Simulation(Base):
    __tablename__ = 'Simulations'
    __table_args__ = {u'schema': 'ODM2'}

    SimulationID = Column(Integer, primary_key=True)
    ActionID = Column(ForeignKey(u'ODM2.Actions.ActionID'), nullable=False)
    SimulationName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SimulationDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    SimulationStartDateTime = Column(DateTime, nullable=False)
    SimulationStartDateTimeUTCOffset = Column(Integer, nullable=False)
    SimulationEndDateTime = Column(DateTime, nullable=False)
    SimulationEndDateTimeUTCOffset = Column(Integer, nullable=False)
    TimeStepValue = Column(Float(53), nullable=False)
    TimeStepUnitsID = Column(Integer, nullable=False)
    InputDataSetID = Column(Integer)
    ModelID = Column(ForeignKey(u'ODM2.Models.ModelID'), nullable=False)

    Action = relationship(u'Action')
    Model = relationship(u'Model')


class SpatialOffset(Base):
    __tablename__ = 'SpatialOffsets'
    __table_args__ = {u'schema': 'ODM2'}

    SpatialOffsetID = Column(Integer, primary_key=True)
    SpatialOffsetTypeCV = Column(ForeignKey(u'ODM2.CV_SpatialOffsetType.Name'), nullable=False)
    Offset1Value = Column(Float(53), nullable=False)
    Offset1UnitID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    Offset2Value = Column(Float(53))
    Offset2UnitID = Column(ForeignKey(u'ODM2.Units.UnitsID'))
    Offset3Value = Column(Float(53))
    Offset3UnitID = Column(ForeignKey(u'ODM2.Units.UnitsID'))

    Unit = relationship(u'Unit', primaryjoin='SpatialOffset.Offset1UnitID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='SpatialOffset.Offset2UnitID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='SpatialOffset.Offset3UnitID == Unit.UnitsID')
    CV_SpatialOffsetType = relationship(u'CVSpatialOffsetType')


class SpatialReferenceExternalIdentifier(Base):
    __tablename__ = 'SpatialReferenceExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    SpatialReferenceID = Column(ForeignKey(u'ODM2.SpatialReferences.SpatialReferenceID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    SpatialReferenceExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SpatialReferenceExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    SpatialReference = relationship(u'SpatialReference')


class SpatialReference(Base):
    __tablename__ = 'SpatialReferences'
    __table_args__ = {u'schema': 'ODM2'}

    SpatialReferenceID = Column(Integer, primary_key=True)
    SRSCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'))
    SRSName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SRSDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    SRSLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))


class SpecimenTaxonomicClassifier(Base):
    __tablename__ = 'SpecimenTaxonomicClassifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    SamplingFeatureID = Column(ForeignKey(u'ODM2.Specimens.SamplingFeatureID'), nullable=False)
    TaxonomicClassifierID = Column(ForeignKey(u'ODM2.TaxonomicClassifiers.TaxonomicClassifierID'), nullable=False)
    CitationID = Column(ForeignKey(u'ODM2.Citations.CitationID'))

    Citation = relationship(u'Citation')
    Specimen = relationship(u'Specimen')
    TaxonomicClassifier = relationship(u'TaxonomicClassifier')


class SpectraResultValueAnnotation(Base):
    __tablename__ = 'SpectraResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.SpectraResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    SpectraResultValue = relationship(u'SpectraResultValue')


class SpectraResultValue(Base):
    __tablename__ = 'SpectraResultValues'
    __table_args__ = (
        Index('uc_SpectraResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'ExcitationWavelength', 'EmissionWavelength', 'WavelengthUnitsID', 'CensorCodeCV', 'QualityCodeCV', 'TimeAggregationInterval', 'TimeAggregationIntervalUnitsID', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.SpectraResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    ExcitationWavelength = Column(Float(53), nullable=False)
    EmissionWavelength = Column(Float(53), nullable=False)
    WavelengthUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    SpectraResult = relationship(u'SpectraResult')
    Unit = relationship(u'Unit', primaryjoin='SpectraResultValue.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='SpectraResultValue.WavelengthUnitsID == Unit.UnitsID')


class TaxonomicClassifierExternalIdentifier(Base):
    __tablename__ = 'TaxonomicClassifierExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    TaxonomicClassifierID = Column(ForeignKey(u'ODM2.TaxonomicClassifiers.TaxonomicClassifierID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    TaxonomicClassifierExternalIdentifier = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TaxonomicClassifierExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    TaxonomicClassifier = relationship(u'TaxonomicClassifier')


class TaxonomicClassifier(Base):
    __tablename__ = 'TaxonomicClassifiers'
    __table_args__ = {u'schema': 'ODM2'}

    TaxonomicClassifierID = Column(Integer, primary_key=True)
    TaxonomicClassifierTypeCV = Column(ForeignKey(u'ODM2.CV_TaxonomicClassifierType.Name'), nullable=False)
    TaxonomicClassifierName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TaxonomicClassifierCommonName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))
    TaxonomicClassifierDescription = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    ParentTaxonomicClassifierID = Column(ForeignKey(u'ODM2.TaxonomicClassifiers.TaxonomicClassifierID'))

    parent = relationship(u'TaxonomicClassifier', remote_side=[TaxonomicClassifierID])
    CV_TaxonomicClassifierType = relationship(u'CVTaxonomicClassifierType')


class TimeSeriesResultValueAnnotation(Base):
    __tablename__ = 'TimeSeriesResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.TimeSeriesResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    TimeSeriesResultValue = relationship(u'TimeSeriesResultValue')


class TimeSeriesResultValue(Base):
    __tablename__ = 'TimeSeriesResultValues'
    __table_args__ = (
        Index('uc_TimeSeriesResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'CensorCodeCV', 'QualityCodeCV', 'TimeAggregationInterval', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.TimeSeriesResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    TimeSeriesResult = relationship(u'TimeSeriesResult')
    Unit = relationship(u'Unit')


class TrajectoryResultValueAnnotation(Base):
    __tablename__ = 'TrajectoryResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.TrajectoryResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    TrajectoryResultValue = relationship(u'TrajectoryResultValue')


class TrajectoryResultValue(Base):
    __tablename__ = 'TrajectoryResultValues'
    __table_args__ = (
        Index('uc_TrajectoryResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'XLocation', 'XLocationUnitsID', 'YLocation', 'YLocationUnitsID', 'ZLocation', 'ZLocationUnitsID', 'TrajectoryDistance', 'TrajectoryDistanceAggregationInterval', 'TrajectoryDistanceUnitsID', 'CensorCodeCV', 'QualityCodeCV', 'TimeAggregationInterval', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.TrajectoryResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    XLocation = Column(Float(53), nullable=False)
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    YLocation = Column(Float(53), nullable=False)
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    ZLocation = Column(Float(53), nullable=False)
    ZLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    TrajectoryDistance = Column(Float(53), nullable=False)
    TrajectoryDistanceAggregationInterval = Column(Float(53), nullable=False)
    TrajectoryDistanceUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    TrajectoryResult = relationship(u'TrajectoryResult')
    Unit = relationship(u'Unit', primaryjoin='TrajectoryResultValue.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='TrajectoryResultValue.TrajectoryDistanceUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='TrajectoryResultValue.XLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='TrajectoryResultValue.YLocationUnitsID == Unit.UnitsID')
    Unit4 = relationship(u'Unit', primaryjoin='TrajectoryResultValue.ZLocationUnitsID == Unit.UnitsID')


class TransectResultValueAnnotation(Base):
    __tablename__ = 'TransectResultValueAnnotations'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    ValueID = Column(ForeignKey(u'ODM2.TransectResultValues.ValueID'), nullable=False)
    AnnotationID = Column(ForeignKey(u'ODM2.Annotations.AnnotationID'), nullable=False)

    Annotation = relationship(u'Annotation')
    TransectResultValue = relationship(u'TransectResultValue')


class TransectResultValue(Base):
    __tablename__ = 'TransectResultValues'
    __table_args__ = (
        Index('uc_TransectResultValues', 'ResultID', 'DataValue', 'ValueDateTime', 'ValueDateTimeUTCOffset', 'XLocation', 'XLocationUnitsID', 'YLocation', 'YLocationUnitsID', 'TransectDistance', 'TransectDistanceAggregationInterval', 'TransectDistanceUnitsID', 'CensorCodeCV', 'QualityCodeCV', 'AggregationStatisticCV', 'TimeAggregationInterval', 'TimeAggregationIntervalUnitsID', unique=True),
        {u'schema': 'ODM2'}
    )

    ValueID = Column(BigInteger, primary_key=True)
    ResultID = Column(ForeignKey(u'ODM2.TransectResults.ResultID'), nullable=False)
    DataValue = Column(Float(53), nullable=False)
    ValueDateTime = Column(DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column(Integer, nullable=False)
    XLocation = Column(Float(53), nullable=False)
    XLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    YLocation = Column(Float(53), nullable=False)
    YLocationUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    TransectDistance = Column(Float(53), nullable=False)
    TransectDistanceAggregationInterval = Column(Float(53), nullable=False)
    TransectDistanceUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)
    CensorCodeCV = Column(ForeignKey(u'ODM2.CV_CensorCode.Name'), nullable=False)
    QualityCodeCV = Column(ForeignKey(u'ODM2.CV_QualityCode.Name'), nullable=False)
    AggregationStatisticCV = Column(ForeignKey(u'ODM2.CV_AggregationStatistic.Name'), nullable=False)
    TimeAggregationInterval = Column(Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column(ForeignKey(u'ODM2.Units.UnitsID'), nullable=False)

    CV_AggregationStatistic = relationship(u'CVAggregationStatistic')
    CV_CensorCode = relationship(u'CVCensorCode')
    CV_QualityCode = relationship(u'CVQualityCode')
    TransectResult = relationship(u'TransectResult')
    Unit = relationship(u'Unit', primaryjoin='TransectResultValue.TimeAggregationIntervalUnitsID == Unit.UnitsID')
    Unit1 = relationship(u'Unit', primaryjoin='TransectResultValue.TransectDistanceUnitsID == Unit.UnitsID')
    Unit2 = relationship(u'Unit', primaryjoin='TransectResultValue.XLocationUnitsID == Unit.UnitsID')
    Unit3 = relationship(u'Unit', primaryjoin='TransectResultValue.YLocationUnitsID == Unit.UnitsID')


class Unit(Base):
    __tablename__ = 'Units'
    __table_args__ = {u'schema': 'ODM2'}

    UnitsID = Column(Integer, primary_key=True)
    UnitsTypeCV = Column(ForeignKey(u'ODM2.CV_UnitsType.Name'), nullable=False)
    UnitsAbbreviation = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UnitsName = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UnitsLink = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    CV_UnitsType = relationship(u'CVUnitsType')


class VariableExtensionPropertyValue(Base):
    __tablename__ = 'VariableExtensionPropertyValues'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    VariableID = Column(ForeignKey(u'ODM2.Variables.VariableID'), nullable=False)
    PropertyID = Column(ForeignKey(u'ODM2.ExtensionProperties.PropertyID'), nullable=False)
    PropertyValue = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    ExtensionProperty = relationship(u'ExtensionProperty')
    Variable = relationship(u'Variable')


class VariableExternalIdentifier(Base):
    __tablename__ = 'VariableExternalIdentifiers'
    __table_args__ = {u'schema': 'ODM2'}

    BridgeID = Column(Integer, primary_key=True)
    VariableID = Column(ForeignKey(u'ODM2.Variables.VariableID'), nullable=False)
    ExternalIdentifierSystemID = Column(ForeignKey(u'ODM2.ExternalIdentifierSystems.ExternalIdentifierSystemID'), nullable=False)
    VariableExternalIdentifer = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    VariableExternalIdentifierURI = Column(String(255, u'SQL_Latin1_General_CP1_CI_AS'))

    ExternalIdentifierSystem = relationship(u'ExternalIdentifierSystem')
    Variable = relationship(u'Variable')


class Variable(Base):
    __tablename__ = 'Variables'
    __table_args__ = {u'schema': 'ODM2'}

    VariableID = Column(Integer, primary_key=True)
    VariableTypeCV = Column(ForeignKey(u'ODM2.CV_VariableType.Name'), nullable=False)
    VariableCode = Column(String(50, u'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    VariableNameCV = Column(ForeignKey(u'ODM2.CV_VariableName.Name'), nullable=False)
    VariableDefinition = Column(String(500, u'SQL_Latin1_General_CP1_CI_AS'))
    SpeciationCV = Column(ForeignKey(u'ODM2.CV_Speciation.Name'))
    NoDataValue = Column(Float(53), nullable=False)

    CV_Speciation = relationship(u'CVSpeciation')
    CV_VariableName = relationship(u'CVVariableName')
    CV_VariableType = relationship(u'CVVariableType')
