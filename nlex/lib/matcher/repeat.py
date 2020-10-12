from .. import abc
from .module import ModuleMatcher
from ..result import MatchResult
from ..repeat import Repeat

class RepeatMatcher(ModuleMatcher):
    def match(self, x : MatchResult, repeat, sub_matcher, args, kwargs):
        if not isinstance(repeat, abc.Repeat):
            repeat = Repeat(repeat)
        
        new_result = []
        cnt = 0
        if repeat.checkin(0):
            new_result.extend (
                [ it for it in x ]
            )
        while len(x) > 0 and (not repeat.overflow(cnt + 1)):
            x = sub_matcher(x, *args, **kwargs)
            cnt += 1
            if repeat.checkin(cnt):
                new_result.extend (
                    [it for it in x]
                )
        return MatchResult( x.sentence, new_result )
            