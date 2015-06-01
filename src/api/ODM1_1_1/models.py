'''rom base import Base
from censor_code_cv import CensorCodeCV
from data_type_cv import DataTypeCV
from data_value import DataValue
from general_category_cv import GeneralCategoryCV
from iso_metadata import ISOMetadata
from lab_method import LabMethod
from method import Method
from odm_version import ODMVersion
from offset_type import OffsetType
from qualifier import Qualifier
from quality_control_level import QualityControlLevel
from sample import Sample
from sample_medium_cv import SampleMediumCV
from sample_type_cv import SampleTypeCV
from series import Series
from session_factory import SessionFactory
from site import Site
from site_type_cv import SiteTypeCV
from source import Source
from spatial_reference import SpatialReference
from speciation_cv import SpeciationCV
from topic_category_cv import TopicCategoryCV
from unit import Unit
from value_type_cv import ValueTypeCV
from variable import Variable
from variable_name_cv import VariableNameCV
from vertical_datum_cv import VerticalDatumCV

from series import copy_series
from data_value import copy_data_value

__all__ = [
    'Base',
    'CensorCodeCV',
    'DataTypeCV',
    'DataValue',
    'GeneralCategoryCV',
    'ISOMetadata',
    'LabMethod',
    'Method',
    'ODMVersion',
    'OffsetType',
    'Qualifier',
    'QualityControlLevel',
    'Sample',
    'SampleMediumCV',
    'SampleTypeCV',
    'Series',
    'SessionFactory',
    'Site',
    'SiteTypeCV',
    'Source',
    'SpatialReference',
    'SpeciationCV',
    'TopicCategoryCV',
    'Unit',
    'ValueTypeCV',
    'Variable',
    'VariableNameCV',
    'VerticalDatumCV',
    'MemoryDatabase',
    'copy_series',
    'copy_data_value'
]
'''

from sqlalchemy.ext.declarative import declarative_base


from collections import OrderedDict # Requires Python 2.7 >=
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata


class CensorCodeCV(Base):
    __tablename__ = 'CensorCodeCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<CensorCodeCV('%s', '%s')>" % (self.term, self.definition)


class DataTypeCV(Base):
    __tablename__ = 'DataTypeCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<DataTypeCV('%s', '%s')>" % (self.term, self.definition)


def copy_data_value(from_dv):
    new = DataValue()
    new.data_value = from_dv.data_value
    new.value_accuracy = from_dv.value_accuracy
    new.local_date_time = from_dv.local_date_time
    new.utc_offset = from_dv.utc_offset
    new.date_time_utc = from_dv.date_time_utc
    new.site_id = from_dv.site_id
    new.variable_id = from_dv.variable_id
    new.offset_value = from_dv.offset_value
    new.offset_type_id = from_dv.offset_type_id
    new.censor_code = from_dv.censor_code
    new.qualifier_id = from_dv.qualifier_id
    new.method_id = from_dv.method_id
    new.source_id = from_dv.source_id
    new.sample_id = from_dv.sample_id
    new.derived_from_id = from_dv.derived_from_id
    new.quality_control_level_id = from_dv.quality_control_level_id
    return new


