from .lib import *
from .nlexp import Nlex
from .pack import mod_map

nlex = Nlex()
for name in mod_map.keys():
    nlex.register(name)
del mod_map