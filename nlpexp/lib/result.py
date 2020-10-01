from typing import Iterator, Optional, Tuple, Union, List
from .abc import Matcher, Repeat, Token
from .sentence import Sentence
from .structure import Structure, StartStructure, StartStructure, ModuleStructure, TokenStructure
from .slot import Slot

def find_slot(structure: Structure, slot) -> Union[Tuple[int, int], None]:
    x = structure
    while not isinstance(x, StartStructure):
        if x.is_slot(slot):
            return x.get_value()
        if isinstance(x, ModuleStructure):
            res = find_slot( x.sub, slot )
            if res is not None:
                return res
    return None

class SingleResult(object):
    def __init__(self, start_idx, structure : Structure):
        self.__start_idx = start_idx
        self.structure = structure

    def index(self):
        return self.__start_idx
    
    def get_slot(self, slot : Slot):
        return find_slot(self.structure, slot)

    def __repr__(self):
        return "<Result (0, %d)>" % self.__start_idx
    
    def __iter__(self):
        ret = []
        x = self.structure
        while not isinstance(x, StartStructure):
            ret.append(x)
            x = x.last()
        for it in ret[::-1]:
            yield it
    
    def to_list(self):
        ret = []
        x = self.structure
        while not isinstance(x, StartStructure):
            ret.append(x)
            x = x.last()
        return ret[::-1]
    
    def __getitem__(self, key : int) -> Structure:
        return self.to_list()[key]
    
class MatchResult(object):
    def __init__(self, sentence : Sentence, results : Optional[List[SingleResult]] = None):
        self.sentence = sentence
        if results is None:
            self.__results = [ SingleResult(0, StartStructure()) ]
        else:
            self.__results = results

    def __iter__(self) -> Iterator[SingleResult]:
        for it in self.__results:
            yield it

    def __len__(self) -> int:
        return len(self.__results)
    
    def __repr__(self):
        return "<ResultList of %d results >" % len(self.__results)
    
    def __getitem__(self, key : int) -> SingleResult:
        return self.__results[key]
    
    def slot(self) -> Slot:
        return Slot(self.sentence)