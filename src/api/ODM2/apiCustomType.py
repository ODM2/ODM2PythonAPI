
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
        val = "%s(%s)"%(element.name, compiler.process(element.clauses.clauses[0]))
        print  "postgresql Alter Table %s " % val
        #ST_AsText("\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")
        return val

    @compiles(cls)#, 'mysql')
    def compile_function(element, compiler, **kw):

        val="%s(%s)"%(element.name.lower().split('_')[1], compiler.process(element.clauses.clauses[0]))
        print  "mysql Alter Table %s" % val
        #astext("`ODM2`.`SamplingFeatures`.`FeatureGeometry`")
        #ST_astext()
        return val

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        print  "sqlite Alter Table %s Alter column %s"% (dir(element), dir(compiler))
        return "%s(%s)"%(element.name, compiler.process(element.clauses.clauses[0]))
        #return ST_AsText(samplingfeatures.featuregeometry)


    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        print  "mssql Alter Table %s Alter column %s"%(dir(element), dir(compiler))
        #[SamplingFeatures_1].[FeatureGeometry].STAsText()
        return "%s.%s()" % ( compiler.process(element.clauses.clauses[0]), element.name.replace('_', '') )

    return cls



# function to save to the database
def saves_as_bound(cls):

    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):

        print  "postgresql Save Table %s Alter column %s" % (dir(element), dir(compiler))
        return "%s(%s)"%("ST_GeomFromText", "\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")

    @compiles(cls)#, 'mysql')
    def compile_function(element, compiler, **kw):
        # print element.schema
        # print element.name
        # print element.clauses
        # print element.params

        print  "mysql Save Table %s Alter column %s" % (dir(element), dir(compiler))
        #return None
        return "%s(%s)"%("ST_GeomFromText", "`SamplingFeatures`.`FeatureGeometry`")

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        print  "sqlite Save Table %s Alter column %s"% (dir(element), dir(compiler))
        return "%s(%s)" % ("STGeomFromText", "samplingfeatures.featuregeometry")

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        print  "mssql Save Table %s Alter column %s"%(dir(element), dir(compiler))
        return "Geometry::%s(%s, 0)"%("STGeomFromText", "samplingfeature.featuregeometry")

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









