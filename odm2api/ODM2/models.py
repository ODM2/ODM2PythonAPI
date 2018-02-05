from __future__ import (absolute_import, division, print_function)

import warnings

from odm2api.models import *  # noqa

warnings.warn('The module odm2api.ODM2.models will be deprecated. '
              'Please use odm2api.models instead.',
              FutureWarning, stacklevel=2)
