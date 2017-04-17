from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Integer, String, Boolean, case
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql, mysql, sqlite


from odm2api.base import modelBase

Base = modelBase.Base

BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')
BigIntegerType = BigIntegerType.with_variant(postgresql.BIGINT(), 'postgresql')
BigIntegerType = BigIntegerType.with_variant(mysql.BIGINT(), 'mysql')





def is_hex(s):
    try:
        int(s, base=16)
        return True
    except ValueError:
        return False


################################################################################
# CV
################################################################################
class CV (object):
    __table_args__ = {u'schema': 'odm2'}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CVActionType('%s', '%s', '%s', '%s')>" % (self.Term, self.Name, self.Definition, self.Category)

class CVActionType(Base, CV):
    __tablename__ = 'cv_actiontype'


class CVAggregationStatistic(Base, CV):
    __tablename__ = 'cv_aggregationstatistic'


class CVAnnotationType(Base, CV):
    __tablename__ = 'cv_annotationtype'


class CVCensorCode(Base, CV):
    __tablename__ = 'cv_censorcode'


class CVDataQualityType(Base, CV):
    __tablename__ = 'cv_dataqualitytype'


class CVDataSetType(Base, CV):
    __tablename__ = 'cv_datasettypecv'


class CVDeploymentType(Base, CV):
    __tablename__ = 'cv_deploymenttype'


class CVDirectiveType(Base, CV):
    __tablename__ = 'cv_directivetype'


class CVElevationDatum(Base, CV):
    __tablename__ = 'cv_elevationdatum'


class CVEquipmentType(Base, CV):
    __tablename__ = 'cv_equipmenttype'


class CVMediumType(Base, CV):
    __tablename__ = 'cv_medium'


class CVMethodType(Base, CV):
    __tablename__ = 'cv_methodtype'


class CVOrganizationType(Base, CV):
    __tablename__ = 'cv_organizationtype'


class CVPropertyDataType(Base, CV):
    __tablename__ = 'cv_propertydatatype'


class CVQualityCode(Base, CV):
    __tablename__ = 'cv_qualitycode'


class CVResultType(Base, CV):
    __tablename__ = 'cv_resulttype'


class CVRelationshipType(Base, CV):
    __tablename__ = 'cv_relationshiptype'


class CVSamplingFeatureGeoType(Base, CV):
    __tablename__ = 'cv_samplingfeaturegeotype'


class CVSamplingFeatureType(Base, CV):
    __tablename__ = 'cv_samplingfeaturetype'


class CVSpatialOffsetType(Base, CV):
    __tablename__ = 'cv_spatialoffsettype'


class CVSpeciation(Base, CV):
    __tablename__ = 'cv_speciation'


class CVSpecimenType(Base, CV):
    __tablename__ = 'cv_specimentype'


class CVSiteType(Base, CV):
    __tablename__ = 'cv_sitetype'


class CVStatus(Base, CV):
    __tablename__ = 'cv_status'


class CVTaxonomicClassifierType(Base, CV):
    __tablename__ = 'cv_taxonomicclassifiertype'


class CVUnitsType(Base, CV):
    __tablename__ = 'cv_unitstype'


class CVVariableName(Base, CV):
    __tablename__ = 'cv_variablename'


class CVVariableType(Base, CV):
    __tablename__ = 'cv_variabletype'


class CVReferenceMaterialMedium(Base, CV):
    __tablename__ = 'cv_referencematerialmedium'


# ################################################################################
# Core
# ################################################################################
class People(Base):

    PersonID = Column('personid', Integer, primary_key=True, nullable=False)
    PersonFirstName = Column('personfirstname', String(255), nullable=False)
    PersonMiddleName = Column('personmiddlename', String(255))
    PersonLastName = Column('personlastname', String(255), nullable=False)

    def __repr__(self):
        return "<Person('%s', '%s', '%s')>" % (self.PersonID, self.PersonFirstName,
                                               self.PersonLastName)


class Organizations(Base):

    OrganizationID = Column('organizationid', Integer, primary_key=True, nullable=False)
    OrganizationTypeCV = Column('organizationtypecv', ForeignKey(CVOrganizationType.Name), nullable=False,
                                index=True)
    OrganizationCode = Column('organizationcode', String(50), nullable=False)
    OrganizationName = Column('organizationname', String(255), nullable=False)
    OrganizationDescription = Column('organizationdescription', String(500))
    OrganizationLink = Column('organizationlink', String(255))
    ParentOrganizationID = Column('parentorganizationid', ForeignKey('odm2.organizations.organizationid'))

    OrganizationObj = relationship(u'Organizations', remote_side=[OrganizationID])

    def __repr__(self):
        return "<Organizations('%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.OrganizationID, self.OrganizationTypeCV, self.OrganizationCode,
            self.OrganizationName, self.OrganizationDescription, self.OrganizationLink
        )


class Affiliations(Base):

    AffiliationID = Column('affiliationid', Integer, primary_key=True, nullable=False)
    PersonID = Column('personid', ForeignKey(People.PersonID), nullable=False)
    OrganizationID = Column('organizationid', ForeignKey(Organizations.OrganizationID))
    IsPrimaryOrganizationContact = Column('isprimaryorganizationcontact', Boolean)
    AffiliationStartDate = Column('affiliationstartdate', Date, nullable=False)
    AffiliationEndDate = Column('affiliationenddate', Date)
    PrimaryPhone = Column('primaryphone', String(50))
    PrimaryEmail = Column('primaryemail', String(255), nullable=False)
    PrimaryAddress = Column('primaryaddress', String(255))
    PersonLink = Column('personlink', String(255))

    OrganizationObj = relationship(Organizations)
    PersonObj = relationship(People)


class Methods(Base):

    MethodID = Column('methodid', Integer, primary_key=True, nullable=False)
    MethodTypeCV = Column('methodtypecv', ForeignKey(CVMethodType.Name), nullable=False, index=True)
    MethodCode = Column('methodcode', String(50), nullable=False)
    MethodName = Column('methodname', String(255), nullable=False)
    MethodDescription = Column('methoddescription', String(500))
    MethodLink = Column('methodlink', String(255))
    OrganizationID = Column('organizationid', Integer, ForeignKey(Organizations.OrganizationID))

    OrganizationObj = relationship(Organizations)

    def __repr__(self):
        return "<Methods('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.MethodID, self.MethodTypeCV, self.MethodCode, self.MethodName, self.MethodDescription,
                  self.MethodLink, self.OrganizationID)


class Actions(Base):

    ActionID = Column('actionid', Integer, primary_key=True, nullable=False)
    ActionTypeCV = Column('actiontypecv', ForeignKey(CVActionType.Name), nullable=False, index=True)
    MethodID = Column('methodid', ForeignKey(Methods.MethodID), nullable=False)
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

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID), nullable=False)
    AffiliationID = Column('affiliationid', ForeignKey(Affiliations.AffiliationID), nullable=False)
    IsActionLead = Column('isactionlead', Boolean, nullable=False)
    RoleDescription = Column('roledescription', String(500))

    ActionObj = relationship(Actions)
    AffiliationObj = relationship(Affiliations)


class SamplingFeatures(Base):

    SamplingFeatureID = Column('samplingfeatureid', Integer, primary_key=True, nullable=False)
    SamplingFeatureUUID = Column('samplingfeatureuuid', String(36), nullable=False)
    SamplingFeatureTypeCV = Column('samplingfeaturetypecv', ForeignKey(CVSamplingFeatureType.Name),
                                   nullable=False, index=True)
    SamplingFeatureCode = Column('samplingfeaturecode', String(50), nullable=False)
    SamplingFeatureName = Column('samplingfeaturename', String(255))
    SamplingFeatureDescription = Column('samplingfeaturedescription', String(500))
    SamplingFeatureGeotypeCV = Column('samplingfeaturegeotypecv', ForeignKey(CVSamplingFeatureGeoType.Name),
                                      index=True)
    Elevation_m = Column('elevation_m', Float(53))
    ElevationDatumCV = Column('elevationdatumcv', ForeignKey(CVElevationDatum.Name), index=True)
    #FeatureGeometry = Column('featuregeometry',  String(50))
    FeatureGeometryWKT = Column('featuregeometrywkt', String(50))
    __mapper_args__ = {
        # 'polymorphic_on': SamplingFeatureTypeCV,
        "polymorphic_on":case([
            (SamplingFeatureTypeCV == "Specimen", "Specimen"),
            (SamplingFeatureTypeCV == "Site", "Site"),
        ], else_="samplingfeatures"),
        'polymorphic_identity':'samplingfeatures',

    }

    def __repr__(self):
        return "<SamplingFeatures('%s', '%s', '%s', '%s', '%s')>" % (
            self.SamplingFeatureCode, self.SamplingFeatureName, self.SamplingFeatureDescription,
            # self.Elevation_m, geomkt)
            self.Elevation_m, self.FeatureGeometryWKT)


