from typing import Iterator, AnyStr
from .abc import Token
from .abc import Sentence as Sentence_
class Sentence(Sentence_):
    def __init__(self, sent : AnyStr):
        self.__sent = sent
        self.__tokens = {}
    
    def get_sentence(self) -> AnyStr:
        return self.__sent
    
    def add_token(self, token : Token):
        st = token.start()
        if st not in self.__tokens:
            self.__tokens[st] = []
        self.__tokens[st].append( token )
    
    def get_tokens(self, index) -> Iterator[Token]:
        if index not in self.__tokens:
            return
        for it in self.__tokens[index]:
            yield it
    
    def __len__(self):
        return len(self.__sent)