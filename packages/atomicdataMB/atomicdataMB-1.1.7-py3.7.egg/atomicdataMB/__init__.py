from .g_values import RadPresConst, gValue
from .photolossrates import PhotoRate
from .initialize_atomicdata import initialize_atomicdata
from .atomicmass import atomicmass
from .database_connect import database_connect


name = 'atomicdataMB'
__author__ = 'Matthew Burger'
__email__ = 'mburger@stsci.edu'
__version__ = '1.1.7'

initialize_atomicdata()