class FeatureActions(Base):
    __tablename__ = u'featureactions'
    __table_args__ = {u'schema': 'odm2'}

    FeatureActionID = Column('featureactionid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)

    ActionObj = relationship(Actions)
    SamplingFeatureObj = relationship(SamplingFeatures)

    def __repr__(self):
        return "<FeatureActions('%s', '%s', '%s', )>" % (self.FeatureActionID, self.SamplingFeatureID, self.ActionID)


class DataSets(Base):
    __tablename__ = u'datasets'
    __table_args__ = {u'schema': 'odm2'}

    DataSetID = Column('datasetid', Integer, primary_key=True, nullable=False)

    # This has been changed to String to support multiple database uuid types
    DataSetUUID = Column('datasetuuid', String(255), nullable=False)
    DataSetTypeCV = Column('datasettypecv', ForeignKey(CVDataSetType.Name), nullable=False, index=True)
    DataSetCode = Column('datasetcode', String(50), nullable=False)
    DataSetTitle = Column('datasettitle', String(255), nullable=False)
    DataSetAbstract = Column('datasetabstract', String(500), nullable=False)

    def __repr__(self):
        return "<DataSets('%s', '%s', '%s', '%s', '%s')>" % (
            self.DataSetID, self.DataSetTypeCV, self.DataSetCode, self.DataSetTitle, self.DataSetAbstract)


class ProcessingLevels(Base):
    __tablename__ = u'processinglevels'
    __table_args__ = {u'schema': 'odm2'}

    ProcessingLevelID = Column('processinglevelid', Integer, primary_key=True, nullable=False)
    ProcessingLevelCode = Column('processinglevelcode', String(50), nullable=False)
    Definition = Column('definition', String(500))
    Explanation = Column('explanation', String(500))

    def __repr__(self):
        return "<ProcessingLevels('%s', '%s', '%s', '%s')>" \
               % (self.ProcessingLevelID, self.ProcessingLevelCode, self.Definition, self.Explanation)


class RelatedActions(Base):
    __tablename__ = u'relatedactions'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedActionID = Column('relatedactionid', ForeignKey(Actions.ActionID), nullable=False)

    ActionObj = relationship(Actions, primaryjoin='RelatedActions.ActionID == Actions.ActionID')
    RelatedActionObj = relationship(Actions, primaryjoin='RelatedActions.RelatedActionID == Actions.ActionID')


class TaxonomicClassifiers(Base):
    __tablename__ = u'taxonomicclassifiers'
    __table_args__ = {u'schema': 'odm2'}

    TaxonomicClassifierID = Column('taxonomicclassifierid', Integer, primary_key=True, nullable=False)
    TaxonomicClassifierTypeCV = Column('taxonomicclassifiertypecv', ForeignKey(CVTaxonomicClassifierType.Name),
                                       nullable=False, index=True)
    TaxonomicClassifierName = Column('taxonomicclassifiername', String(255),
                                     nullable=False)
    TaxonomicClassifierCommonName = Column('taxonomicclassifiercommonname', String(255))
    TaxonomicClassifierDescription = Column('taxonomicclassifierdescription', String(500))
    ParentTaxonomicClassifierID = Column('parenttaxonomicclassifierid',
                                         ForeignKey('odm2.taxonomicclassifiers.taxonomicclassifierid'))

    parent = relationship(u'TaxonomicClassifiers', remote_side=[TaxonomicClassifierID])


class Units(Base):
    __tablename__ = u'units'
    __table_args__ = {u'schema': 'odm2'}

    UnitsID = Column('unitsid', Integer, primary_key=True, nullable=False)
    UnitsTypeCV = Column('unitstypecv', ForeignKey(CVUnitsType.Name), nullable=False, index=True)
    UnitsAbbreviation = Column('unitsabbreviation', String(255), nullable=False)
    UnitsName = Column('unitsname', String, nullable=False)
    UnitsLink = Column('unitslink', String(255))

    def __repr__(self):
        return "<Units('%s', '%s', '%s', '%s')>" % (
            self.UnitsID, self.UnitsTypeCV, self.UnitsAbbreviation, self.UnitsName)


class Variables(Base):
    __tablename__ = u'variables'
    __table_args__ = {u'schema': 'odm2'}

    VariableID = Column('variableid', Integer, primary_key=True, nullable=False)
    VariableTypeCV = Column('variabletypecv', ForeignKey(CVVariableType.Name), nullable=False, index=True)
    VariableCode = Column('variablecode', String(50), nullable=False)
    VariableNameCV = Column('variablenamecv', ForeignKey(CVVariableName.Name), nullable=False, index=True)
    VariableDefinition = Column('variabledefinition', String(500))
    SpeciationCV = Column('speciationcv', ForeignKey(CVSpeciation.Name), index=True)
    NoDataValue = Column('nodatavalue', Float(asdecimal=True), nullable=False)

    def __repr__(self):
        return "<Variables('%s', '%s', '%s')>" % (self.VariableID, self.VariableCode, self.VariableNameCV)


class Results(Base):
    __tablename__ = u'results'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', BigIntegerType, primary_key=True)

    # This has been changed to String to support multiple database uuid types
    # ResultUUID = Column(UNIQUEIDENTIFIER, nullable=False)
    ResultUUID = Column('resultuuid', String(36), nullable=False)
    FeatureActionID = Column('featureactionid', ForeignKey(FeatureActions.FeatureActionID), nullable=False)
    ResultTypeCV = Column('resulttypecv', ForeignKey(CVResultType.Name), nullable=False, index=True)
    VariableID = Column('variableid', ForeignKey(Variables.VariableID), nullable=False)
    UnitsID = Column('unitsid', ForeignKey(Units.UnitsID), nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(TaxonomicClassifiers.TaxonomicClassifierID))
    ProcessingLevelID = Column('processinglevelid', ForeignKey(ProcessingLevels.ProcessingLevelID),
                               nullable=False)
    ResultDateTime = Column('resultdatetime', DateTime)
    ResultDateTimeUTCOffset = Column('resultdatetimeutcoffset', BigInteger)
    ValidDateTime = Column('validdatetime', DateTime)
    ValidDateTimeUTCOffset = Column('validdatetimeutcoffset', BigInteger)
    StatusCV = Column('statuscv', ForeignKey(CVStatus.Name), index=True)
    SampledMediumCV = Column('sampledmediumcv', ForeignKey(CVMediumType.Name), nullable=False, index=True)
    ValueCount = Column('valuecount', Integer, nullable=False)

    # IntendedObservationSpacing = Column(String(255))

    FeatureActionObj = relationship(FeatureActions)
    ProcessingLevelObj = relationship(ProcessingLevels)

    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)
    UnitsObj = relationship(Units)
    VariableObj = relationship(Variables)

    __mapper_args__ = {
        # 'polymorphic_on':ResultTypeCV,
        "polymorphic_on":case([
            (ResultTypeCV == "Point coverage", "Point coverage"),
            (ResultTypeCV == "Profile Coverage", "Profile Coverage"),
            (ResultTypeCV == "Category coverage", "Category coverage"),
            (ResultTypeCV == "Transect Coverage", "Transect Coverage"),
            (ResultTypeCV == "Spectra coverage", "Spectra coverage"),
            (ResultTypeCV == "Time series coverage", "Time series coverage"),
            (ResultTypeCV == "Section coverage", "Section coverage"),
            (ResultTypeCV == "Profile Coverage", "Profile Coverage"),
            (ResultTypeCV == "Trajectory coverage", "Trajectory coverage"),
            (ResultTypeCV == "Measurement", "Measurement"),
        ], else_="results"),
        'polymorphic_identity':'results',
        # 'with_polymorphic':'*'
    }

    def __repr__(self):
        return "<Results('%s', '%s', '%s', '%s', '%s')>" % (
            self.ResultID, self.ResultUUID, self.ResultTypeCV, self.ProcessingLevelID, self.ValueCount)


# ################################################################################
# Equipment
# ################################################################################


class DataLoggerProgramFiles(Base):
    __tablename__ = u'dataloggerprogramfiles'
    __table_args__ = {u'schema': 'odm2'}
    ProgramID = Column('programid', Integer, primary_key=True, nullable=False)
    AffiliationID = Column('affiliationid', Integer, ForeignKey(Affiliations.AffiliationID), nullable=False)
    ProgramName = Column('programname', String(255), nullable=False)
    ProgramDescription = Column('programdescription', String(500))
    ProgramVersion = Column('programversion', String(50))
    ProgramFileLink = Column('programfilelink', String(255))

    AffiliationObj = relationship(Affiliations)


