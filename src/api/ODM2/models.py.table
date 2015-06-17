from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
import sqlalchemy.orm as orm


# Should not be importing anything from a specific dialect
# from sqlalchemy.dialects.mssql.base import BIT

from apiCustomType import Geometry


from base import modelBase


'''
class CVElevationDatum(Base):
    __tablename__ = 'cv_elevationdatum'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.name, self.Definition, self.Category)
'''
cvelevationdatum_table = Table('cv_elevationdatum', modelBase.metadata,
    Column('term', String(255), nullable=False),
    Column('name', String(255), primary_key=True),
    Column('definition', String(1000)),
    Column('category', String(255)),
    Column('sourcevocabularyuri', String(255))
                               )
class CVElevationDatum(object):
    def __repr__(self):
        return "<CVElevationDatum('%s', '%s', '%s', '%s')>" % (self.term, self.name, self.definition, self.category)

orm.mapper(CVElevationDatum, cvelevationdatum_table)

'''
class CVSamplingFeatureGeoType(Base):
    __tablename__ = 'cv_samplingfeaturegeotype'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.Name, self.Definition, self.Category)
'''
cvamplingfeaturegeo_table = Table('cv_samplingfeaturegeotype', modelBase.metadata,
    Column('term', String(255), nullable=False),
    Column('name', String(255), primary_key=True),
    Column('definition', String(1000)),
    Column('category', String(255)),
    Column('sourcevocabularyuri', String(255))
                               )
class CVSamplingFeatureGeoType(object):
    def __repr__(self):
        return "<CVSamplingFeatureGeoType('%s', '%s', '%s', '%s')>" % (self.term, self.name, self.definition, self.category)

orm.mapper(CVSamplingFeatureGeoType, cvamplingfeaturegeo_table)

'''
class CVSamplingFeatureType(Base):
    __tablename__ = 'cv_samplingfeaturetype'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ = {u'schema': Schema.getSchema()}

    Term = Column('term', String(255), nullable=False)
    Name = Column('name', String(255), primary_key=True)
    Definition = Column('definition', String(1000))
    Category = Column('category', String(255))
    SourceVocabularyURI = Column('sourcevocabularyuri', String(255))

    def __repr__(self):
        return "<CV('%s', '%s', '%s', '%s')>" % (self.Term, self.Name, self.Definition, self.Category)
'''

cvamplingfeature_table = Table('cv_samplingfeaturetype', modelBase.metadata,
    Column('term', String(255), nullable=False),
    Column('name', String(255), primary_key=True),
    Column('definition', String(1000)),
    Column('category', String(255)),
    Column('sourcevocabularyuri', String(255))
                               )
class CVSamplingFeatureType(object):
    def __repr__(self):
        return "<CVSamplingFeatureType('%s', '%s', '%s', '%s')>" % (self.term, self.name, self.definition, self.category)

orm.mapper(CVSamplingFeatureType, cvamplingfeature_table)



'''
class SamplingFeatures(Base):
    __tablename__ = u'samplingfeatures'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ = {u'schema': Schema.getSchema()}

    SamplingFeatureID = Column('samplingfeatureid', Integer, primary_key=True, nullable=False)
    SamplingFeatureUUID = Column('samplingfeatureuuid', String(36), nullable=False)
    SamplingFeatureTypeCV = Column('samplingfeaturetypecv', ForeignKey('odm2.cv_samplingfeaturetype.name'),
                                   nullable=False, index=True)
    SamplingFeatureCode = Column('samplingfeaturecode', String(50), nullable=False)
    SamplingFeatureName = Column('samplingfeaturename', String(255))
    SamplingFeatureDescription = Column('samplingfeaturedescription', String(500))
    SamplingFeatureGeotypeCV = Column('samplingfeaturegeotypecv', ForeignKey('odm2.cv_samplingfeaturegeotype.name'),
                                      index=True)
    Elevation_m = Column('elevation_m', Float(53))
    ElevationDatumCV = Column('elevationdatumcv', ForeignKey('odm2.cv_elevationdatum.name'), index=True)
    FeatureGeometry = Column('featuregeometry', Geometry)

    def __repr__(self):
        return "<SamplingFeatures('%s', '%s', '%s', '%s')>" % (
            self.SamplingFeatureCode, self.SamplingFeatureName, self.SamplingFeatureDescription,
            self.Elevation_m)  # self.FeatureGeometry)
'''
sf_table = Table('samplingfeatures', modelBase.metadata,
                 Column('samplingfeatureid', Integer, primary_key=True, nullable=False),
    # Column('samplingfeatureuuid', String(36), nullable=False),
    Column('samplingfeaturetypecv', ForeignKey('cv_samplingfeaturetype.name'),
                                   nullable=False, index=True),
    Column('samplingfeaturecode', String(50), nullable=False),
    Column('samplingfeaturename', String(255)),
    Column('samplingfeaturedescription', String(500)),
    Column('samplingfeaturegeotypecv', ForeignKey('cv_samplingfeaturegeotype.name'),
                                      index=True),
    Column('elevation_m', Float(53)),
    Column('elevationdatumcv', ForeignKey('cv_elevationdatum.name'), index=True),
    Column('featuregeometry', Geometry)
)

class SamplingFeatures(object):
    def __repr__(self):
        return "<SamplingFeatures('%s', '%s', '%s', '%s', '%s')>" % (
            self.samplingfeaturecode, self.samplingfeaturename, self.samplingfeaturedescription,
            self.elevation_m, self.featuregeometry)

    def __init__(self):
        pass
# meta.mapper(ActivityDetail, activity_detail_table, properties = {
#    'activity':orm.relation ( Activity, backref=orm.backref('activity_detail'))
#    })

orm.mapper(SamplingFeatures, sf_table, properties={'cv_elevationdatum': orm.relation(CVElevationDatum, backref=orm.backref('cv_elevationdatum')),
                                                     'cv_samplingfeaturegeotype': orm.relation(CVSamplingFeatureGeoType, backref=orm.backref('cv_samplingfeaturegeotype')),
                                                     'cv_samplingfeaturetype': orm.relation(CVSamplingFeatureType, backref=orm.backref('cv_samplingfeaturetype'))
                                                   })
from sqlalchemy.ext.declarative import declarative_base
Base= declarative_base()
class Variables(Base):
    __tablename__ = u'variables'
    __table_args__ = {u'schema': 'odm2'}  # __table_args__ = {u'schema': Schema.getSchema()}

    VariableID = Column('variableid', Integer, primary_key=True, nullable=False)
    VariableTypeCV = Column('variabletypecv', ForeignKey('odm2.cv_variabletype.name'), nullable=False, index=True)
    VariableCode = Column('variablecode', String(50), nullable=False)
    VariableNameCV = Column('variablenamecv', ForeignKey('odm2.cv_variablename.name'), nullable=False, index=True)
    VariableDefinition = Column('variabledefinition', String(500))
    SpeciationCV = Column('speciationcv', ForeignKey('odm2.cv_speciation.name'), index=True)
    NoDataValue = Column('nodatavalue', Float(asdecimal=True), nullable=False)

    def __repr__(self):
        return "<Variables('%s', '%s', '%s')>" % (self.VariableID, self.VariableCode, self.VariableNameCV)