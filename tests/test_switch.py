__author__ = 'stephanie'

from api.ODMconnection import dbconnection
from api.versionSwitcher import ODM, refreshDB

class TestSwitch:

    def setup(self):
        session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
        refreshDB(2.0)
        self.session = session_factory.getSession()

    def test_switch(self):
        s=self.session.query(ODM.Site).all()

        print type(ODM.Site)
        #print ODM.Series.get(self.session)
        print s