class DataLoggerFiles(Base):
    __tablename__ = u'dataloggerfiles'
    __table_args__ = {u'schema': 'odm2'}

    DataLoggerFileID = Column('dataloggerfileid', Integer, primary_key=True, nullable=False)
    ProgramID = Column('actionid', Integer, ForeignKey(DataLoggerProgramFiles.ProgramID), nullable=False)
    DataLoggerFileName = Column('dataloggerfilename', String(255), nullable=False)
    DataLoggerOutputFileDescription = Column('dataloggeroutputfiledescription', String(500))
    DataLoggerOutputFileLink = Column('dataloggeroutputfilelink', String(255))

    ProgramObj = relationship(DataLoggerProgramFiles)


class EquipmentModels(Base):
    __tablename__ = u'equipmentmodels'
    __table_args__ = {u'schema': 'odm2'}

    ModelID = Column('modelid', Integer, primary_key=True, nullable=False)
    ModelManufacturerID = Column('modelmanufacturerid', Integer,
                                 ForeignKey(Organizations.OrganizationID), nullable=False)
    ModelPartNumber = Column('modelpartnumber', String(50))
    ModelName = Column('modelname', String(255), nullable=False)
    ModelDescription = Column('modeldescription', String(500))
    ModelSpecificationsFileLink = Column('modelspecificationsfilelink', String(255))
    ModelLink = Column('modellink', String(255))
    IsInstrument = Column('isinstrument', Boolean, nullable=False)

    OrganizationObj = relationship(Organizations)


class InstrumentOutputVariables(Base):
    __tablename__ = u'instrumentoutputvariables'
    __table_args__ = {u'schema': 'odm2'}

    InstrumentOutputVariableID = Column('instrumentoutputvariableid', Integer, primary_key=True, nullable=False)
    ModelID = Column('modelid', Integer, ForeignKey(EquipmentModels.ModelID), nullable=False)
    VariableID = Column('variableid', Integer, ForeignKey(Variables.VariableID), nullable=False)
    InstrumentMethodID = Column('instrumentmethodid', Integer, ForeignKey(Methods.MethodID), nullable=False)
    InstrumentResolution = Column('instrumentresolution', String(255))
    InstrumentAccuracy = Column('instrumentaccuracy', String(255))
    InstrumentRawOutputUnitsID = Column('instrumentrawoutputunitsid', Integer, ForeignKey(Units.UnitsID),
                                        nullable=False)

    MethodObj = relationship(Methods)
    OutputUnitObj = relationship(Units)
    EquipmentModelObj = relationship(EquipmentModels)
    VariableObj = relationship(Variables)


class DataLoggerFileColumns(Base):
    __tablename__ = u'dataloggerfilecolumns'
    __table_args__ = {u'schema': 'odm2'}

    DataLoggerFileColumnID = Column('dataloggerfilecolumnid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', BigInteger, ForeignKey(Results.ResultID))
    DataLoggerFileID = Column('dataloggerfileid', Integer,
                              ForeignKey(DataLoggerFiles.DataLoggerFileID), nullable=False)
    InstrumentOutputVariableID = Column('instrumentoutputvariableid', Integer,
                                        ForeignKey(InstrumentOutputVariables.VariableID),
                                        nullable=False)
    ColumnLabel = Column('columnlabel', String(50), nullable=False)
    ColumnDescription = Column('columndescription', String(500))
    MeasurementEquation = Column('measurmentequation', String(255))
    ScanInterval = Column('scaninterval', Float(50))
    ScanIntervalUnitsID = Column('scanintervalunitsid', Integer, ForeignKey(Units.UnitsID))
    RecordingInterval = Column('recordinginterval', Float(50))
    RecordingIntervalUnitsID = Column('recordingintervalunitsid', Integer, ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', String(255), ForeignKey(CVAggregationStatistic.Name),
                                    index=True)

    ResultObj = relationship(Results)
    DataLoggerFileObj = relationship(DataLoggerFiles)
    InstrumentOutputVariableObj = relationship(InstrumentOutputVariables)
    ScanIntervalUnitsObj = relationship(Units, primaryjoin='DataLoggerFileColumns.ScanIntervalUnitsID == Units.UnitsID')
    RecordingIntervalUnitsObj = relationship(Units, primaryjoin='DataLoggerFileColumns.RecordingIntervalUnitsID == Units.UnitsID')


class Equipment(Base):
    __tablename__ = u'equipment'
    __table_args__ = {u'schema': 'odm2'}

    EquipmentID = Column('equipmentid', Integer, primary_key=True, nullable=False)
    EquipmentCode = Column('equipmentcode', String(50), nullable=False)
    EquipmentName = Column('equipmentname', String(255), nullable=False)
    EquipmentTypeCV = Column('equipmenttypecv', ForeignKey(CVEquipmentType.Name), nullable=False, index=True)
    ModelID = Column('modelid', ForeignKey(EquipmentModels.ModelID), nullable=False)
    EquipmentSerialNumber = Column('equipmentseriealnumber', String(50), nullable=False)
    EquipmentInventoryNumber = Column('equipmentinventorynumber', String(50))
    EquipmentOwnerID = Column('equipmentownerid', ForeignKey(People.PersonID), nullable=False)
    EquipmentVendorID = Column('equipmentvendorid', ForeignKey(Organizations.OrganizationID), nullable=False)
    EquipmentPurchaseDate = Column('equipmentpurchasedate', DateTime, nullable=False)
    EquipmentPurchaseOrderNumber = Column('equipmentpurchaseordernumber', String(50))
    EquipmentDescription = Column('equipmentdescription', String(500))
    # ParentEquipmentID = Column('parentequipmentid', ForeignKey('odm2.equipment.equipmentid'))

    PersonObj = relationship(People)
    OrganizationObj = relationship(Organizations)
    EquipmentModelObj = relationship(EquipmentModels)

    # parent = relationship(u'Equipment', remote_side=[EquipmentID])


class CalibrationReferenceEquipment(Base):
    __tablename__ = u'calibrationreferenceequipment'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID), nullable=False)
    EquipmentID = Column('equipmentid', Integer, ForeignKey(Equipment.EquipmentID), nullable=False)

    ActionObj = relationship(Actions)
    EquipmentObj = relationship(Equipment)


class EquipmentActions(Base):
    __tablename__ = u'equipmentactions'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    EquipmentID = Column('equipmentid', ForeignKey(Equipment.EquipmentID), nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)

    ActionObj = relationship(Actions)
    EquipmentObj = relationship(Equipment)


class EquipmentUsed(Base):
    __tablename__ = u'equipmentused'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID), nullable=False)
    EquipmentID = Column('equipmentid', Integer, ForeignKey(Equipment.EquipmentID), nullable=False)

    ActionObj = relationship(Actions)
    EquipmentObj = relationship(Equipment)


class MaintenanceActions(Base):
    __tablename__ = u'maintenanceactions'
    __table_args__ = {u'schema': 'odm2'}

    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID), primary_key=True,  nullable=False)
    IsFactoryService = Column('isfactoryservce', Boolean, nullable=False)
    MaintenanceCode = Column('maintenancecode', String(50))
    MantenanceReason = Column('maintenancereason', String(50))

    ActionObj = relationship(Actions)


class RelatedEquipment(Base):
    __tablename__ = u'relatedequipment'
    __table_args__ = {u'schema': 'odm2'}
    RelationID = Column('relationid', Integer, primary_key=True, nullable=True)
    EquipmentID = Column('equipmentid', Integer, ForeignKey(Equipment.EquipmentID), nullable=True)
    RelationshipTypeCV = Column('relationshiptypecv', String(255), nullable=True, index=True)
    RelatedEquipmentID = Column('relatedequipmentid', Integer, ForeignKey(Equipment.EquipmentID), nullable=True)
    RelationshipStartDateTime = Column('relationshipstartdatetime', DateTime, nullable=True)
    RelationshipStartDateTimeUTCOffset = Column('relationshipstartdatetimeutcoffset', Integer, nullable=True)
    RelationshipEndDateTime = Column('relationshipenddatetime', DateTime)
    RelationshipEndDateTimeUTCOffset = Column('relationshipenddatetimeutcoffset', Integer)

    EquipmentObj = relationship(Equipment, primaryjoin='RelatedEquipment.EquipmentID == Equipment.EquipmentID')
    RelatedEquipmentObj = relationship(Equipment, primaryjoin='RelatedEquipment.RelatedEquipmentID == Equipment.EquipmentID')


