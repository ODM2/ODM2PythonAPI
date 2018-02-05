from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api.services.readService import ReadODM2 as newClass

warnings.warn('The module odm2api.ODM2.services.readService will be depricated. '
              'Please use odm2api.services.readService instead.',
              FutureWarning, stacklevel=2)


__author__ = 'sreeder'


def ReadODM2(*args, **kwargs):
    warnings.warn('The class odm2api.ODM2.services.readService.ReadODM2 will be depricated. '
                  'Please use odm2api.services.readService.ReadODM2 instead.',
                  FutureWarning, stacklevel=2)
    return newClass(*args, **kwargs)
