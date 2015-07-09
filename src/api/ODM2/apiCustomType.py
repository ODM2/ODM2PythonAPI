
from sqlalchemy.dialects.mssql.base import MSSQLCompiler
from sqlalchemy.dialects.mysql.mysqldb import MySQLCompiler
from sqlalchemy import func
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles


from geoalchemy2 import Geometry as GeometryBase

# function to pull from the database
def compiles_as_bound(cls):
    '''
    @compiles(cls)
    def compile_function(element, compiler, **kw):

        if isinstance(compiler, MSSQLCompiler):
            #return "%s.%s(%s)" % (element.clauses.clauses[0], element.name,", ".join([compiler.process(e) for e in element.clauses.clauses[1:]]))
            val = "%s.%s(%s)" % ("[SamplingFeatures_1].[FeatureGeometry]", element.name,", ".join([compiler.process(e) for e in element.clauses.clauses[1:]]))

        elif isinstance(compiler, MySQLCompiler):
            val= "%s(%s)"%("astext", "`ODM2`.`SamplingFeatures`.`FeatureGeometry`")

        else:
            val= "%s(%s)"%("ST_AsText", "\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")
    '''
    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):

        print  "postgresql Alter Table %s Alter column %s" % (dir(element), dir(compiler))
        #ST_GeomFromText(compiler)
        return "%s(%s)"%("ST_AsText", "\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")

    @compiles(cls)#, 'mysql')
    def compile_function(element, compiler, **kw):
        # print element.schema
        # print element.name
        # print element.clauses
        # print element.params


        print  "mysql Alter Table %s Alter column %s" % (element.name.lower().replace('_', ''), "find odm2.samplingfeatures.featuregeometry")
        #return None
        return "%s(%s)"%("astext", "`ODM2`.`SamplingFeatures`.`FeatureGeometry`")

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        print  "sqlite Alter Table %s Alter column %s"% (dir(element), dir(compiler))
        return "ST_AsText(samplingfeatures.featuregeometry"
        #return "samplingfeatures.featuregeometry"
        #return None

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        print  "mssql Alter Table %s Alter column %s"%(dir(element), dir(compiler))
        #compiler.STAsText()
        return None

    return cls


# function to save to the database
def saves_as_bound(cls):

    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):

        print  "postgresql Save Table %s Alter column %s" % (dir(element), dir(compiler))
        return "%s(%s)"%("ST_GeomFromText", "\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")

    @compiles(cls)#, 'mysql')
    def compile_function(element, compiler, **kw):
        print element.schema
        print element.name
        print element.clauses
        print element.params


        print  "mysql Save Table %s Alter column %s" % (dir(element), dir(compiler))
        #return None
        return "%s(%s)"%("ST_GeomFromText", "`ODM2`.`SamplingFeatures`.`FeatureGeometry`")

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        print  "sqlite Save Table %s Alter column %s"% (dir(element), dir(compiler))
        return None

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        print  "mssql Save Table %s Alter column %s"%(dir(element), dir(compiler))
        #Geometry::STGeomFromText(compiler, 0)
        return None

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



class Geometry(GeometryBase):

    def column_expression(self, col):

        value = ST_AsText(col, type_=self)

        if value is None:
            value = func.ST_AsText(col, type_=self)
        return value

    def bind_expression(self, bindvalue):
        return ST_GeomFromText(bindvalue, type_=self)