class CalibrationActions(Base):
    __tablename__ = u'calibrationactions'
    __table_args__ = {u'schema': 'odm2'}
    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID),primary_key=True,  nullable=False)
    CalibrationCheckValue = Column('calibrationcheckvalue', Float(53))
    InstrumentOutputVariableID = Column('instrumentoutputvariableid', Integer,
                                        ForeignKey(InstrumentOutputVariables.VariableID), nullable=False)
    CalibrationEquation = Column('calibrationequation', String(255))

    ActionObj = relationship(Actions)
    InstrumentOutputVariableObj = relationship(InstrumentOutputVariables)

# ################################################################################
# Lab Analyses
# ################################################################################


class Directives(Base):
    __tablename__ = u'directives'
    __table_args__ = {u'schema': 'odm2'}

    DirectiveID = Column('directiveid', Integer, primary_key=True, nullable=False)
    DirectiveTypeCV = Column('directivetypecv', ForeignKey(CVDirectiveType.Name), nullable=False, index=True)
    DirectiveDescription = Column('directivedescription', String(500), nullable=False)


class ActionDirectives(Base):
    __tablename__ = u'actiondirectives'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)
    DirectiveID = Column('directiveid', ForeignKey(Directives.DirectiveID), nullable=False)

    ActionObj = relationship(Actions)
    DirectiveObj = relationship(Directives)


class SpecimenBatchPositions(Base):
    #todo fix misspelling
    __tablename__ = u'specimenbatchpostions'
    __table_args__ = {u'schema': 'odm2'}

    FeatureActionID = Column('featureactionid', Integer, ForeignKey(FeatureActions.FeatureActionID), primary_key=True, nullable=False)
    BatchPositionsNumber = Column('batchpositionnumber', Integer, nullable = False)
    BatchPositionLabel =Column('batchpositionlabel', String(255))

    FeatureActionObj = relationship(FeatureActions)


# ################################################################################
# Sampling Features
# ################################################################################
class SpatialReferences(Base):
    __tablename__ = u'spatialreferences'
    __table_args__ = {u'schema': 'odm2'}

    SpatialReferenceID = Column('spatialreferenceid', Integer, primary_key=True, nullable=False)
    SRSCode = Column('srscode', String(50))
    SRSName = Column('srsname', String(255), nullable=False)
    SRSDescription = Column('srsdescription', String(500))
    SRSLink = Column('srslink', String(255))

    def __repr__(self):
        return "<SpatialReferences('%s', '%s', '%s', '%s', '%s')>" \
               % (self.SpatialReferenceID, self.SRSCode, self.SRSName, self.SRSDescription, self.SRSLink)


class Specimens(SamplingFeatures):
    __tablename__ = u'specimens'
    __table_args__ = {u'schema': 'odm2'}

    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               primary_key=True)
    SpecimenTypeCV = Column('specimentypecv', ForeignKey(CVSpecimenType.Name), nullable=False, index=True)
    SpecimenMediumCV = Column('specimenmediumcv', ForeignKey(CVMediumType.Name), nullable=False, index=True)
    IsFieldSpecimen = Column('isfieldspecimen', Boolean, nullable=False)

    # SamplingFeatureObj = relationship(SamplingFeatures)
    __mapper_args__ = {
        'polymorphic_identity':'Specimen',
    }

    def __repr__(self):
        return "<Specimens('%s', '%s', '%s',  '%s',)>" \
               % (self.SamplingFeatureID, self.SamplingFeatureCode, self.SpecimenTypeCV,self.SamplingFeatureCode)


class SpatialOffsets(Base):
    __tablename__ = u'spatialoffsets'
    __table_args__ = {u'schema': 'odm2'}

    SpatialOffsetID = Column('spatialoffsetid', Integer, primary_key=True, nullable=False)
    SpatialOffsetTypeCV = Column('spatialoffsettypecv', ForeignKey(CVSpatialOffsetType.Name), nullable=False,
                                 index=True)
    Offset1Value = Column('offset1value', Float(53), nullable=False)
    Offset1UnitID = Column('offset1unitid', Integer, ForeignKey(Units.UnitsID), nullable=False)
    Offset2Value = Column('offset2value', Float(53))
    Offset2UnitID = Column('offset2unitid', Integer, ForeignKey(Units.UnitsID))
    Offset3Value = Column('offset3value', Float(53))
    Offset3UnitID = Column('offset3unitid', Integer, ForeignKey(Units.UnitsID))

    Offset1UnitObj = relationship(Units, primaryjoin='SpatialOffsets.Offset1UnitID == Units.UnitsID')
    Offset2UnitObj = relationship(Units, primaryjoin='SpatialOffsets.Offset2UnitID == Units.UnitsID')
    Offset3UnitObj = relationship(Units, primaryjoin='SpatialOffsets.Offset3UnitID == Units.UnitsID')


class Sites(SamplingFeatures):
    __tablename__ = u'sites'
    __table_args__ = {u'schema': 'odm2'}

    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               primary_key=True)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID),
                                nullable=False)
    SiteTypeCV = Column('sitetypecv', ForeignKey(CVSiteType.Name), nullable=False, index=True)
    Latitude = Column('latitude', Float(53), nullable=False)
    Longitude = Column('longitude', Float(53), nullable=False)

    SpatialReferenceObj = relationship(SpatialReferences)
    # SamplingFeatureObj = relationship(SamplingFeatures)

    __mapper_args__ = {
        'polymorphic_identity':'Site',
    }
    def __repr__(self):
        return "<Sites('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.SamplingFeatureID, self.SpatialReferenceID, self.SiteTypeCV, self.Latitude, self.Longitude,
                  self.SpatialReferenceObj, self.SamplingFeatureCode)


class RelatedFeatures(Base):
    __tablename__ = u'relatedfeatures'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedFeatureID = Column('relatedfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID), nullable=False)
    SpatialOffsetID = Column('spatialoffsetid', ForeignKey(SpatialOffsets.SpatialOffsetID))

    SamplingFeatureObj = relationship(SamplingFeatures,
                                      primaryjoin='RelatedFeatures.SamplingFeatureID == SamplingFeatures.SamplingFeatureID')
    RelatedFeatureObj = relationship(SamplingFeatures,
                                     primaryjoin='RelatedFeatures.RelatedFeatureID == SamplingFeatures.SamplingFeatureID')
    SpatialOffsetObj = relationship(SpatialOffsets)


class SpecimenTaxonomicClassifiers(Base):
    __tablename__ = u'specimentaxonomicclassifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(Specimens.SamplingFeatureID), nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(TaxonomicClassifiers.TaxonomicClassifierID), nullable=False)
    CitationID = Column('citationid', Integer)

    SpecimenObj = relationship(Specimens)
    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)


# ################################################################################
# Simulation
# ################################################################################
class Models(Base):
    __tablename__ = 'models'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ ={u'schema': Schema.getSchema()}

    ModelID = Column('modelid', Integer, primary_key=True, nullable=False)
    ModelCode = Column('modelcode', String(255), nullable=False)
    ModelName = Column('modelname', String(255), nullable=False)
    ModelDescription = Column('modeldescription', String(500))


