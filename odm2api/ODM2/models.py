from __future__ import (absolute_import, division, print_function)
import warnings

warnings.warn('The module odm2api.ODM2.models will be depricated. '
              'Please use odm2api.models instead.',
              FutureWarning, stacklevel=2)

from odm2api.models import *
