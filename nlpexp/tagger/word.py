from ..lib.abc import Tagger, Token
from ..lib import Sentence

class WordToken(Token):
    def __init__(self, val, pos, start, end):
        self.val = val
        self.pos = pos
        self.__start = start
        self.__end = end
    
    def start(self):
        return self.__start
    
    def end(self):
        return self.__end

class WordTagger(Tagger):
    def __init__(self):
        from fastHan import FastHan
        self.model = FastHan()
    
    def tag(self, sentence : Sentence) -> None:
        sent = sentence.get_sentence()

        start_idx = 0
        for word in self.model( sent, target="POS" )[0]:
            word, pos = word.word, word.pos
            start_idx = sent.find(word, start_idx)
            sentence.add_token( WordToken( word, pos, start=start_idx, end=start_idx + len(word)) )
            start_idx += len(word)
        

from ..main import NlpExp
NlpExp.register_tagger(WordTagger)