class RelatedModels(Base):
    __tablename__ = 'relatedmodels'
    __table_args__ = {u'schema': 'odm2'}

    RelatedID = Column('relatedid', Integer, primary_key=True, nullable=False)
    ModelID = Column('modelid', ForeignKey(Models.ModelID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedModelID = Column('relatedmodelid', ForeignKey(Models.ModelID), nullable=False)

    ModelObj = relationship(Models, primaryjoin='RelatedModels.ModelID == Models.ModelID')
    RelatedModelObj = relationship(Models, primaryjoin='RelatedModels.RelatedModelID == Models.ModelID')


class Simulations(Base):
    __tablename__ = 'simulations'
    __table_args__ = {u'schema': 'odm2'}

    SimulationID = Column('simulationid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)
    SimulationName = Column('simulationname', String(255), nullable=False)
    SimulationDescription = Column('simulationdescription', String(500))
    SimulationStartDateTime = Column('simulationstartdatetime', Date, nullable=False)
    SimulationStartDateTimeUTCOffset = Column('simulationstartdatetimeutcoffset', Integer, nullable=False)
    SimulationEndDateTime = Column('simulationenddatetime', Date, nullable=False)
    SimulationEndDateTimeUTCOffset = Column('simulationenddatetimeutcoffset', Integer, nullable=False)
    TimeStepValue = Column('timestepvalue', Float(53), nullable=False)
    TimeStepUnitsID = Column('timestepunitsid', ForeignKey(Units.UnitsID), nullable=False)
    InputDataSetID = Column('inputdatasetid', ForeignKey(DataSets.DataSetID))
    # OutputDataSetID = Column('outputdatasetid', Integer) # What's this ?
    ModelID = Column('modelid', ForeignKey(Models.ModelID), nullable=False)

    Action = relationship(Actions)
    DataSet = relationship(DataSets)
    Model = relationship(Models)
    Unit = relationship(Units)

    def __repr__(self):
        return "<Simulations('%s', '%s', '%s', '%s')>" % \
               (self.SimulationID, self.ActionID, self.SimulationName, self.SimulationStartDateTime)


# Part of the Provenance table, needed here to meet dependancies
class Citations(Base):
    __tablename__ = u'citations'
    __table_args__ = {u'schema': 'odm2'}

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
    __table_args__ = {u'schema': 'odm2'}

    AnnotationID = Column('annotationid', Integer, primary_key=True, nullable=False)
    AnnotationTypeCV = Column('annotationtypecv', ForeignKey(CVAnnotationType.Name), nullable=False, index=True)
    AnnotationCode = Column('annotationcode', String(50))
    AnnotationText = Column('annotationtext', String(500), nullable=False)
    AnnotationDateTime = Column('annotationdatetime', DateTime)
    AnnotationUTCOffset = Column('annotationutcoffset', Integer)
    AnnotationLink = Column('annotationlink', String(255))
    AnnotatorID = Column('annotatorid', ForeignKey(People.PersonID))
    CitationID = Column('citationid', ForeignKey(Citations.CitationID))

    PersonObj = relationship(People)
    CitationObj = relationship(Citations)


class ActionAnnotations(Base):
    __tablename__ = u'actionannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    ActionObj = relationship(Actions)
    AnnotationObj = relationship(Annotations)


class EquipmentAnnotations(Base):
    __tablename__ = u'equipmentannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    EquipmentID = Column('valueid', BigInteger, ForeignKey(Equipment.EquipmentID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    EquipmentObj = relationship(Equipment)


class MethodAnnotations(Base):
    __tablename__ = u'methodannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Methods.MethodID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    MethodObj = relationship(Methods)


class ResultAnnotations(Base):
    __tablename__ = u'resultannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Results.ResultID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)
    BeginDateTime = Column('begindatetime', DateTime, nullable=False)
    EndDateTime = Column('enddatetime', DateTime, nullable=False)

    AnnotationObj = relationship(Annotations)
    ResultObj = relationship(Results)


class SamplingFeatureAnnotations(Base):
    __tablename__ = u'samplingfeatureannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    SamplingFeatureObj = relationship(SamplingFeatures)


# ################################################################################
# Data Quality
# ################################################################################
class DataSetsResults(Base):
    __tablename__ = u'datasetsresults'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    DataSetID = Column('datasetid', ForeignKey(DataSets.DataSetID), nullable=False)
    ResultID = Column('resultid', ForeignKey(Results.ResultID), nullable=False)

    DataSetObj = relationship(DataSets)
    ResultObj = relationship(Results)


class DataQuality(Base):
    __tablename__ = 'dataquality'
    __table_args__ = {u'schema': 'odm2'}

    DataQualityID = Column('dataqualityid', Integer, primary_key=True, nullable=False)
    DataQualityTypeCV = Column('dataqualitytypecv', ForeignKey(CVDataQualityType.Name), nullable=False,
                               index=True)
    DataQualityCode = Column('dataqualitycode', String(255), nullable=False)
    DataQualityValue = Column('dataqualityvalue', Float(53))
    DataQualityValueUnitsID = Column('dataqualityvalueunitsid', ForeignKey(Units.UnitsID))
    DataQualityDescription = Column('dataqualitydescription', String(500))
    DataQualityLink = Column('dataqualitylink', String(255))

    UnitObj = relationship(Units)


class ReferenceMaterials(Base):
    __tablename__ = 'referencematerials'
    __table_args__ = {u'schema': 'odm2'}

    ReferenceMaterialID = Column('referencematerialid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialMediumCV = Column('referencematerialmediumcv', ForeignKey(CVReferenceMaterialMedium.Name),
                                       nullable=False, index=True)
    ReferenceMaterialOrganizationID = Column('referencematerialoranizationid',
                                             ForeignKey(Organizations.OrganizationID), nullable=False)
    ReferenceMaterialCode = Column('referencematerialcode', String(50), nullable=False)
    ReferenceMaterialLotCode = Column('referencemateriallotcode', String(255))
    ReferenceMaterialPurchaseDate = Column('referencematerialpurchasedate', DateTime)
    ReferenceMaterialExpirationDate = Column('referencematerialexpirationdate', DateTime)
    ReferenceMaterialCertificateLink = Column('referencematerialcertificatelink', String(255))
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID))

    OrganizationObj = relationship(Organizations)
    SamplingFeatureObj = relationship(SamplingFeatures)


class CalibrationStandards(Base):
    __tablename__ = u'calibrationstandards'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', Integer, ForeignKey(Actions.ActionID), nullable=False)
    ReferenceMaterialID = Column('referencematerialid', Integer, ForeignKey(ReferenceMaterials.ReferenceMaterialID),
                                 nullable=False)

    ActionObj = relationship(Actions)
    ReferenceMaterialObj = relationship(ReferenceMaterials)

# ResultNormalizationValues = Table(
# u'resultnormalizationvalues', Base.metadata,
# Column(u'resultid', ForeignKey(Results.ResultID), primary_key=True),
#     Column(u'normalizedbyreferencematerialvalueid', ForeignKey('odm2.referencematerialvalues.referencematerialvalueid'),
#            nullable=False),
#     schema='odm2'
# )


class ReferenceMaterialValues(Base):
    __tablename__ = u'referencematerialvalues'
    __table_args__ = {u'schema': 'odm2'}

    ReferenceMaterialValueID = Column('referencematerialvalueid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialID = Column('referencematerialid', ForeignKey(ReferenceMaterials.ReferenceMaterialID),
                                 nullable=False)
    ReferenceMaterialValue = Column('referencematerialvalue', Float(53), nullable=False)
    ReferenceMaterialAccuracy = Column('referencematerialaccuracy', Float(53))
    VariableID = Column('variableid', ForeignKey(Variables.VariableID), nullable=False)
    UnitsID = Column('unitsid', ForeignKey(Units.UnitsID), nullable=False)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)

    CitationObj = relationship(Citations)
    ReferenceMaterialObj = relationship(ReferenceMaterials)
    UnitObj = relationship(Units)
    VariableObj = relationship(Variables)
    #ResultsObj = relationship(Results, secondary=ResultNormalizationValues)


class ResultNormalizationValues(Base):
    __tablename__ = 'resultnormalizationvalues'
    ResultID = Column(u'resultid', ForeignKey(Results.ResultID), primary_key=True)
    ReferenceMaterialValueID = Column(u'referencematerialvalueid',
                                      ForeignKey(ReferenceMaterialValues.ReferenceMaterialValueID),
                                      nullable=False)

    ResultsObj = relationship(Results)
    ReferenceMaterialValueObj = relationship(ReferenceMaterialValues)


class ResultsDataQuality(Base):
    __tablename__ = 'resultsdataquality'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Results.ResultID), nullable=False)
    DataQualityID = Column('dataqualityid', ForeignKey(DataQuality.DataQualityID), nullable=False)

    DataQualityObj = relationship(DataQuality)
    ResultObj = relationship(Results)


# ################################################################################
# Extension Properties
# ################################################################################
class ExtensionProperties(Base):
    __tablename__ = u'extensionproperties'
    __table_args__ = {u'schema': 'odm2'}

    PropertyID = Column('propertyid', Integer, primary_key=True, nullable=False)
    PropertyName = Column('propertyname', String(255), nullable=False)
    PropertyDescription = Column('propertydescription', String(500))
    PropertyDataTypeCV = Column('propertydatatypecv', ForeignKey(CVPropertyDataType.Name), nullable=False,
                                index=True)
    PropertyUnitsID = Column('propertyunitsid', ForeignKey(Units.UnitsID))

    UnitObj = relationship(Units)


class ActionExtensionPropertyValues(Base):
    __tablename__ = u'actionextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ActionID = Column('actionid', ForeignKey(Actions.ActionID), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ActionObj = relationship(Actions)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class CitationExtensionPropertyValues(Base):
    __tablename__ = u'citationextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    CitationObj = relationship(Citations)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class MethodExtensionPropertyValues(Base):
    __tablename__ = u'methodextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Methods.MethodID), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    MethodObj = relationship(Methods)
    ExtensionPropertyObj = relationship(ExtensionProperties)


