__author__ = 'valentine'
from odm2api.ODMconnection import SessionFactory
from odm2api.ODM2.models import *
import pytest
from sqlalchemy.engine import reflection

# assumes that pytest is being run from ODM2PythonAPI director
dbs_readonly = [
 #   ['mysql', 'localhost', 'odm2', 'ODM', 'odm'],
     ['mysql@Localhost/odm2', 'mysql+pymysql://root@127.0.0.1/odm2'],
     ['postgresql', 'postgresql+psycopg2://postgres:localhost/marchantariats', 'marchantariats', 'postgres',  None],

     ["mssql",   "mssql+pyodbc://nrb8xkgxaj.database.windows.net"   ,  'odm2', 'web', '1Forgetit!'],
#    ["mssql",   "localhost",                        'odm2', 'odm', 'odm'],
 #   ["sqlite", "./tests/spatialite/odm2_test.sqlite", None, None, None],
    ["sqlite", "sqlite:///./tests/spatialite/wof2odm/ODM2.sqlite", None,      None,   None]
]
dbs_test = [
    ["sqlite", "./tests/spatialite/odm2_test.sqlite", None, None, None]

]
class SessionFactory:
    def __init__(self, request):
        #session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
        db = request.param
        print ("dbtype", db[0], db[1] )
        #session_factory = dbconnection.createConnection(db[0],db[1],db[2],db[3],db[4], echo=True)
        session_factory = SessionFactory(connection_string=db[1])
        assert session_factory is not None, ("failed to create a session for ", db[0], db[1])
#        assert session_factory.engine is not None, ("failed: session has no engine ", db[0], db[1])
#
 #       insp = reflection.Inspector.from_engine(session_factory.engine)
#        tables = insp.get_table_names()
        self.session = session_factory
        # self.session = session_factory.test_Session()


#
#              params=["sqlite+pysqlite:///../../ODM2PythonAPI/tests/spatialite/odm2_test.sqlite", "mail.python.org"])
@pytest.fixture(scope="session", params = dbs_readonly)
def setup(request):
    return SessionFactory(request)


#connect to all 4 database types( mssql, mysql, postgresql, sqlite, mssql on mac)
def test_connection(setup):

    q= setup.session.query(CVElevationDatum)
    results= q.all()
    #print results
    assert len(results) > 0



