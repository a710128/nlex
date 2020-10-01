from ..abc import Matcher
from ..result import MatchResult, SingleResult
from ..structure import TokenStructure

class TokenMatcher(Matcher):
    def __init__(self, token_cls):
        self.__token_cls = token_cls
    
    def match(self, token):
        return isinstance(token, self.__token_cls)
    
    def __call__(self, match_result: MatchResult, *args, **kwargs):
        new_result = []
        for it in match_result:
            
            for token in match_result.sentence.get_tokens(it.index()):
                if self.match(token, *args, **kwargs):
                    new_result.append(
                        SingleResult( token.end(), TokenStructure( it.structure, token ) )
                    )
        return MatchResult( match_result.sentence, new_result )

