from ..lib import TokenMatcher
from ..tagger.char import CharToken

class CharMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(CharToken)

    def match(self, token, val = None):
        if super().match(token):
            if val is not None:
                return token.val == val
            return True
        return False

from ..main import NlpExp
NlpExp.register_exp("char", CharMatcher)
