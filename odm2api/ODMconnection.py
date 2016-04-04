
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .ODM2.models import Variables as Variable2, setSchema
#from .versionSwitcher import ODM, refreshDB #import Variable as Variable1
from .ODM1_1_1.services import ODM#, refreshDB
import urllib
import sys
import os


# LIBSPATIALITE_PATH = './libspatialite.so.5.1.0'

class SessionFactory():
    def __init__(self, connection_string, echo=True, version = 1.1):
        if 'sqlite' in connection_string:
            # from sqlite3 import dbapi2 as sqlite
            # put the spatialite dll on the path. If one had pyspatialite installed thn
            # this would not be required... but trying to get that on a windows machine
            # was way too hard to bother
            # dirDLLspatialite = 'C:/bin'
            # os.environ['PATH'] = dirDLLspatialite + ';' + os.environ['PATH']

            # #engine = create_engine('sqlite:///D:\\temp\\test_1.db', module=sqlite, echo=False)
            # engine = create_engine(connection_string, module=sqlite, echo=False)

            # this enables the extension on each connection
            # @event.listens_for(engine, "connect")
            # def connect(dbapi_connection, connection_rec):
            #     dbapi_connection.enable_load_extension(True)
            #     dbapi_connection.execute("SELECT load_extension('libspatialite-4.dll')")

            #from pysqlite2 import dbapi2 as sqlite
            #import pyspatialite.dpabi as sqlite
            # self.engine = create_engine(connection_string, model = sqlite ,encoding='utf-8', echo=echo)

            # @event.listens_for(self.engine, "connect")
            # def connect(dbapi_connection, connection_rec):
            #         dbapi_connection.enable_load_extension(True)
            #         dbapi_connection.execute("SELECT load_extension('{0}');".format("mod_spatialite"))

            # self.engine.execute("SELECT InitSpatialMetaData();")#
            # self.engine.connect().connection.enable_load_extension(True)
            # self.engine.execute("SELECT load_extension('mod_spatialite');")#
            self.engine = create_engine(connection_string,  encoding='utf-8', echo=echo)
            self.test_engine = self.engine

        elif 'mssql' in connection_string:
              import pyodbc
              self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600)
              self.test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, connect_args={'timeout': 1})
        elif 'postgresql' in connection_string or 'mysql' in connection_string:
            self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, pool_timeout=5, pool_size=20, max_overflow=0)
            self.test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, pool_timeout=5, max_overflow=0, connect_args={'connect_timeout': 1})

        # Create session maker
        self.Session = sessionmaker(bind=self.engine)
        self.test_Session = sessionmaker(bind=self.test_engine)
        self.version=version

    def getSession(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)


