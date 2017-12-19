from __future__ import (absolute_import, division, print_function)

from odm2api.ODM2.models import (CVElevationDatum, CVSamplingFeatureGeoType,
                                 CVSamplingFeatureType, SamplingFeatures)

import pytest

from .. import test_connection as testConnection

__author__ = 'stephanie'

dbs = testConnection.dbs_readonly


@pytest.fixture(scope='session', params=dbs)
def setup(request):
    return testConnection.Connection(request)


# Fixtures
def test_cvelevationdatum(setup):
    q = setup.session.query(CVElevationDatum)
    results = q.all()
    assert len(results) > 0


def test_cvsamplingfeatuergeotype(setup):
    q = setup.session.query(CVSamplingFeatureGeoType)
    results = q.all()
    assert len(results) > 0


def test_cvsamplingfeaturetype(setup):
    q = setup.session.query(CVSamplingFeatureType)
    results = q.all()
    assert len(results) > 0


def test_sampling_feature(setup):
    q = setup.session.query(SamplingFeatures)
    results = q.all()
    assert len(results) > 0
