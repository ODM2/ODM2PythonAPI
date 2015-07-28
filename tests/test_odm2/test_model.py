__author__ = 'stephanie'
# run with 'py.test -s test_example.py'
from src.api.ODMconnection import dbconnection
from src.api.ODM2.models import *



############
# Fixtures #
############
class TestODM2:

    def setup(self):
        session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
        self.session = session_factory.getSession()

    def test_cvelevationdatum(self):
        q= self.session.query(CVElevationDatum)
        results= q.all()
        #print results
        assert len(results) > 0

    def test_cvsamplingfeatuergeotype(self):
        q=self.session.query(CVSamplingFeatureGeoType)
        results = q.all()
        #print results
        assert len(results) > 0

    def test_cvsamplingfeaturetype(self):
        q = self.session.query(CVSamplingFeatureType)
        results = q.all()
        #print results
        assert len(results) > 0

    def test_sampling_feature(self):
        q = self.session.query(SamplingFeatures)
        results = q.all()
        '''
        for r in results:
            print r
            print r.SamplingFeatureGeotypeCV
            print r.FeatureGeometry
        #print results
        '''
        assert len(results) > 0

