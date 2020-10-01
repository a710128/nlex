from ..lib import RepeatMatcher, Sentence, MatchResult, MatchResult, Slot
from ..lib.abc import Tagger, Matcher
from typing import Union, Tuple, List, AnyStr, Optional, Dict

class ExpWrapper(object):
    def __init__(self, matcher):
        self.matcher = matcher
    
    def __call__(self, match_result : MatchResult, *args, repeat : Union[int, Tuple[int, int], List[int], AnyStr] = None, slot : Optional[Slot] = None, **kwargs) -> MatchResult:
        if repeat is not None:
            ret = RepeatMatcher()(match_result, repeat, self.matcher, *args, **kwargs)

        else:
            ret = self.matcher(match_result, *args, **kwargs)
        if slot is not None:
            for it in ret:
                it.structure.set_slot(slot)
        return ret

class NlpExp(object):
    def __init__(self):
        self.__taggers = []
        self.__exps = {}
    
    def register_exp(self, name, exp):
        self.__exps[name] = exp
    
    def register_tagger(self, tagger : Tagger):
        self.__taggers.append(tagger())
    
    def __getattr__(self, name):
        if name in self.__exps:
            return ExpWrapper(self.__exps[name]())
        raise AttributeError(
            "'%s' object has no attribute '%s" % \
                ( self.__class__.__name__, name )
        )
    
    def _get_matchers(self) -> Dict[AnyStr, Matcher]:
        return self.__exps
    
    def Sentence(self, sent):
        sent = Sentence(sent)
        for tag in self.__taggers:
            tag.tag(sent)
        return MatchResult(sent)