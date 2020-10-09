
from .abc import Repeat as _Repeat
from typing import Union, Tuple, List, AnyStr

class IntRepeat(_Repeat):
    def __init__(self, repeat):
        self.__repeat = repeat
    
    def checkin(self, repeat):
        return self.__repeat == repeat
    
    def overflow(self, repeat):
        return repeat > self.__repeat
class RangeRepeat(_Repeat):
    def __init__(self, low, high):
        self.__repeat_low = low
        self.__repeat_high = high
    
    def checkin(self, repeat):
        return self.__repeat_low <= repeat and repeat <= self.__repeat_high
    
    def overflow(self, repeat):
        return repeat > self.__repeat_high
    
class LowRepeat(_Repeat):
    def __init__(self, low):
        self.__low = low

    def checkin(self, repeat):
        return repeat >= self.__low
    
    def overflow(self, repeat):
        return False

class ListRepeat(_Repeat):
    def __init__(self, lst):
        self.__lst = sorted(lst)
    
    def checkin(self, repeat):
        return repeat in self.__lst
    
    def overflow(self, repeat):
        if len(self.__lst) == 0:
            return True
        else:
            return repeat > self.__lst[-1]

def Repeat(repeat : Union[int, Tuple[int, int], List[int], AnyStr]) -> _Repeat:
    if isinstance(repeat, int):
        return IntRepeat(repeat)
    elif isinstance(repeat, tuple):
        start, end = repeat
        if start is None:
            start = 0
        if end is None:
            return LowRepeat(start)
        else:
            return RangeRepeat(start, end)
    elif isinstance(repeat, list):
        return ListRepeat(repeat)
    elif isinstance(repeat, str):
        if repeat == "*":
            return LowRepeat(0)
        elif repeat == "+":
            return LowRepeat(1)
        elif repeat == "?":
            return RangeRepeat(0, 1)
    raise TypeError(
        "Unknown repeat type"
    )
        