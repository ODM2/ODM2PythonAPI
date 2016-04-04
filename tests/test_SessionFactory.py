__author__ = 'valentine'
from odm2api.ODMconnection import SessionFactory
from odm2api.ODM2.models import *
import pytest
from sqlalchemy.engine import reflection

# assumes that pytest is being run from ODM2PythonAPI director
# [name, driver, connectionstring ]
dbs_readonly = [
 #   ['mysql', 'localhost', 'odm2', 'ODM', 'odm'],
    ['mysql@Localhost/odm2', 'mysql', 'mysql+pymysql://root:@localhost/odm2'],
   [' mysql + mysqldb:', 'mysql', 'mysql+mysqldb://root@localhost/odm2'],
                     #'mysql+pymysql://ODM:odm@127.0.0.1/odm2'
     ['postgresql_marchantariats_none', 'postgresql', 'postgresql+psycopg2://postgres:None@localhost/marchantariats', 'marchantariats', 'postgres',  None],
    ['postgresql_marchantariats_empty', 'postgresql', 'postgresql+psycopg2://postgres@localhost/marchantariats', 'marchantariats', 'postgres',  None],
    #'postgresql+psycopg2://postgres:None@localhost/marchantariats'

     ["mssql_pyodbc_azure",   "mssql",   "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BFreeTDS%7D%3BDSN%3Dnrb8xkgxaj.database.windows.net%3BUID%3Dweb%3BPWD%3D1Forgetit%21%3B"   ,  'odm2', 'web', '1Forgetit!'],
    ["mssql_pyodbc2_azure", "mssql",
     "mssql+pyodbc:///?odbc_connect={DRIVER=FreeTDS;SERVER=nrb8xkgxaj.database.windows.net;UID=web@nrb8xkgxaj;PWD=1Forgetit!;DATABASE=odm2}",
     'odm2', 'web', '1Forgetit!'],
    ["mssql_pyodbc3_azure", "mssql",
     "mssql+pyodbc:///?odbc_connect={DRIVER=FreeTDS;SERVER=nrb8xkgxaj.database.windows.net;UID=web;PWD=1Forgetit!;DATABASE=odm2}",
     'odm2', 'web', '1Forgetit!'],
    #'mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BFreeTDS%7D%3BDSN%3Dnrb8xkgxaj.database.windows.net%3BUID%3Dweb%3BPWD%3D1Forgetit%21%3B'
    ["mssql_pyodbc_kyle",   "mssql",
     "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BFreeTDS%7D%3BDSN%3Dkyle.ucsd.edu%3BUID%3Dweb%3BPWD%3Dweb%21%3B",
     'odm2', 'web', '1Forgetit!'],
    ["mssql_pyodbc2",   "mssql",
     "mssql+pyodbc:///?odbc_connect={DRIVER=FreeTDS;SERVER=moonstone.ucsd.edu;UID=web;PWD=web;DATABASE=odm2}",
     'odm2', 'web', '1Forgetit!'],
    ["pymssql_azre",   "mssql",
     "mssql+pymssql://web@nrb8xkgxaj:1Forgetit!@kyle?charset=utf8",
     'odm2', 'web', '1Forgetit!'],
    ["pymssql_moonstone",   "mssql",
     "mssql+pymssql://webservice:webservice@moonstone?charset=utf8",
     'odm2', 'web', '1Forgetit!'],
    #    ["mssql",   "localhost",                        'odm2', 'odm', 'odm'],
 #   ["sqlite", "./tests/spatialite/odm2_test.sqlite", None, None, None],
    ["sqlite_wof", "sqlite","sqlite:///./tests/spatialite/wof2odm/ODM2.sqlite", None,      None,   None]
    #'sqlite:///./tests/spatialite/wof2odm/ODM2.sqlite'
]
dbs_test = [
    ["sqlite_test","sqlite" "./tests/spatialite/odm2_test.sqlite", None, None, None]

]
class aSessionFactory:
    def __init__(self, request):
        #session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
        db = request.param
        print ("dbtype", db[0], db[1] )
        #session_factory = dbconnection.createConnection(db[0],db[1],db[2],db[3],db[4], echo=True)
        session_factory = SessionFactory(db[2])
        setSchema(session_factory.engine)
        assert session_factory is not None, ("failed to create a session for ", db[0], db[1])
#        assert session_factory.engine is not None, ("failed: session has no engine ", db[0], db[1])
#
 #       insp = reflection.Inspector.from_engine(session_factory.engine)
#        tables = insp.get_table_names()

        self.session = session_factory.test_Session()


#
#              params=["sqlite+pysqlite:///../../ODM2PythonAPI/tests/spatialite/odm2_test.sqlite", "mail.python.org"])
@pytest.fixture(scope="session", params = dbs_readonly)
def setup(request):
    return aSessionFactory(request)


#connect to all 4 database types( mssql, mysql, postgresql, sqlite, mssql on mac)
def test_connection(setup):

    q= setup.session.query(CVElevationDatum)
    results= q.all()
    #print results
    assert len(results) > 0



