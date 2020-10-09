from .result import MatchResult
from .matcher import RepeatMatcher
from .abc import Matcher
from typing import Union, Tuple, List, AnyStr, Optional
from .slot import Slot
import inspect

def unique_repeat(x : MatchResult):
    # keep the longer one
    vis = {}
    for it in x:
        st, ed = it.structure.get_value()
        if st not in vis:
            vis[st] = (ed, it)
        else:
            if vis[st][0] < ed:
                vis[st] = (ed, it)
    return MatchResult (
        x.sentence,
        [ it for _, it in vis.values() ]
    )

class ExpWrapper(object):
    def __init__(self, matcher : Matcher):
        self.matcher = matcher
    
    def __call__(self, match_result : MatchResult, *args, repeat : Union[int, Tuple[int, int], List[int], AnyStr] = None, greedy : Optional[bool] = None, slot : Optional[Slot] = None, **kwargs) -> MatchResult:
        if greedy is not None:
            if "greedy" in inspect.getfullargspec(self.matcher.match).args:
                kwargs["greedy"] = greedy

        if greedy is None:
            greedy = True

        if repeat is not None:
            ret = RepeatMatcher()(match_result, repeat, self.matcher, *args, slot=slot, **kwargs)
            if greedy and len(ret) > 0:
                ret = unique_repeat(ret)
        else:
            ret = self.matcher(match_result, *args, slot=slot, **kwargs)
        ret.unique_()
        return ret