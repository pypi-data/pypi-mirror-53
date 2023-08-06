from distutils.version import LooseVersion

import cms

DJANGO_CMS_VERSION = LooseVersion(cms.__version__)

DJANGO_CMS_35 = DJANGO_CMS_VERSION >= LooseVersion("3.5")
