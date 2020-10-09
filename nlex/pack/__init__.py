import pkgutil
from ..lib.abc import Package
from typing import List

def load_mod() -> List[Package]:
    ret = []
    for mod in pkgutil.iter_modules(__path__):
        mod = mod.module_finder.find_loader(mod.name)[0].load_module()
        for name in dir(mod):
            if name.startswith("__"):
                continue
            obj = getattr( mod, name )
            if isinstance(obj, type) and issubclass(obj, Package) and obj != Package:
                ret.append( obj )
    return ret


mod_map = {
    it.NAME : it for it in load_mod()
}
del load_mod
