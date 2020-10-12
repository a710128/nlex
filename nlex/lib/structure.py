from .abc import Token, Structure
from .slot import Slot
from typing import TypeVar, Type, Tuple, Iterator, List, Union


class StartStructure(Structure):
    def __init__(self, parent = None, pos = None):
        self.parent = parent
        self.pos = pos

    def set_slot(self, slot : Slot):
        pass
    
    def is_slot(self, slot : Slot) -> bool:
        return False
    
    def get_value(self) -> Tuple[int, int]:
        return 0, 0
    
    def last(self) -> None:
        return None
    
    def __repr__(self):
        return "<Start>"


class TokenStructure(Structure):
    def __init__(self, last, token : Token):
        self.__last = last
        self.token = token
        self.__start = token.start()
        self.__end = token.end()

        self.slot = None

    def set_slot(self, slot : Slot):
        self.slot = slot
    
    def is_slot(self, slot : Slot) -> bool:
        return (self.slot is not None) and (self.slot is slot)
    
    def get_value(self) -> Tuple[int, int]:
        return self.__start, self.__end
    
    def last(self) -> int:
        return self.__last
    
    def __repr__(self):
        if hasattr(self.token, "val"):
            return "<Token '%s' (%d, %d)>" % (self.token.val, self.__start, self.__end)
        return "<Token (%d, %d)>" % (self.__start, self.__end)

class ModuleStructure(Structure):
    def __init__(self, cls_name : Type['ModuleMatcher'], last : Structure, sub : Structure, start : int, end : int):
        self.__cls_name = cls_name
        self.__last = last
        self.sub = sub
        self.__start = start
        self.__end = end

        self.slot = None
    
    def set_slot(self, slot : Slot):
        self.slot = slot
    
    def is_slot(self, slot : Slot) -> bool:
        return (self.slot is not None) and (self.slot is slot)

    def get_value(self) -> Tuple[int, int]:
        return self.__start, self.__end
    
    def last(self) -> int:
        return self.__last
    
    def __repr__(self):
        return "<Module '%s' (%d, %d)>" % (self.__cls_name.__name__, self.__start, self.__end)
    
    def __iter__(self) -> Iterator[Structure]:
        ret = []
        x = self.sub
        while not isinstance(x, StartStructure):
            ret.append(x)
            x = x.last()
        for it in ret[::-1]:
            yield it
    
    def to_list(self) -> List[Structure]:
        ret = []
        x = self.sub
        while not isinstance(x, StartStructure):
            ret.append(x)
            x = x.last()
        return ret[::-1]