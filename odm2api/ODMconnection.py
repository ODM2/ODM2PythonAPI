
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from odm2api.ODM2.models import Variables as Variable2, setSchema

from odm2api.ODM1_1_1.services import ODM#, refreshDB
import urllib
import sys
import os


# LIBSPATIALITE_PATH = './libspatialite.so.5.1.0'

class SessionFactory():
    def __init__(self, connection_string, echo=True, version = 2.0):
        if 'sqlite' in connection_string:
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
        self.version = -1
        self._connection_format = "%s+%s://%s:%s@%s/%s"
        self._connection_format_nopassword = "%s+%s://%s@%s/%s"

    @classmethod
    def createConnection(self, engine, address, db=None, user=None, password=None, dbtype = 2.0, echo=False):

        if engine == 'sqlite':
            connection_string = engine +':///'+address
            return self.createConnectionFromString(connection_string, dbtype, echo)

        else:
            connection_string = dbconnection.__buildConnectionString(dbconnection(), engine, address, db, user, password)
            if self.isValidConnection(connection_string, dbtype):
                return self.createConnectionFromString(connection_string, dbtype, echo)
            else :
                return None
        # if self.testConnection(connection_string):


    @classmethod
    def createConnectionFromString(self, conn_string, dbtype= 2.0, echo = False):
        s = SessionFactory(conn_string, echo=echo, version=dbtype)
        setSchema(s.engine)
        return s

    @classmethod
    def isValidConnection(self, connection_string=None,  dbtype=2.0):
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
        s = SessionFactory(connection_string, echo=echo, version = 2.0)
        try:
            setSchema(s.test_engine)
            s.test_Session().query(Variable2.VariableCode).limit(1).first()

        except Exception as e:
            print("Connection was unsuccessful ", e.message)
            return False
        return True

    @classmethod
    def testEngine1_1(self, connection_string, echo = False ):
        s = SessionFactory(connection_string, echo=echo, version = 1.1)
        try:
            # s.ms_test_Session().query(Variable1).limit(1).first()
            s.test_Session().query(ODM.Variable.code).limit(1).first()

        except Exception as e:
            print("Connection was unsuccessful ", e.message)
            return False
        return True

    @classmethod
    def buildConnectionString(self, engine, address, db, user, password):
        return dbconnection.__buildConnectionString(dbconnection(), engine, address, db, user, password)




    ## ###################
    # private variables
    ## ###################


    def __buildConnectionString(self, engine=None, address=None, db=None, user=None, password=None):

        if engine == 'mssql' and sys.platform != 'win32':
            driver = "pyodbc"
            quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;' % (address, user, password))
            # quoted = urllib.quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;DATABASE=%s' %
            #                            (conn_dict['address'], conn_dict['user'], conn_dict['password'],conn_dict['db'],
            #                             ))
            conn_string = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
        elif engine=='sqlite':
            driver = 'sqlite'
            conn_string = "%s:///%s" % (driver, address)
        else:
            if engine == 'mssql':
                driver = "pyodbc"
                conn = "%s+%s://%s:%s@%s/%s?driver=SQL+Server"
                if "sqlncli11.dll" in os.listdir("C:\\Windows\\System32"):
                    conn = "%s+%s://%s:%s@%s/%s?driver=SQL+Server+Native+Client+11.0"
                self._connection_format = conn
                conn_string = self._connection_format % (engine, driver, user, password, address, db)
            else:
                if engine == 'mysql':
                    driver = "pymysql"
                elif engine == 'postgresql':
                    driver = "psycopg2"
                else:
                    driver = "None"
                conn_string = self.constringBuilder(engine, address, db, user, password, driver)

        return conn_string

    def constringBuilder(self, engine=None, address=None, db=None, user=None, password=None, driver= None):
        if password is None or not password:
            conn_string = self._connection_format_nopassword % (
                engine, driver, user, address, db)
        else:
            conn_string = self._connection_format % (
                engine, driver, user, password, address, db)
        return conn_string
