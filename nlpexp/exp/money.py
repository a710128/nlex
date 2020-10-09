from ..lib import Module

class Money(Module, name="Money"):
    def match(self, x : 'MatchResult'):
        x = self.Number(x)
        x = self.Char(x, "元")
        return x