class DataValue(Base):
    __tablename__ = 'DataValues'

    id = Column('ValueID', Integer, primary_key=True)
    data_value = Column('DataValue', Float)
    value_accuracy = Column('ValueAccuracy', Float)
    local_date_time = Column('LocalDateTime', DateTime)
    utc_offset = Column('UTCOffset', Float)
    date_time_utc = Column('DateTimeUTC', DateTime)
    site_id = Column('SiteID', Integer, ForeignKey('Sites.SiteID'), nullable=False)
    variable_id = Column('VariableID', Integer, ForeignKey('Variables.VariableID'), nullable=False)
    offset_value = Column('OffsetValue', Float)
    offset_type_id = Column('OffsetTypeID', Integer, ForeignKey('OffsetTypes.OffsetTypeID'))
    censor_code = Column('CensorCode', String)
    qualifier_id = Column('QualifierID', Integer, ForeignKey('Qualifiers.QualifierID'))
    method_id = Column('MethodID', Integer, ForeignKey('Methods.MethodID'), nullable=False)
    source_id = Column('SourceID', Integer, ForeignKey('Sources.SourceID'), nullable=False)
    sample_id = Column('SampleID', Integer, ForeignKey('Samples.SampleID'))
    derived_from_id = Column('DerivedFromID', Integer)
    quality_control_level_id = Column('QualityControlLevelID', Integer,
                                      ForeignKey('QualityControlLevels.QualityControlLevelID'), nullable=False)

    # relationships
    site = relationship(Site)
    variable = relationship(Variable)
    method = relationship(Method)
    source = relationship(Source)
    quality_control_level = relationship(QualityControlLevel)

    qualifier = relationship(Qualifier)
    offset_type = relationship(OffsetType)
    sample = relationship(Sample)

    def list_repr(self):
        return [self.id, self.data_value, self.value_accuracy, self.local_date_time,
                self.utc_offset, self.date_time_utc, self.site_id, self.variable_id,
                self.offset_value, self.offset_type_id, self.censor_code, self.qualifier_id,
                self.method_id, self.source_id, self.sample_id, self.derived_from_id,
                self.quality_control_level_id]

    def __repr__(self):
        return "<DataValue('%s', '%s', '%s')>" % (self.data_value, self.local_date_time, self.value_accuracy)


class GeneralCategoryCV(Base):
    __tablename__ = 'GeneralCategoryCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<GeneralCategoryCV('%s', '%s')>" % (self.term, self.definition)


class ISOMetadata(Base):
    __tablename__ = 'ISOMetadata'

    id = Column('MetadataID', Integer, primary_key=True)
    topic_category = Column('TopicCategory', String, nullable=False)
    title = Column('Title', String, nullable=False)
    abstract = Column('Abstract', String, nullable=False)
    profile_version = Column('ProfileVersion', String, nullable=False)
    metadata_link = Column('MetadataLink', String)

    def __repr__(self):
        return "<ISOMetadata('%s', '%s', '%s')>" % (self.id, self.topic_category, self.title)


class LabMethod(Base):
    __tablename__ = 'LabMethods'

    id = Column('LabMethodID', Integer, primary_key=True)
    name = Column('LabName', String, nullable=False)
    organization = Column('LabOrganization', String, nullable=False)
    method_name = Column('LabMethodName', String, nullable=False)
    method_description = Column('LabMethodDescription', String, nullable=False)
    method_link = Column('LabMethodLink', String)

    def __repr__(self):
        return "<LabMethod('%s', '%s', '%s', '%s')>" % (self.id, self.name, self.organization, self.method_name)


class Method(Base):
    __tablename__ = 'Methods'

    id = Column('MethodID', Integer, primary_key=True)
    description = Column('MethodDescription', String, nullable=False)
    link = Column('MethodLink', String)

    def __repr__(self):
        return "<Method('%s', '%s', '%s')>" % (self.id, self.description, self.link)


class ODMVersion(Base):
    __tablename__ = 'ODMVersion'

    version_number = Column('VersionNumber', String, primary_key=True)

    def __repr__(self):
        return "<ODMVersion('%s')>" % (self.version_number)


class OffsetType(Base):
    __tablename__ = 'OffsetTypes'

    id = Column('OffsetTypeID', Integer, primary_key=True)
    unit_id = Column('OffsetUnitsID', Integer, ForeignKey('Units.UnitsID'), nullable=False)
    description = Column('OffsetDescription', String)

    # relationships
    unit = relationship(Unit)

    def __repr__(self):
        return "<Unit('%s', '%s', '%s')>" % (self.id, self.unit_id, self.description)


class Qualifier(Base):
    __tablename__ = 'Qualifiers'

    id = Column('QualifierID', Integer, primary_key=True)
    code = Column('QualifierCode', String, nullable=False)
    description = Column('QualifierDescription', String, nullable=False)

    def __repr__(self):
        return "<Qualifier('%s', '%s', '%s')>" % (self.id, self.code, self.description)


class QualityControlLevel(Base):
    __tablename__ = 'QualityControlLevels'

    id = Column('QualityControlLevelID', Integer, primary_key=True)
    code = Column('QualityControlLevelCode', String, nullable=False)
    definition = Column('Definition', String, nullable=False)
    explanation = Column('Explanation', String, nullable=False)

    def __repr__(self):
        return "<QualityControlLevel('%s', '%s', '%s', '%s')>" % (self.id, self.code, self.definition, self.explanation)


