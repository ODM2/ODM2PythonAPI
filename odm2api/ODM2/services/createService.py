from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api.services import CreateODM2 as newClass

warnings.warn('The module odm2api.ODM2.services.createService will be deprecated. '
              'Please use odm2api.services.createService instead.',
              FutureWarning, stacklevel=2)


__author__ = 'sreeder'


def CreateODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.CreateODM2 will be deprecated. '
                  'Please use odm2api.services.readService.CreateODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
