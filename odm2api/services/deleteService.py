from __future__ import (absolute_import, division, print_function)

from odm2api import serviceBase
from odm2api.models import TimeSeriesResultValues


__author__ = 'jmeline'

# Annotations


class DeleteODM2(serviceBase):

    def remove(self, obj):
        self._session.delete(obj)

# CV
# Core
# Data Quality
# Equipment
# Extension Properties
# External Identifiers
# Lab Analyses
# Provenance
# Annotations
# Sampling Features
# Sensors
# Result Values

    def deleteTSRValues(self, ids=None, startdate=None, dates=None):

        q = self._session.query(TimeSeriesResultValues)
        if ids:
            q = q.filter(TimeSeriesResultValues.ResultID.in_(ids))
        if startdate:
            # delete all values on or after the startdate.
            q = q.filter(TimeSeriesResultValues.ValueDateTime >= startdate)
        if dates:
            q = q.filter(TimeSeriesResultValues.ValueDateTime.in_(dates))
        numvals = q.count()
        q.delete(False)
        return numvals