class Sample(Base):
    __tablename__ = 'Samples'

    id = Column('SampleID', Integer, primary_key=True)
    type = Column('SampleType', String, nullable=False)
    lab_sample_code = Column('LabSampleCode', String, nullable=False)
    lab_method_id = Column('LabMethodID', Integer, ForeignKey('LabMethods.LabMethodID'), nullable=False)

    # relationships
    lab_method = relationship(LabMethod)

    def __repr__(self):
        return "<Sample('%s', '%s', '%s', '%s')>" % (self.id, self.type, self.lab_sample_code, self.lab_method_id)


class SampleMediumCV(Base):
    __tablename__ = 'SampleMediumCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<SampleMedium('%s', '%s')>" % (self.term, self.definition)


class SampleTypeCV(Base):
    __tablename__ = 'SampleTypeCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<SampleTypeCV('%s', '%s')>" % (self.term, self.definition)


class Site(Base):
    __tablename__ = 'Sites'

    id = Column('SiteID', Integer, primary_key=True)
    code = Column('SiteCode', String)
    name = Column('SiteName', String)
    latitude = Column('Latitude', Float)
    longitude = Column('Longitude', Float)
    lat_long_datum_id = Column('LatLongDatumID', Integer, ForeignKey('SpatialReferences.SpatialReferenceID'))
    elevation_m = Column('Elevation_m', Float)
    vertical_datum_id = Column('VerticalDatum', Integer)
    local_x = Column('LocalX', Float)
    local_y = Column('LocalY', Float)
    local_projection_id = Column('LocalProjectionID', Integer, ForeignKey('SpatialReferences.SpatialReferenceID'))
    pos_accuracy_m = Column('PosAccuracy_m', Float)
    state = Column('State', String)
    county = Column('County', String)
    comments = Column('Comments', String)

    type = Column('SiteType', String)

    # relationships
    spatial_ref = relationship(SpatialReference, primaryjoin=("SpatialReference.id==Site.lat_long_datum_id"))
    local_spatial_ref = relationship(SpatialReference, primaryjoin=("SpatialReference.id==Site.local_projection_id"))

    def __init__(self, site_code, site_name):
        self.code = site_code
        self.name = site_name

    def __repr__(self):
        return "<Site('%s', '%s')>" % (self.code, self.name)


class SiteTypeCV(Base):
    __tablename__ = 'SiteTypeCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<SiteTypeCV('%s', '%s')>" % (self.term, self.definition)


class Source(Base):
    __tablename__ = 'Sources'

    id = Column('SourceID', Integer, primary_key=True)
    organization = Column('Organization', String, nullable=False)
    description = Column('SourceDescription', String, nullable=False)
    link = Column('SourceLink', String)
    contact_name = Column('ContactName', String, nullable=False)
    phone = Column('Phone', String, nullable=False)
    email = Column('Email', String, nullable=False)
    address = Column('Address', String, nullable=False)
    city = Column('City', String, nullable=False)
    state = Column('State', String, nullable=False)
    zip_code = Column('ZipCode', String, nullable=False)
    citation = Column('Citation', String, nullable=False)
    iso_metadata_id = Column('MetadataID', Integer, ForeignKey('ISOMetadata.MetadataID'), nullable=False)

    # relationships
    iso_metadata = relationship(ISOMetadata)

    def __repr__(self):
        return "<Source('%s', '%s', '%s')>" % (self.id, self.organization, self.description)


class SpatialReference(Base):
    __tablename__ = 'SpatialReferences'

    id = Column('SpatialReferenceID', Integer, primary_key=True)
    srs_id = Column('SRSID', Integer)
    srs_name = Column('SRSName', String)
    is_geographic = Column('IsGeographic', Boolean)
    notes = Column('Notes', String)

    def __repr__(self):
        return "<SpatialReference('%s', '%s')>" % (self.id, self.srs_name)


class SpeciationCV(Base):
    __tablename__ = 'SpeciationCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<SpeciationCV('%s', '%s')>" % (self.term, self.definition)


class TopicCategoryCV(Base):
    __tablename__ = 'TopicCategoryCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<TopicCategoryCV('%s', '%s')>" % (self.term, self.definition)


