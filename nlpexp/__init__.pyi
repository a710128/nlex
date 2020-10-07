from typing import AnyStr, overload, List
from .lib.abc import Matcher, Tagger
from .lib import MatchResult

def register_exp(name : AnyStr, exp : Matcher): ...

def register_tagger(tagger : Tagger): ...

def Sentence(sent : AnyStr) -> MatchResult: ...

@overload
def All(result_list : List[MatchResult]) -> MatchResult : ...

@overload
def All(*args : MatchResult) -> MatchResult : ...

from .exp import *