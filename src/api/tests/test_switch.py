__author__ = 'stephanie'

from src.api.ODMconnection import dbconnection
from src.api.versionSwitcher import Series

class TestSwitch:

    def setup(self):
        session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
        self.session = session_factory.getSession()

    def test_switch(self):
        s=self.session.query(Series).all()
        print "a;ldksfj;aldkhfj;akhdfjl;ka;lkdjsf;lakjdsf;lakjdsf;lakjsdf;lkajsdf;lkajdf;lkjadsl;fkja;dkfjla;lsdkjf;al"
        print type(Series)
        print Series.get(self.session)
        print s