class ResultExtensionPropertyValues(Base):
    __tablename__ = u'resultextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Results.ResultID), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    ResultObj = relationship(Results)


class SamplingFeatureExtensionPropertyValues(Base):
    __tablename__ = u'samplingfeatureextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    SamplingFeatureObj = relationship(SamplingFeatures)


class VariableExtensionPropertyValues(Base):
    __tablename__ = u'variableextensionpropertyvalues'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    VariableID = Column('variableid', ForeignKey(Variables.VariableID), nullable=False)
    PropertyID = Column('propertyid', ForeignKey(ExtensionProperties.PropertyID), nullable=False)
    PropertyValue = Column('propertyvalue', String(255), nullable=False)

    ExtensionPropertyObj = relationship(ExtensionProperties)
    VariableObj = relationship(Variables)


# ################################################################################
# Extension Identifiers
# ################################################################################
class ExternalIdentifierSystems(Base):
    __tablename__ = u'externalidentifiersystems'
    __table_args__ = {u'schema': 'odm2'}

    ExternalIdentifierSystemID = Column('externalidentifiersystemid', Integer, primary_key=True, nullable=False)
    ExternalIdentifierSystemName = Column('externalidentifiersystemname', String(255), nullable=False)
    IdentifierSystemOrganizationID = Column('identifiersystemorganizationid',
                                            ForeignKey(Organizations.OrganizationID), nullable=False)
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
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    CitationExternalIdentifier = Column('citationexternaldentifier', String(255), nullable=False)
    CitationExternalIdentifierURI = Column('citationexternaldentifieruri', String(255))

    CitationObj = relationship(Citations)
    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)


