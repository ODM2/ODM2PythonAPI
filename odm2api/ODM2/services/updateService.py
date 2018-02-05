from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api.services import UpdateODM2 as newClass

warnings.warn('The module odm2api.ODM2.services.updateService will be depricated. '
              'Please use odm2api.services.updateService instead.',
              FutureWarning, stacklevel=2)

__author__ = 'jmeline'


def UpdateODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.CreateODM2 will be depricated. '
                  'Please use odm2api.services.readService.CreateODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
