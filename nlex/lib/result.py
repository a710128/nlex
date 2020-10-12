from typing import Iterator, Optional, Tuple, Union, List
from .abc import Matcher, Repeat, Token
from .sentence import Sentence
from .structure import Structure, StartStructure, StartStructure, ModuleStructure, TokenStructure
from .slot import Slot

def find_slot(structure: Structure, slot) -> Union[Structure, None]:
    x = structure
    while not isinstance(x, StartStructure):
        if x.is_slot(slot):
            return x
        if isinstance(x, ModuleStructure):
            res = find_slot( x.sub, slot )
            if res is not None:
                return res
        x = x.last()
    return None


class SingleResult(object):
    def __init__(self, start_idx, structure : Structure):
        self.__start_idx = start_idx
        self.structure = structure

    def index(self):
        return self.__start_idx
    
    def _get_slot(self, slot : Slot) -> Union[Structure, None]:
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
            self.__results = [ SingleResult(idx, StartStructure()) for idx in range(len(self.sentence)) ]
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
    
    def combine(self, result_b : 'MatchResult') -> 'MatchResult':
        return MatchResult(self.sentence, self.__results + result_b.__results )
    
    def unique_(self, short : bool = True):
        vis = {}
        for it in self.__results:
            if it.index() not in vis:
                vis[it.index()] = it
            else:
                if (vis[it.index()].structure.get_value()[0] < it.structure.get_value()[0]) == short:
                    vis[it.index()] = it
        self.__results = list(vis.values())
    
    def unique(self, short : bool = True) -> 'MatchResult':
        vis = {}
        for it in self.__results:
            if it.index() not in vis:
                vis[it.index()] = it
            else:
                if (vis[it.index()].structure.get_value()[0] < it.structure.get_value()[0]) == short:
                    vis[it.index()] = it
        return MatchResult(self.sentence, list(vis.values()))
    
    def exclude(self, result_b : 'MatchResult') -> 'MatchResult':
        vis = set()
        for it in result_b.__results:
            vis.add(it.index())
        ret = [it for it in self.__results if it.index() not in vis ]
        return MatchResult(self.sentence, ret)
    
    def exclude_(self, result_b : 'MatchResult'):
        vis = set()
        for it in result_b.__results:
            vis.add(it.index())
        ret = [it for it in self.__results if it.index() not in vis ]
        self.__results = ret