import sys

if sys.version_info.major == 2:
    from yaml2 import *
else:
    from .yaml3 import *