class Unit(Base):
    __tablename__ = 'Units'

    id = Column('UnitsID', Integer, primary_key=True)
    name = Column('UnitsName', String)
    type = Column('UnitsType', String)
    abbreviation = Column('UnitsAbbreviation', String)  # (convert_unicode=True))

    def __repr__(self):
        return "<Unit('%s', '%s', '%s')>" % (self.id, self.name, self.type)


class ValueTypeCV(Base):
    __tablename__ = 'ValueTypeCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<ValueTypeCV('%s', '%s')>" % (self.term, self.definition)


class Variable(Base):
    __tablename__ = 'Variables'

    id = Column('VariableID', Integer, primary_key=True)
    code = Column('VariableCode', String, nullable=False)
    name = Column('VariableName', String, nullable=False)
    speciation = Column('Speciation', String, nullable=False)
    variable_unit_id = Column('VariableUnitsID', Integer, ForeignKey('Units.UnitsID'), nullable=False)
    sample_medium = Column('SampleMedium', String, nullable=False)
    value_type = Column('ValueType', String, nullable=False)
    is_regular = Column('IsRegular', Boolean, nullable=False)
    time_support = Column('TimeSupport', Float, nullable=False)
    time_unit_id = Column('TimeUnitsID', Integer, ForeignKey('Units.UnitsID'), nullable=False)
    data_type = Column('DataType', String, nullable=False)
    general_category = Column('GeneralCategory', String, nullable=False)
    no_data_value = Column('NoDataValue', Float, nullable=False)

    # relationships
    variable_unit = relationship(Unit, primaryjoin=(
    "Unit.id==Variable.variable_unit_id"))  # <-- Uses class attribute names, not table column names
    time_unit = relationship(Unit, primaryjoin=("Unit.id==Variable.time_unit_id"))

    def __repr__(self):
        return "<Variable('%s', '%s', '%s')>" % (self.id, self.code, self.name)


class VariableNameCV(Base):
    __tablename__ = 'VariableNameCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<VariableNameCV('%s', '%s')>" % (self.term, self.definition)


class VerticalDatumCV(Base):
    __tablename__ = 'VerticalDatumCV'

    term = Column('Term', String, primary_key=True)
    definition = Column('Definition', String)

    def __repr__(self):
        return "<VerticalDatumCV('%s', '%s')>" % (self.term, self.definition)


def copy_series(from_series):
    new = Series()
    new.site_id = from_series.site_id
    new.site_code = from_series.site_code
    new.site_name = from_series.site_name
    new.variable_id = from_series.variable_id
    new.variable_code = from_series.variable_code
    new.variable_name = from_series.variable_name
    new.speciation = from_series.speciation
    new.variable_units_id = from_series.variable_units_id
    new.variable_units_name = from_series.variable_units_name
    new.sample_medium = from_series.sample_medium
    new.value_type = from_series.value_type
    new.time_support = from_series.time_support
    new.time_units_id = from_series.time_units_id
    new.time_units_name = from_series.time_units_name
    new.data_type = from_series.data_type
    new.general_category = from_series.general_category
    new.method_id = from_series.method_id
    new.method_description = from_series.method_description
    new.source_id = from_series.source_id
    new.source_description = from_series.source_description
    new.organization = from_series.organization
    new.citation = from_series.citation
    new.quality_control_level_id = from_series.quality_control_level_id
    new.quality_control_level_code = from_series.quality_control_level_code
    new.begin_date_time = from_series.begin_date_time
    new.begin_date_time_utc = from_series.begin_date_time_utc
    new.end_date_time_utc = from_series.end_date_time_utc
    new.value_count = from_series.value_count
    return new


