from .pack import mod_map
from typing import Union, Tuple, List, AnyStr, Optional, Dict, Type
from .lib.abc import Tagger, Matcher
from .lib import MatchResult, RepeatMatcher, Sentence, Slot, Module
from .lib.wrapper import ExpWrapper

    
class Nlex(object):
    def __init__(self):
        self.__taggers = {}
        self.__methods = {}
        self.__registerd = set()
    
    def register(self, name : AnyStr, *args, **kwargs):
        if name not in mod_map:
            raise AttributeError(
                "No module named '%s'" % name
            )
        if name in self.__registerd:
            return
        self.__registerd.add(name)
        obj = mod_map[name](*args, **kwargs)
        obj.init(self)
    
    def _add_tagger(self, name : AnyStr, tagger : Union[Type[Tagger], Tagger]):
        if isinstance(tagger, type):
            self.__taggers[name] = tagger()
        else:
            self.__taggers[name] = tagger
    
    def _add_method(self, name : AnyStr, method : Union[Type[Matcher], Matcher]):
        self.__methods[name] = method
    
    def __getattr__(self, name : AnyStr) -> ExpWrapper:
        if name in self.__methods:
            if isinstance(self.__methods[name], type):
                # if it is a class, then new an instance
                return ExpWrapper(self.__methods[name]())
            else:
                return ExpWrapper(self.__methods[name])
        raise AttributeError(
            "'%s' object has no attribute '%s" % \
                ( self.__class__.__name__, name )
        )
    
    def add(self, module : Type[Module], *args, name=None, **kwargs):
        if name is None:
            name = module.NAME
        mod = module(*args, **kwargs)
        mod._assign(self)
        self.__methods[ name ] = mod
    
    def Sentence(self, sent : AnyStr) -> MatchResult:
        sent = Sentence(sent)
        for tag in self.__taggers.values():
            tag.tag(sent)
        return MatchResult(sent)
    
    def All(self, *args) -> MatchResult:
        if len(args) == 0:
            raise TypeError("`All()` needs at least one parameter.")
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        for i, result in enumerate(args):
            if not isinstance(result, MatchResult):
                raise TypeError("`All()`: parameter %d is not an instance of MatchResult" % i)
        sent = args[0].sentence
        for i, result in enumerate(args):
            if result.sentence is not sent:
                raise TypeError("`All()`: the sentence of result %d is different than result 0." % i)
        ret = MatchResult(sent, [])
        for result in args:
            ret = ret.combine(result)
        ret.unique_()
        return ret
