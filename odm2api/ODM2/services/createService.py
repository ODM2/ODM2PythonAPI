from __future__ import (absolute_import, division, print_function)
import warnings
warnings.warn('The module odm2api.ODM2.services.createService will be depricated. '
              'Please use odm2api.services.createService instead.',
              FutureWarning, stacklevel=2)

from odm2api.services import CreateODM2 as newClass

__author__ = 'sreeder'


def CreateODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.CreateODM2 will be depricated. '
                  'Please use odm2api.services.readService.CreateODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