class Series(Base):
    __tablename__ = 'seriescatalog'

    id = Column('SeriesID', Integer, primary_key=True)
    site_id = Column('SiteID', Integer, ForeignKey('Sites.SiteID'), nullable=False)
    site_code = Column('SiteCode', String)
    site_name = Column('SiteName', String)
    variable_id = Column('VariableID', Integer, ForeignKey('Variables.VariableID'), nullable=False)
    variable_code = Column('VariableCode', String)
    variable_name = Column('VariableName', String)
    speciation = Column('Speciation', String)
    variable_units_id = Column('VariableUnitsID', Integer)
    variable_units_name = Column('VariableUnitsName', String)
    sample_medium = Column('SampleMedium', String)
    value_type = Column('ValueType', String)
    time_support = Column('TimeSupport', Float)
    time_units_id = Column('TimeUnitsID', Integer)
    time_units_name = Column('TimeUnitsName', String)
    data_type = Column('DataType', String)
    general_category = Column('GeneralCategory', String)
    method_id = Column('MethodID', Integer, ForeignKey('Methods.MethodID'), nullable=False)
    method_description = Column('MethodDescription', String)
    source_id = Column('SourceID', Integer, ForeignKey('Sources.SourceID'), nullable=False)
    source_description = Column('SourceDescription', String)
    organization = Column('Organization', String)
    citation = Column('Citation', String)
    quality_control_level_id = Column('QualityControlLevelID', Integer,
                                      ForeignKey('QualityControlLevels.QualityControlLevelID'), nullable=False)
    quality_control_level_code = Column('QualityControlLevelCode', String)
    begin_date_time = Column('BeginDateTime', DateTime)
    end_date_time = Column('EndDateTime', DateTime)
    begin_date_time_utc = Column('BeginDateTimeUTC', DateTime)
    end_date_time_utc = Column('EndDateTimeUTC', DateTime)
    value_count = Column('ValueCount', Integer)

    data_values = relationship("DataValue",
                               primaryjoin="and_(DataValue.site_id == Series.site_id, "
                                           "DataValue.variable_id == Series.variable_id, "
                                           "DataValue.method_id == Series.method_id, "
                                           "DataValue.source_id == Series.source_id, "
                                           "DataValue.quality_control_level_id == Series.quality_control_level_id)",
                               foreign_keys="[DataValue.site_id, DataValue.variable_id, DataValue.method_id, DataValue.source_id, DataValue.quality_control_level_id]",
                               order_by="DataValue.local_date_time",
                               backref="series")

    site = relationship(Site)
    variable = relationship(Variable)
    method = relationship(Method)
    source = relationship(Source)
    quality_control_level = relationship(QualityControlLevel)

    # TODO add all to repr
    def __repr__(self):
        return "<Series('%s', '%s', '%s', '%s')>" % (self.id, self.site_name, self.variable_code, self.variable_name)

    def get_table_columns(self):
        return self.__table__.columns.keys()

    def list_repr(self):
        return [self.id, self.site_id, self.site_code, self.site_name, self.variable_id, self.variable_code,
                self.variable_name, self.speciation, self.variable_units_id, self.variable_units_name,
                self.sample_medium, self.value_type, self.time_support, self.time_units_id, self.time_units_name,
                self.data_type, self.general_category, self.method_id, self.method_description,
                self.source_id, self.source_description, self.organization, self.citation,
                self.quality_control_level_id, self.quality_control_level_code, self.begin_date_time,
                self.end_date_time, self.begin_date_time_utc, self.end_date_time_utc, self.value_count]


def returnDict():
    keys = ['SeriesID', 'SiteID', 'SiteCode', 'SiteName', 'VariableID', 'VariableCode', 'VariableName', 'Speciation',
            'VariableUnitsID', 'VariableUnitsName', 'SampleMedium', 'ValueType', 'TimeSupport', 'TimeUnitsID',
            'TimeUnitsName', 'DataType', 'GeneralCategory', 'MethodID', 'MethodDescription', 'SourceID',
            'SourceDescription', 'Organization', 'Citation', 'QualityControlLevelID', 'QualityControlLevelCode',
            'BeginDateTime', 'EndDateTime', 'BeginDateTimeUTC', 'EndDateTimeUTC', 'ValueCount'
            ]
    values = ['id', 'site_id', 'site_code', 'site_name', 'variable_id', 'variable_code', 'variable_name', 'speciation',
              'variable_units_id', 'variable_units_name', 'sample_medium', 'value_type', 'time_support',
              'time_units_id', 'time_units_name', 'data_type', 'general_category', 'method_id', 'method_description',
              'source_id', 'source_description', 'organization', 'citation', 'quality_control_level_id',
              'quality_control_level_code', 'begin_date_time', 'end_date_time', 'begin_date_time_utc',
              'end_date_time_utc', 'value_count'
              ]
    return OrderedDict(zip(keys, values))