class MethodExternalIdentifiers(Base):
    __tablename__ = u'methodexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Methods.MethodID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)

    MethodExternalIdentifier = Column('methodexternalidentifier', String(255), nullable=False)
    MethodExternalIdentifierURI = Column('methodexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    MethodObj = relationship(Methods)


class PersonExternalIdentifiers(Base):
    __tablename__ = u'personexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    PersonID = Column('personid', ForeignKey(People.PersonID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    PersonExternalIdentifier = Column('personexternalidentifier', String(255), nullable=False)
    PersonExternalIdentifierURI = Column('personexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    PersonObj = relationship(People)


class ReferenceMaterialExternalIdentifiers(Base):
    __tablename__ = u'referencematerialexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ReferenceMaterialID = Column(ForeignKey(ReferenceMaterials.ReferenceMaterialID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    ReferenceMaterialExternalIdentifier = Column('referencematerialexternalidentifier', String(255), nullable=False)
    ReferenceMaterialExternalIdentifierURI = Column('referencematerialexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    ReferenceMaterialObj = relationship(ReferenceMaterials)


class SamplingFeatureExternalIdentifiers(Base):
    __tablename__ = u'samplingfeatureexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SamplingFeatureID = Column('samplingfeatureid', ForeignKey(SamplingFeatures.SamplingFeatureID),
                               nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    SamplingFeatureExternalIdentifier = Column('samplingfeatureexternalidentifier', String(255), nullable=False)
    SamplingFeatureExternalIdentifierURI = Column('samplingfeatureexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    SamplingFeatureObj = relationship(SamplingFeatures)


class SpatialReferenceExternalIdentifiers(Base):
    __tablename__ = u'spatialreferenceexternaledentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID),
                                nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    SpatialReferenceExternalIdentifier = Column('spatialreferenceexternalidentifier', String(255), nullable=False)
    SpatialReferenceExternalIdentifierURI = Column('spatialreferenceexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    SpatialReferenceObj = relationship(SpatialReferences)


class TaxonomicClassifierExternalIdentifiers(Base):
    __tablename__ = u'taxonomicclassifierexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    TaxonomicClassifierID = Column('taxonomicclassifierid',
                                   ForeignKey(TaxonomicClassifiers.TaxonomicClassifierID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
                                        nullable=False)
    TaxonomicClassifierExternalIdentifier = Column('taxonomicclassifierexternalidentifier', String(255), nullable=False)
    TaxonomicClassifierExternalIdentifierURI = Column('taxonomicclassifierexternalidentifieruri', String(255))

    ExternalIdentifierSystemObj = relationship(ExternalIdentifierSystems)
    TaxonomicClassifierObj = relationship(TaxonomicClassifiers)


class VariableExternalIdentifiers(Base):
    __tablename__ = u'variableexternalidentifiers'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    VariableID = Column('variableid', ForeignKey(Variables.VariableID), nullable=False)
    ExternalIdentifierSystemID = Column('externalidentifiersystemid',
                                        ForeignKey(ExternalIdentifierSystems.ExternalIdentifierSystemID),
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
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)
    PersonID = Column('personid', ForeignKey(People.PersonID), nullable=False)
    AuthorOrder = Column('authororder', Integer, nullable=False)

    CitationObj = relationship(Citations, primaryjoin='AuthorLists.CitationID == Citations.CitationID')
    PersonObj = relationship(People, primaryjoin='AuthorLists.PersonID == People.PersonID')

    def __repr__(self):
        return "<AuthorLists('%s', '%s', '%s', '%s', '%s', '%s')>" \
               % (self.BridgeID, self.CitationID, self.PersonID, self.AuthorOrder, self.CitationObj, self.PersonObj)


class DataSetCitations(Base):
    __tablename__ = u'datasetcitations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    DataSetID = Column('datasetid', ForeignKey(DataSets.DataSetID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)

    CitationObj = relationship(Citations)
    DataSetObj = relationship(DataSets)


# ResultDerivationEquations = Table(
#     u'resultderivationequations', Base.metadata,
#     Column(u'resultid', ForeignKey(Results.ResultID), primary_key=True),
#     Column(u'derivationequationid', ForeignKey('odm2.derivationequations.derivationequationid'), nullable=False),
#     schema='odm2'
# )


class DerivationEquations(Base):
    __tablename__ = u'derivationequations'
    __table_args__ = {u'schema': 'odm2'}

    DerivationEquationID = Column('derivationequationid', Integer, primary_key=True, nullable=False)
    DerivationEquation = Column('derivationequation', String(255), nullable=False)

    #ResultsObj = relationship(Results, secondary=ResultDerivationEquations)


class ResultDerivationEquations(Base):
    __tablename__ = u'resultderivationequations'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column(u'resultid', ForeignKey(Results.ResultID), primary_key=True)
    DerivationEquationID = Column(u'derivationequationid', ForeignKey(DerivationEquations.DerivationEquationID),
                                  nullable=False)

    ResultsObj = relationship(Results)
    DerivationEquationsObj = relationship(DerivationEquations)


class MethodCitations(Base):
    __tablename__ = u'methodcitations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    MethodID = Column('methodid', ForeignKey(Methods.MethodID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)
    CitationObj = relationship(Citations)
    MethodObj = relationship(Methods)


# from odm2.Annotations.converter import Annotation
class RelatedAnnotations(Base):
    __tablename__ = u'relatedannotations'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedAnnotationID = Column('relatedannotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations, primaryjoin='RelatedAnnotations.AnnotationID == Annotations.AnnotationID')
    RelatedAnnotationObj = relationship(Annotations,
                                        primaryjoin='RelatedAnnotations.RelatedAnnotationID == Annotations.AnnotationID')


class RelatedCitations(Base):
    __tablename__ = u'relatedcitations'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    CitationID = Column('citationid', ForeignKey(Citations.CitationID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedCitationID = Column('relatedcitationid', ForeignKey(Citations.CitationID), nullable=False)

    CitationObj = relationship(Citations, primaryjoin='RelatedCitations.CitationID == Citations.CitationID')
    RelatedCitationObj = relationship(Citations,
                                      primaryjoin='RelatedCitations.RelatedCitationID == Citations.CitationID')


class RelatedDataSets(Base):
    __tablename__ = u'relateddatasets'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    DataSetID = Column('datasetid', ForeignKey(DataSets.DataSetID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedDataSetID = Column('relateddatasetid', ForeignKey(DataSets.DataSetID), nullable=False)
    VersionCode = Column('versioncode', String(50))

    DataSetObj = relationship(DataSets, primaryjoin='RelatedDataSets.DataSetID == DataSets.DataSetID')
    RelatedDataSetObj = relationship(DataSets, primaryjoin='RelatedDataSets.RelatedDataSetID == DataSets.DataSetID')


class RelatedResults(Base):
    __tablename__ = u'relatedresults'
    __table_args__ = {u'schema': 'odm2'}

    RelationID = Column('relationid', Integer, primary_key=True, nullable=False)
    ResultID = Column('resultid', ForeignKey(Results.ResultID), nullable=False)
    RelationshipTypeCV = Column('relationshiptypecv', ForeignKey(CVRelationshipType.Name), nullable=False,
                                index=True)
    RelatedResultID = Column('relatedresultid', ForeignKey(Results.ResultID), nullable=False)
    VersionCode = Column('versioncode', String(50))
    RelatedResultSequenceNumber = Column('relatedresultsequencenumber', Integer)

    ResultObj = relationship(Results, primaryjoin='RelatedResults.RelatedResultID == Results.ResultID')
    RelatedResultObj = relationship(Results, primaryjoin='RelatedResults.ResultID == Results.ResultID')


# ################################################################################
# Results
# ################################################################################
class PointCoverageResults(Results):
    __tablename__ = u'pointcoverageresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedXSpacing = Column('intendedxspacing', Float(53))
    IntendedXSpacingUnitsID = Column('intendedxspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedYSpacing = Column('intendedyspacing', Float(53))
    IntendedYSpacingUnitsID = Column('intendedyspacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', Integer, nullable=False)

    IntendedXSpacingUnitsObj = relationship(Units, primaryjoin='PointCoverageResults.IntendedXSpacingUnitsID == Units.UnitsID')
    IntendedYSpacingUnitsObj = relationship(Units, primaryjoin='PointCoverageResults.IntendedYSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    ZLocationUnitsObj = relationship(Units, primaryjoin='PointCoverageResults.ZLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='PointCoverageResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Point coverage'}


class ProfileResults(Results):
    __tablename__ = u'profileresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedZSpacing = Column('intendedzspacing', Float(53))
    IntendedZSpacingUnitsID = Column('intendedzspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    IntendedTimeSpacingUnitsObj = relationship(Units, primaryjoin='ProfileResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    IntendedZSpacingUnitsObj = relationship(Units, primaryjoin='ProfileResults.IntendedZSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XLocationUnitsObj = relationship(Units, primaryjoin='ProfileResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='ProfileResults.YLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='ProfileResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Profile Coverage'}


class CategoricalResults(Results):
    __tablename__ = u'categoricalresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', Integer, ForeignKey(Units.UnitsID))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', Integer, ForeignKey(Units.UnitsID))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', Integer, ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)

    SpatialReferenceObj = relationship(SpatialReferences)
    XLocationUnitsObj = relationship(Units, primaryjoin='CategoricalResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='CategoricalResults.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='CategoricalResults.ZLocationUnitsID == Units.UnitsID')

    # ResultObj = relationship(Results, primaryjoin='CategoricalResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Category coverage'}


class TransectResults(Results):
    __tablename__ = u'transectresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedTransectSpacing = Column('intendedtransectspacing', Float(53))
    IntendedTransectSpacingUnitsID = Column('intendedtransectspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    IntendedTimeSpacingUnitsObj = relationship(Units, primaryjoin='TransectResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    IntendedTransectSpacingUnitsObj = relationship(Units, primaryjoin='TransectResults.IntendedTransectSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    ZLocationUnitsObj = relationship(Units, primaryjoin='TransectResults.ZLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='TransectResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Transect Coverage'}


class SpectraResults(Results):
    __tablename__ = u'spectraresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedWavelengthSpacing = Column('intendedwavelengthspacing', Float(53))
    IntendedWavelengthSpacingUnitsID = Column('intendedwavelengthspacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    IntendedWavelengthSpacingUnitsObj = relationship(Units, primaryjoin='SpectraResults.IntendedWavelengthSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XLocationUnitsObj = relationship(Units, primaryjoin='SpectraResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='SpectraResults.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='SpectraResults.ZLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='SpectraResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Spectra coverage'}


class TimeSeriesResults(Results):
    __tablename__ = u'timeseriesresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    # ResultObj = relationship(Results)
    IntendedTimeSpacingUnitsObj = relationship(Units,
                                               primaryjoin='TimeSeriesResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    XLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='TimeSeriesResults.ZLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='TimeSeriesResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Time series coverage'}

    # def __repr__(self):
    #     return "<TimeSeriesResults('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % \
    #            ( self.FeatureActionID, self.ProcessingLevelID, self.VariableID,
    #              self.self.XLocation, self.YLocation, self.ResultTypeCV,
    #             self.IntendedTimeSpacing, self.AggregationStatisticCV)


class SectionResults(Results):
    __tablename__ = u'sectionresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedXSpacing = Column('intendedxspacing', Float(53))
    IntendedXSpacingUnitsID = Column('intendedxspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedZSpacing = Column('intendedzspacing', Float(53))
    IntendedZSpacingUnitsID = Column('intendedzspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    IntendedTimeSpacingUnitsObj = relationship(Units, primaryjoin='SectionResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    IntendedXSpacingUnitsObj = relationship(Units, primaryjoin='SectionResults.IntendedXSpacingUnitsID == Units.UnitsID')
    IntendedZSpacingUnitsObj = relationship(Units, primaryjoin='SectionResults.IntendedZSpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    YLocationUnitsObj = relationship(Units, primaryjoin='SectionResults.YLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='SectionResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Section coverage'}


class TrajectoryResults(Results):
    __tablename__ = u'trajectoryresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    IntendedTrajectorySpacing = Column('intendedtrajectoryspacing', Float(53))
    IntendedTrajectorySpacingUnitsID = Column('intendedtrajectoryspacingunitsid', ForeignKey(Units.UnitsID))
    IntendedTimeSpacing = Column('intendedtimespacing', Float(53))
    IntendedTimeSpacingUnitsID = Column('intendedtimespacingunitsid', ForeignKey(Units.UnitsID))
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)

    IntendedTimeSpacingUnitsObj = relationship(Units, primaryjoin='TrajectoryResults.IntendedTimeSpacingUnitsID == Units.UnitsID')
    IntendedTrajectorySpacingUnitsObj = relationship(Units,
                                     primaryjoin='TrajectoryResults.IntendedTrajectorySpacingUnitsID == Units.UnitsID')
    SpatialReferenceObj = relationship(SpatialReferences)
    # ResultObj = relationship(Results, primaryjoin='TrajectoryResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Trajectory coverage'}


class MeasurementResults(Results):
    __tablename__ = u'measurementresults'
    __table_args__ = {u'schema': 'odm2'}

    ResultID = Column('resultid', ForeignKey(Results.ResultID), primary_key=True)
    XLocation = Column('xlocation', Float(53))
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID))
    YLocation = Column('ylocation', Float(53))
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID))
    ZLocation = Column('zlocation', Float(53))
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID))
    SpatialReferenceID = Column('spatialreferenceid', ForeignKey(SpatialReferences.SpatialReferenceID))
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    SpatialReferenceObj = relationship(SpatialReferences)
    TimeAggregationIntervalUnitsObj = relationship(Units, primaryjoin='MeasurementResults.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XLocationUnitsObj = relationship(Units, primaryjoin='MeasurementResults.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='MeasurementResults.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='MeasurementResults.ZLocationUnitsID == Units.UnitsID')
    # ResultObj = relationship(Results, primaryjoin='MeasurementResults.ResultID == Results.ResultID')
    __mapper_args__ = {'polymorphic_identity':'Measurement'}

    def __repr__(self):
        return "<MeasResults('%s', '%s', '%s', '%s', '%s', '%s', '%s',  '%s')>" % \
               (self.ResultID, self.XLocation, self.YLocation, self.XLocation,
                self.ResultTypeCV, self.XLocationUnitsObj, self.SpatialReferenceObj,
                self.AggregationStatisticCV)


class CategoricalResultValues(Base):
    __tablename__ = u'categoricalresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(CategoricalResults.ResultID), nullable=False)
    DataValue = Column('datavalue', String(255), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)

    ResultObj = relationship(CategoricalResults)


class MeasurementResultValues(Base):
    __tablename__ = u'measurementresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(MeasurementResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)

    ResultObj = relationship(MeasurementResults)

    def __repr__(self):
        return "<MeasValues('%s', '%s', '%s')>" % (self.DataValue, self.ValueDateTime, self.ResultID)


class PointCoverageResultValues(Base):
    __tablename__ = u'pointcoverageresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(PointCoverageResults.ResultID), nullable=False)
    DataValue = Column('datavalue', BigInteger, nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)

    ResultObj = relationship(PointCoverageResults)
    XLocationUnitsObj = relationship(Units, primaryjoin='PointCoverageResultValues.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsobj = relationship(Units, primaryjoin='PointCoverageResultValues.YLocationUnitsID == Units.UnitsID')


class ProfileResultValues(Base):
    __tablename__ = u'profileresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(ProfileResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    ZLocation = Column('zlocation', Float(53), nullable=False)
    ZAggregationInterval = Column('zaggregationinterval', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    ResultObj = relationship(ProfileResults)
    TimeAggregationIntervalUnitsObj = relationship(Units, primaryjoin='ProfileResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='ProfileResultValues.ZLocationUnitsID == Units.UnitsID')


class SectionResultValues(Base):
    __tablename__ = u'sectionresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(SectionResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', BigInteger, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', BigInteger, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XAggregationInterval = Column('xaggregationinterval', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    ZLocation = Column('zlocation', BigInteger, nullable=False)
    ZAggregationInterval = Column('zaggregationinterval', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    ResultObj = relationship(SectionResults)
    TimeAggregationIntervalUnitsObj = relationship(Units, primaryjoin='SectionResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XLocationUnitsObj = relationship(Units, primaryjoin='SectionResultValues.XLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='SectionResultValues.ZLocationUnitsID == Units.UnitsID')


class SpectraResultValues(Base):
    __tablename__ = u'spectraresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(SpectraResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    ExcitationWavelength = Column('excitationwavelength', Float(53), nullable=False)
    EmissionWavelength = Column('emmistionwavelength', Float(53), nullable=False)
    WavelengthUnitsID = Column('wavelengthunitsid', ForeignKey(Units.UnitsID), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    ResultObj = relationship(SpectraResults)
    TimeAggregationIntervalUnitsObj = relationship(Units, primaryjoin='SpectraResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    WavelengthUnitsObj = relationship(Units, primaryjoin='SpectraResultValues.WavelengthUnitsID == Units.UnitsID')


class TimeSeriesResultValues(Base):
    __tablename__ = u'timeseriesresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(TimeSeriesResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    ResultObj = relationship(TimeSeriesResults)
    TimeAggregationIntervalUnitsObj = relationship(Units)

    def get_columns(self):
        return ["ValueID", "ResultID", "DataValue", "ValueDateTime", "ValueDateTimeUTCOffset",
                "CensorCodeCV", "QualityCodeCV", "TimeAggregationInterval", "TimeAggregationIntervalUnitsID"]

    def list_repr(self):
        return [self.ValueID, self.ResultID, self.DataValue, self.ValueDateTime, self.ValueDateTimeUTCOffset,
                self.CensorCodeCV, self.QualityCodeCV, self.TimeAggregationInterval,
                self.TimeAggregationIntervalUnitsID]

    def __repr__(self):
        return "<TimeSeriesResultValues('%s', '%s', '%s')>" % (
            self.DataValue, self.ValueDateTime, self.TimeAggregationInterval)


class TrajectoryResultValues(Base):
    __tablename__ = u'trajectoryresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(TrajectoryResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', Integer, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    ZLocation = Column('zlocation', Float(53), nullable=False)
    ZLocationUnitsID = Column('zlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    TrajectoryDistance = Column('trajectorydistance', Float(53), nullable=False)
    TrajectoryDistanceAggregationInterval = Column('trajectorydistanceaggregationinterval', Float(53), nullable=False)
    TrajectoryDistanceUnitsID = Column('trajectorydistanceunitsid', Integer, nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID),
                                            nullable=False)

    ResultObj = relationship(TrajectoryResults)
    TimeAggregationIntervalUnitsObj = relationship(Units,
                               primaryjoin='TrajectoryResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XLocationUnitsObj = relationship(Units, primaryjoin='TrajectoryResultValues.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='TrajectoryResultValues.YLocationUnitsID == Units.UnitsID')
    ZLocationUnitsObj = relationship(Units, primaryjoin='TrajectoryResultValues.ZLocationUnitsID == Units.UnitsID')


class TransectResultValues(Base):
    __tablename__ = u'transectresultvalues'
    __table_args__ = {u'schema': 'odm2'}

    ValueID = Column('valueid', BigIntegerType, primary_key=True)
    ResultID = Column('resultid', ForeignKey(TransectResults.ResultID), nullable=False)
    DataValue = Column('datavalue', Float(53), nullable=False)
    ValueDateTime = Column('valuedatetime', DateTime, nullable=False)
    ValueDateTimeUTCOffset = Column('valuedatetimeutcoffset', DateTime, nullable=False)
    XLocation = Column('xlocation', Float(53), nullable=False)
    XLocationUnitsID = Column('xlocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    YLocation = Column('ylocation', Float(53), nullable=False)
    YLocationUnitsID = Column('ylocationunitsid', ForeignKey(Units.UnitsID), nullable=False)
    TransectDistance = Column('transectdistance', Float(53), nullable=False)
    TransectDistanceAggregationInterval = Column('transectdistanceaggregationinterval', Float(53), nullable=False)
    TransectDistanceUnitsID = Column('transectdistanceunitsid', ForeignKey(Units.UnitsID), nullable=False)
    CensorCodeCV = Column('censorcodecv', ForeignKey(CVCensorCode.Name), nullable=False, index=True)
    QualityCodeCV = Column('qualitycodecv', ForeignKey(CVQualityCode.Name), nullable=False, index=True)
    AggregationStatisticCV = Column('aggregationstatisticcv', ForeignKey(CVAggregationStatistic.Name),
                                    nullable=False, index=True)
    TimeAggregationInterval = Column('timeaggregationinterval', Float(53), nullable=False)
    TimeAggregationIntervalUnitsID = Column('timeaggregationintervalunitsid', ForeignKey(Units.UnitsID), nullable=False)

    ResultObj = relationship(TransectResults)
    TimeAggregationIntervalUnitsObj = relationship(Units,
                                                   primaryjoin='TransectResultValues.TimeAggregationIntervalUnitsID == Units.UnitsID')
    XLocationUnitsObj = relationship(Units, primaryjoin='TransectResultValues.XLocationUnitsID == Units.UnitsID')
    YLocationUnitsObj = relationship(Units, primaryjoin='TransectResultValues.YLocationUnitsID == Units.UnitsID')
    TransectDistanceUnitsObj = relationship(Units, primaryjoin='TransectResultValues.TransectDistanceUnitsID == Units.UnitsID')


class CategoricalResultValueAnnotations(Base):
    __tablename__ = u'categoricalresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(CategoricalResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(CategoricalResultValues)


class MeasurementResultValueAnnotations(Base):
    __tablename__ = u'measurementresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(MeasurementResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(MeasurementResultValues)


class PointCoverageResultValueAnnotations(Base):
    __tablename__ = u'pointcoverageresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(PointCoverageResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(PointCoverageResultValues)


class ProfileResultValueAnnotations(Base):
    __tablename__ = u'profileresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(ProfileResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(ProfileResultValues)


class SectionResultValueAnnotations(Base):
    __tablename__ = u'sectionResultValueAnnotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(SectionResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(SectionResultValues)


class SpectraResultValueAnnotations(Base):
    __tablename__ = u'spectraresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(SpectraResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(SpectraResultValues)


class TimeSeriesResultValueAnnotations(Base):
    __tablename__ = u'timeseriesresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(TimeSeriesResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(TimeSeriesResultValues)


class TrajectoryResultValueAnnotations(Base):
    __tablename__ = u'trajectoryresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(TrajectoryResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(TrajectoryResultValues)


class TransectResultValueAnnotations(Base):
    __tablename__ = u'transectresultvalueannotations'
    __table_args__ = {u'schema': 'odm2'}

    BridgeID = Column('bridgeid', Integer, primary_key=True, nullable=False)
    ValueID = Column('valueid', BigInteger, ForeignKey(TransectResultValues.ValueID), nullable=False)
    AnnotationID = Column('annotationid', ForeignKey(Annotations.AnnotationID), nullable=False)

    AnnotationObj = relationship(Annotations)
    ValueObj = relationship(TransectResultValues)


def _changeSchema(schema):
    import inspect
    import sys
    #get a list of all of the classes in the module
    clsmembers = inspect.getmembers(sys.modules[__name__],
                                    lambda member: inspect.isclass(member) and member.__module__ == __name__)

    for name, Tbl in clsmembers:
        import sqlalchemy.ext.declarative.api as api

        if isinstance(Tbl, api.DeclarativeMeta):
            #check to see if the schema is already set correctly
            if Tbl.__table__.schema ==schema:
                return
            Tbl.__table__.schema = schema
            Tbl.__table_args__["schema"]=schema


def _getSchema(engine):
    from sqlalchemy.engine import reflection

    insp = reflection.Inspector.from_engine(engine)
    for name in insp.get_schema_names():
        if 'odm2' == name.lower():
            return name

    return insp.default_schema_name


def setSchema(engine):

    s = _getSchema(engine)
    # if s is None:
    #     s = ''
    _changeSchema(s)


