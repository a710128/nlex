from nlex.lib.abc import Package, Token, Tagger, Sentence
from nlex.lib import TokenMatcher

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


class CharMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(CharToken)

    def match(self, token, val = None):
        if super().match(token):
            if val is not None:
                return token.val in val
            return True
        return False

class AnyCharMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(CharToken)
    
    def match(self, token):
        if super().match(token):
            return True
        return False

class CharPack(Package, name="char"):
    def init(self, nlex : 'Nlex'):
        nlex._add_tagger("CharTagger", CharTagger() )
        nlex._add_method("Char", CharMatcher())
        nlex._add_method("AnyChar", AnyCharMatcher())