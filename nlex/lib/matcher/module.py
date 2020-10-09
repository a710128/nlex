from ..abc import Matcher
from typing import List, Union, AnyStr
from ..result import MatchResult, SingleResult
from ..structure import ModuleStructure, StartStructure

class ModuleMatcher(Matcher):
    NAME : AnyStr = "Module"
    REQ : List[AnyStr] = []

    def __init__(self):
        self._submodules = {}

    def _assign(self, nlex):
        self.__nlex = nlex
        for it in self._submodules.values():
            it._assign(nlex)

    def __init_subclass__(cls, name : Union[None, AnyStr] =None, require : Union[List[AnyStr], AnyStr] = []):
        if name is None:
            name = cls.__name__
        if isinstance(require, str):
            require = [require]
        type.__setattr__(cls, "REQ", require)
        type.__setattr__(cls, "NAME", name)

    def __check_init(self):
        if not hasattr(self, "_submodules"):
            raise RuntimeError (
                "Please use `super().__init__()` to initialize Module before assign values."
            )

    def match(self, x : MatchResult, *args, **kwargs) -> MatchResult:
        raise NotImplementedError("%s.match not implemented!" % self.__class__.__name__)

    def __call__(self, match_result : MatchResult, *args, slot=None, **kwargs):        
        new_result = []
        for it in match_result:
            wrapper_result = MatchResult( match_result.sentence, [ SingleResult(it.index(), StartStructure()) ] )
            res = self.match(wrapper_result, *args, **kwargs)
            for sub_res in res:
                new_result.append(
                    SingleResult( sub_res.index(), ModuleStructure( self.__class__, it.structure, sub_res.structure, it.index(), sub_res.index() ) )
                )
        if slot is not None:
            for it in new_result:
                it.structure.set_slot(slot)
        return MatchResult(match_result.sentence, new_result)

    def __getattr__(self, name : AnyStr):
        if name.startswith("_"):
            return super().__getattribute__(name)

        self.__check_init()
        if name in self._submodules:
            from ..wrapper import ExpWrapper
            return ExpWrapper(self._submodules[name])
        return getattr(self.__nlex, name)
    
    def __setattr__(self, name : str, val):
        if (not name.startswith("_")) and isinstance(val, ModuleMatcher):
            self.__check_init()
            self._submodules[name] = val    
        else:
            super().__setattr__(name, val)

    def __delattr__(self, name : str):
        if name.startswith("_"):
            super().__delattr__(name)
        else:
            self.__check_init()
            if name in self._submodules:
                del self._submodules[name]
            else:
                super().__delattr__(name)