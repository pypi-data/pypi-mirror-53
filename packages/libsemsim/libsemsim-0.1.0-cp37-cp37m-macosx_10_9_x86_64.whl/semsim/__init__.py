import os

os.environ['PATH'] = '/cygdrive/c/Users/phantom/Documents/devel/install/libsemsim-cyg64/python3.7/site-packages/semsim:'+os.environ['PATH']

from .semsim import *

__version__ = '0.1.0'
