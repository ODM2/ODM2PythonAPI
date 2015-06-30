
from sqlalchemy.dialects.mssql.base import MSSQLCompiler
from sqlalchemy.dialects.mysql.mysqldb import MySQLCompiler
from sqlalchemy import func
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import UserDefinedType
from sqlalchemy.ext.compiler import compiles


from geoalchemy2 import Geometry as GeometryBase


def compiles_as_bound(cls):
    @compiles(cls)
    def compile_function(element, compiler, **kw):

        if isinstance(compiler, MSSQLCompiler):
            #return "%s.%s(%s)" % (element.clauses.clauses[0], element.name,", ".join([compiler.process(e) for e in element.clauses.clauses[1:]]))
            val = "%s.%s(%s)" % ("[SamplingFeatures_1].[FeatureGeometry]", element.name,", ".join([compiler.process(e) for e in element.clauses.clauses[1:]]))

        elif isinstance(compiler, MySQLCompiler):
            val= "%s(%s)"%("astext", "`ODM2`.`SamplingFeatures`.`FeatureGeometry`")

        else:
            val= "%s(%s)"%("ST_AsText", "\"ODM2\".\"SamplingFeatures\".\"FeatureGeometry\"")

    @compiles(cls, 'postgresql')
    def compile_function(element, compiler, **kw):
        print  "postgresql Alter Table %s Alter column %s"%element.table.name, element.column.name
        return None

    @compiles(cls, 'mysql')
    def compile_function(element, compiler, **kw):
        print  "mysql Alter Table %s Alter column %s"%element.table.name, element.column.name
        return None

    @compiles(cls, 'sqlite')
    def compile_function(element, compiler, **kw):
        print  "sqlite Alter Table %s Alter column %s"%element.table.name, element.column.name
        return None

    @compiles(cls, 'mssql')
    def compile_function(element, compiler, **kw):
        print  "mssql Alter Table %s Alter column %s"%element.table.name, element.column.name
        return None

    return cls

@compiles_as_bound
class ST_AsText(FunctionElement):
    name = 'STAsText'



@compiles_as_bound
class ST_AsBinary(FunctionElement):
    name = 'STAsBinary'



class Geometry(GeometryBase):

    def column_expression(self, col):

        value = ST_AsText(col, type_=self)

        if value is  None:
            value = func.ST_AsText(col, type_=self)
        return value









