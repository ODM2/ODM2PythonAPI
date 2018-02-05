from __future__ import (absolute_import, division, print_function)
import warnings
warnings.warn('The module odm2api.ODM2.services.deleteService will be depricated. '
              'Please use odm2api.services.deleteService instead.',
              FutureWarning, stacklevel=2)

from odm2api.services.deleteService import DeleteODM2 as newClass


__author__ = 'jmeline'

# Annotations


def DeleteODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.DeleteODM2 will be depricated. '
                  'Please use odm2api.services.readService.DeleteODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
