from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api.services.deleteService import DeleteODM2 as newClass

warnings.warn('The module odm2api.ODM2.services.deleteService will be deprecated. '
              'Please use odm2api.services.deleteService instead.',
              FutureWarning, stacklevel=2)


__author__ = 'jmeline'

# Annotations


def DeleteODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.DeleteODM2 will be deprecated. '
                  'Please use odm2api.services.readService.DeleteODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
