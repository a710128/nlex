from typing import Iterator, AnyStr
from .token import Token
class Sentence(object):
    def __init__(self, sent : AnyStr): ...
    
    def get_sentence(self) -> AnyStr: ...
    
    def add_token(self, token : Token): ...
    
    def get_tokens(self, index) -> Iterator[Token]: ...