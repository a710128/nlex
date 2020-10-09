
from nlpexp.lib.abc import Package, Token, Tagger
from nlpexp.lib import Sentence, TokenMatcher
import re

class WordToken(Token):
    def __init__(self, val : str, pos : str, start : int, end : int):
        self.val = val
        self.pos = pos.lower()
        self.__start = start
        self.__end = end
    
    def start(self) -> int:
        return self.__start
    
    def end(self) -> int:
        return self.__end

class NERToken(Token):
    def __init__(self, val : str, ner : str, start : int, end : int):
        self.val = val
        self.ner = ner.lower()


class WordTagger(Tagger):
    def __init__(self):
        from fastHan import FastHan
        self.model = FastHan()

    def tag(self, sentence : Sentence) -> None:
        sent = sentence.get_sentence()

        _pos = 0
        while _pos < len(sent):
            ed = _pos
            last_ok = None
            while ed - _pos < 500 and ed < len(sent):
                if ed + 1 == len(sent) or sent[ed] in "“”，。；？！‘’【】「」：,.;'\":":
                    last_ok = ed + 1
                ed += 1
            if last_ok is not None:
                ed = last_ok
            subsent = sent[_pos: ed]
            _pos = ed

            # Add POS
            start_idx = 0
            for word in self.model( subsent, target="POS" )[0]:
                word, pos = word.word, word.pos
                start_idx = subsent.find(word, start_idx)
                sentence.add_token( WordToken( word, pos, start=start_idx, end=start_idx + len(word)) )
                start_idx += len(word)
            
            # Add NER
            for word in self.model( subsent, target="NER" )[0]:
                word, ner = word.word, word.ner
                
                start_idx = 0
                while True:
                    index = subsent.find(word, start_idx)
                    if index == -1:
                        break
                    sentence.add_token( NERToken( word, ner, index, index + len(word) ) )
                    start_idx = index + 1
            
class WordMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(WordToken)

    def match(self, token : WordToken, val=None, regex=None, pos=None):
        if super().match(token):
            if (val is not None):
                if isinstance(val, str) and (token.val.lower() != val.lower()):
                    return False
                if isinstance(val, list):
                    val = [it.lower() for it in val]
                    if token.val.lower() not in val:
                        return False
            if regex is not None:
                if re.match(regex, token.val) is None:
                    return False
            if (pos is not None) and (token.pos.lower() != pos.lower()):
                return False
            return True
        return False

class AnyWordMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(WordToken)
    
    def match(self, token : WordToken):
        return super().match(token)

class NERMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(NERToken)
    
    def match(self, token : NERToken, ner = None):
        if super().match(token):
            if ner is not None and ner.lower() != token.ner:
                return False
            return True
        return False

class FastHan(Package, name="fast_han"):
    def init(self, nlex : 'Nlex'):
        nlex._add_tagger("WordTagger", WordTagger() )
        nlex._add_method("Word", WordMatcher())
        nlex._add_method("AnyWord", AnyWordMatcher())
        nlex._add_method("NER", NERMatcher())

