from ..lib.abc import Tagger, Token
from ..lib import Sentence

class CharToken(Token):
    def __init__(self, val, start, end):
        self.val = val
        self.__start = start
        self.__end = end
    
    def start(self):
        return self.__start
    
    def end(self):
        return self.__end

class CharTagger(Tagger):
    def __init__(self):
        pass
    
    def tag(self, sentence : Sentence) -> None:
        sent = sentence.get_sentence()
        for i in range(len(sent)):
            sentence.add_token( CharToken( sent[i], i, i + 1 ) )

from ..main import NlpExp
NlpExp.register_tagger(CharTagger)