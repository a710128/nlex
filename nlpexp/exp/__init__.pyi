from ..lib import MatchResult, Slot
from typing import Optional, AnyStr

RepeatType = Union[int, Tuple[int, int], List[int], AnyStr]

__all__ = ["char", "word"]

def char(match_result : MatchResult, val : Optional[AnyStr], repeat : RepeatType, slot : Slot) -> MatchResult: ...

def word(match_result : MatchResult, val : Optional[AnyStr], pos : Optional[AnyStr], repeat : RepeatType, slot : Slot) -> MatchResult: ...