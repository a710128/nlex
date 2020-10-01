from ..abc import Matcher
from ..result import MatchResult, SingleResult
from ..structure import ModuleStructure, StartStructure

class ModuleMatcher(Matcher):
    def __init__(self):
        pass

    def match(self, x : MatchResult, *args, **kwargs) -> MatchResult:
        raise NotImplementedError("%s.match not implemented!" % self.__class__.__name__)

    def __call__(self, match_result : MatchResult, *args, **kwargs):        
        new_result = []
        for it in match_result:
            wrapper_result = MatchResult( match_result.sentence, [ SingleResult(it.index(), StartStructure()) ] )
            res = self.match(wrapper_result, *args, **kwargs)
            for sub_res in res:
                new_result.append(
                    SingleResult( sub_res.index(), ModuleStructure( self.__class__, it.structure, sub_res.structure, it.index(), sub_res.index() ) )
                )
        return MatchResult(match_result.sentence, new_result)