class dbconnection():
    def __init__(self, debug=False):
        self.debug = debug
        self._connections = []
        self.version = 0
        self._connection_format = "%s+%s://%s:%s@%s/%s"
        self._connection_format_nopassword = "%s+%s://%s@%s/%s"

    @classmethod
    def createConnection(self, engine, address, db=None, user=None, password=None, dbtype = 2.0, echo=False):

        if engine == 'sqlite':
            connection_string = engine +':///'+address
            s = SessionFactory(connection_string, echo = echo, version= dbtype)
            setSchema(s.engine)
            return s

        else:
            connection_string = dbconnection.buildConnDict(dbconnection(), engine, address, db, user, password)
            if self.isValidConnection(connection_string, dbtype):
                s= SessionFactory(connection_string, echo = echo, version= dbtype)
                setSchema(s.engine)
                return s
            else :
                return None
        # if self.testConnection(connection_string):

    @classmethod
    def isValidConnection(self, connection_string, dbtype=2.0):
        #refreshDB(dbtype)

        if dbtype == 2.0:
            if self.testEngine(connection_string):
                # print "sucess"
               return True
            else:
                return False
        else:
            if self.testEngine1_1(connection_string):
                # print "sucess"
                return True
            else:
                return False

    @classmethod
    def testEngine(self, connection_string, echo = False ):
        s = SessionFactory(connection_string, echo=echo)
        try:
            setSchema(s.test_engine)
            s.test_Session().query(Variable2.VariableCode).limit(1).first()

        except Exception as e:
            print "Connection was unsuccessful ", e.message
            return False
        return True

    @classmethod
    def testEngine1_1(self, connection_string, echo = False ):
        s = SessionFactory(connection_string, echo=echo)
        try:
            # s.ms_test_Session().query(Variable1).limit(1).first()
            s.test_Session().query(ODM.Variable.code).limit(1).first()

        except Exception as e:
            print "Connection was unsuccessful ", e.message
            return False
        return True

    def buildConnDict(self, engine, address, db, user, password):
        line_dict = {}
        line_dict['engine'] = engine
        line_dict['user'] = user
        line_dict['password'] = password
        line_dict['address'] = address
        line_dict['db'] = db
        self._connections.append(line_dict)
        self._current_connection = self._connections[-1]
        return self.__buildConnectionString(line_dict)

    def getConnections(self):
        return self._connections

    def getCurrentConnection(self):
        return self._current_connection

    def addConnection(self, conn_dict):
        """conn_dict must be a dictionary with keys: engine, user, password, address, db"""

        # remove earlier connections that are identical to this one
        self.deleteConnection(conn_dict)

        self._connections.append(conn_dict)
        self._current_connection = self._connections[-1]


    def deleteConnection(self, conn_dict):
        self._connections[:] = [x for x in self._connections if x != conn_dict]

    ## ###################
    # private variables
    ## ###################

    # def __buildConnectionString(self, conn_dict):
    #     driver = ""
    #     if conn_dict['engine'] == 'mssql':
    #         driver = "pyodbc"
    #     elif conn_dict['engine'] == 'mysql':
    #         driver = "pymysql"
    #     elif conn_dict['engine'] == 'postgresql':
    #         driver = "psycopg2"
    #     else:
    #         driver = "None"
    #
    #     conn_string = self._connection_format % (
    #         conn_dict['engine'], driver, conn_dict['user'], conn_dict['password'], conn_dict['address'],
    #         conn_dict['db'])
    #     # print conn_string
    #     return conn_string

    def __buildConnectionString(self, conn_dict):
        # driver = ""
        # print "****", conn_dict
        if conn_dict['engine'] == 'mssql' and sys.platform != 'win32':
            driver = "pyodbc"
            #'DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;' % (conn_dict['address'], conn_dict['user'], conn_dict['password'])
         #   quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;' % (conn_dict['address'], conn_dict['user'], conn_dict['password']))
            quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;DATABASE=%s' %
                                       (conn_dict['address'], conn_dict['user'], conn_dict['password'],conn_dict['db'],))
            conn_string = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
        else:
            if conn_dict['engine'] == 'mssql':
                driver = "pyodbc"
                #self._connection_format = "%s+%s://%s:%s@%s/%s?driver=SQL+Server+Native+Client+10.0"
                conn = "%s+%s://%s:%s@%s/%s?driver=SQL+Server"
                if "sqlncli11.dll" in os.listdir("C:\\Windows\\System32"):
                    conn = "%s+%s://%s:%s@%s/%s?driver=SQL+Server+Native+Client+11.0"
                self._connection_format = conn
                conn_string = self._connection_format % (
                    conn_dict['engine'], driver, conn_dict['user'], conn_dict['password'], conn_dict['address'],
                    conn_dict['db'])
            elif conn_dict['engine'] == 'mysql':
                driver = "pymysql"
                conn_string = self.constringBuilder(conn_dict, driver)
            elif conn_dict['engine'] == 'postgresql':
                driver = "psycopg2"
                conn_string = self.constringBuilder(conn_dict, driver)
            else:
                driver = "None"
                conn_string = self.constringBuilder(conn_dict, driver)


        # print "******", conn_string
        return conn_string

    def constringBuilder(self, conn_dict, driver):
        if conn_dict['password'] is None or not conn_dict['password']:
            conn_string = self._connection_format_nopassword % (
                conn_dict['engine'], driver, conn_dict['user'], conn_dict['address'],
                conn_dict['db'])
        else:
            conn_string = self._connection_format % (
                conn_dict['engine'], driver, conn_dict['user'], conn_dict['password'], conn_dict['address'],
                conn_dict['db'])
        return conn_string
