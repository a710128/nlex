from typing import AnyStr
from .lib.abc import Matcher, Tagger
from .lib import MatchResult

def register_exp(name : AnyStr, exp : Matcher): ...

def register_tagger(tagger : Tagger): ...

def Sentence(sent : AnyStr) -> MatchResult: ...

from .exp import *