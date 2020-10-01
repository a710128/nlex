from .abc import Matcher, Token
from . import abc
from .repeat import Repeat
from .result import MatchResult, SingleResult, TokenStructure, StartStructure, ModuleStructure
from typing import Type, Union, Tuple, List, AnyStr

class TokenMatcher(Matcher):
    def __init__(self, token_cls : Type[Token]):
        self.__token_cls = token_cls
    
    def match(self, token : Token):
        return isinstance(token, self.__token_cls)
    
    def __call__(self, match_result: MatchResult):
        new_result = []
        for it in match_result:
            for token in match_result.sentence.get_tokens(it.index()):
                if self.match(token):
                    new_result.append(
                        SingleResult( token.end(), TokenStructure( it.strcuture, token ) )
                    )
        return MatchResult( match_result.sentence, new_result )

class ModuleMatcher(Matcher):
    def __init__(self):
        pass

    def match(self, x : MatchResult, *args, **kwargs) -> MatchResult:
        raise NotImplementedError("%s.match not implemented!" % self.__class__.__name__)

    def __call__(self, match_result : MatchResult, *args, **kwargs) -> MatchResult:
        new_result = []
        for it in match_result:
            wrapper_result = MatchResult( match_result.sentence, [ SingleResult(it.index(), StartStructure()) ] )
            res = self.match(wrapper_result, *args, **kwargs)
            for sub_res in res:
                new_result.append(
                    SingleResult( sub_res.index(), ModuleStructure( self.__class__, it.structure, sub_res.structure, it.index(), sub_res.index() ) )
                )
        return MatchResult(new_result)
        
class RepeatMatcher(ModuleMatcher):
    def match(self, x : MatchResult, repeat, sub_matcher, *args, **kwargs):
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
    
    def __call__(self, match_result : MatchResult, repeat : Union[int, Tuple[int ,int], List[int], AnyStr], sub_matcher : Matcher, *args, **kwargs):
        super().__call__(match_result, repeat, sub_matcher, *args, **kwargs)