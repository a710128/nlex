from ..lib import TokenMatcher
from ..tagger.word import WordToken

class WordMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(WordToken)

    def match(self, token : WordToken, val=None, pos=None):
        if super().match(token):
            if (val is not None) and (token.val.lower() != val.lower()):
                return False
            if (pos is not None) and (token.pos.lower() != pos.lower()):
                return False
            return True
        return False

from ..main import NlpExp
NlpExp.register_exp("word", WordMatcher)
