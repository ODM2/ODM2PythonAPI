from __future__ import (absolute_import, division, print_function)

import os
import sys
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

from odm2api.ODM2.models import setSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SessionFactory():
    def __init__(self, connection_string, echo=True, version=2.0):

        if 'sqlite' in connection_string:
            self.engine = create_engine(connection_string,  encoding='utf-8', echo=echo, pool_recycle=100)
            self.test_engine = self.engine
        elif 'mssql' in connection_string:
            self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=100)
            self.test_engine = create_engine(connection_string, encoding='utf-8',
                                             echo=echo, connect_args={'timeout': 1})
        elif 'postgresql' in connection_string or 'mysql' in connection_string:
            self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=100)
            self.test_engine = create_engine(connection_string, encoding='utf-8', echo=echo,
                                             max_overflow=0, connect_args={'connect_timeout': 1})

        # Create session maker.
        self.Session = scoped_session(sessionmaker(bind=self.engine, autoflush=True))
        self.test_Session = scoped_session(sessionmaker(bind=self.test_engine))
        setSchema(self.engine)
        self.version = version

    def getSession(self):
        return self.Session()

    def __repr__(self):
        return '<SessionFactory("%s")>' % self.engine


class dbconnection():
    def __init__(self, debug=False):
        self.debug = debug
        self.version = -1
        self._connection_format = '%s+%s://%s:%s@%s/%s'
        self._connection_format_nopassword = '%s+%s://%s@%s/%s'

    @classmethod
    def createConnection(self, engine, address, db=None, user=None, password=None, dbtype=2.0, echo=False):

        if engine == 'sqlite':
            connection_string = engine + ':///' + address
            return self.createConnectionFromString(connection_string, dbtype, echo)
        else:
            connection_string = dbconnection.__buildConnectionString(
                dbconnection(), engine, address, db, user, password
            )
            if self.isValidConnection(connection_string, dbtype):
                return self.createConnectionFromString(connection_string, dbtype, echo)
            else:
                return None

    @classmethod
    def createConnectionFromString(self, conn_string, dbtype=2.0, echo=False):
        s = SessionFactory(conn_string, echo=echo, version=dbtype)
        return s

    @classmethod
    def isValidConnection(self, connection_string=None,  dbtype=2.0):
        # refreshDB(dbtype)
        if dbtype == 2.0:
            if self.testEngine(connection_string):
                return True
            else:
                return False
        else:
            if self.testEngine1_1(connection_string):
                return True
            else:
                return False

    @classmethod
    def testEngine(self, connection_string, echo=False):
        s = SessionFactory(connection_string, echo=echo, version=2.0)
        try:
            setSchema(s.test_engine)
            # s.test_Session().query(Variable2.VariableCode).limit(1).first()
            s.test_Session().execute('Select 1')
        except Exception as e:
            print('Connection was unsuccessful {}'.format(e.message))
            return False
        finally:
            dbconnection.closeConnection(s.test_Session)
        return True

    @classmethod
    def testEngine1_1(self, connection_string, echo=False):
        s = SessionFactory(connection_string, echo=echo, version=1.1)
        try:
            # s.test_Session().query(ODM.Variable.code).limit(1).first()
            s.test_Session().execute('Select 1')

        except Exception as e:
            print('Connection was unsuccessful {}'.format(e.message))
            return False
        finally:
            dbconnection.closeConnection(s.test_Session)
        return True

    @classmethod
    def buildConnectionString(self, engine, address, db, user, password):
        return dbconnection.__buildConnectionString(dbconnection(), engine, address, db, user, password)

    @classmethod
    def closeConnection(self, session):
        session.remove()

    # ####################
    # private variables
    # # ###################

    def __buildConnectionString(self, engine=None, address=None, db=None, user=None, password=None):

        if engine == 'mssql' and sys.platform != 'win32':
            driver = 'pyodbc'
            quoted = quote_plus('DRIVER={FreeTDS};DSN=%s;UID=%s;PWD=%s;' % (address, user, password))
            conn_string = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
        elif engine == 'sqlite':
            driver = 'sqlite'
            conn_string = '%s:///%s' % (driver, address)
        else:
            if engine == 'mssql':
                driver = 'pyodbc'
                conn = '%s+%s://%s:%s@%s/%s?driver=SQL+Server'
                if 'sqlncli11.dll' in os.listdir('C:\\Windows\\System32'):
                    conn = '%s+%s://%s:%s@%s/%s?driver=SQL+Server+Native+Client+11.0'
                self._connection_format = conn
                conn_string = self._connection_format % (engine, driver, user, password, address, db)
            else:
                if engine == 'mysql':
                    driver = 'pymysql'
                elif engine == 'postgresql':
                    driver = 'psycopg2'
                else:
                    driver = 'None'
                conn_string = self.constringBuilder(engine, address, db, user, password, driver)

        return conn_string

    def constringBuilder(self, engine=None, address=None, db=None, user=None, password=None, driver=None):
        if password is None or not password:
            conn_string = self._connection_format_nopassword % (
                engine, driver, user, address, db)
        else:
            conn_string = self._connection_format % (
                engine, driver, user, password, address, db)
        return conn_string
