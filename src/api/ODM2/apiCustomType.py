from sqlalchemy import func
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles


from geoalchemy2 import Geometry as GeometryBase

# function to pull from the database
def compiles_as_bound(cls):

    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):
        val = "%s(%s)"%(element.name, compiler.process(element.clauses.clauses[0]))
        #ST_AsText("\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")
        return val

    @compiles(cls)#, 'mysql')
    def compile_function(element, compiler, **kw):
        val="%s(%s)"%(element.name.lower().split('_')[1], compiler.process(element.clauses.clauses[0]))
        #astext("`ODM2`.`SamplingFeatures`.`FeatureGeometry`")
        #ST_astext()
        return val

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        return "%s(%s)"%(element.name.split('_')[-1], compiler.process(element.clauses.clauses[0]))
        #return ST_AsText(samplingfeatures.featuregeometry)

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        #[SamplingFeatures_1].[FeatureGeometry].STAsText()
        return "%s.%s()" % (compiler.process(element.clauses.clauses[0]), element.name.replace('_', '') )

    return cls



# function to save to the database
def saves_as_bound(cls):

    @compiles(cls)
    def compile_function(element, compiler, **kw):
        return element

    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):
        #print "postgresql Save : %s" % element.__str__()
        return "%s(%s)"%(element.name, "'POINT(30 10)'")

    @compiles(cls, 'mysql')
    def compile_function(element, compiler, **kw):
        name= element.name.split('_')[-1]

        # GeomFromText("POINT(30 10)")
        # GeomFromText(:featuregeometry)

        val = "%s(%s)"%(name, element.clauses.clauses[0])
        return val

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        name= element.name.split('_')[-1]
        #return "%s(%s)" % (element.name.replace('_', ''), "'POINT (30 10)'")

        return "%s(%s)"%(name, "'POINT(30 10)'")

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        #return "Geometry::%s(%s, 0)"%(element.name.replace('_', ''), "'POINT (30 10)'")
        name = "Geometry::%s" % element.name.replace('_', '')
        return "%s(%s,0)"%(name, "'POINT(30 10)'")



    return cls



@saves_as_bound
class ST_GeomFromText(FunctionElement):
    name = "ST_GeomFromText"

@compiles_as_bound
class ST_AsText(FunctionElement):
    name = 'ST_AsText'

@compiles_as_bound
class ST_AsBinary(FunctionElement):
    name = 'ST_AsBinary'

from sqlalchemy import String, type_coerce
class Geometry(GeometryBase):

    def column_expression(self, col):
        value = ST_AsText(col, type_=self)
        if value is None:
            value = func.ST_AsText(col, type_=self)
        return value

    def bind_expression(self, bindvalue):

        #mysql, sqlite
        val = func.GeomFromText(bindvalue, type_=self)

        #postgresql
        #val = func.ST_GeomFromText(bindvalue, type_=self)
        #mssql
        if val is None:
            val = ST_GeomFromText(bindvalue, type_=self)
        return val








