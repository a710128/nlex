from ..lib import Module
from ..consts import pos

class DateYear(Module, name="Date.Year", require=["fast_han"]):
    def match(self, x):
        x = self.Number(x)
        x = self.Char(x, "年")
        return x

class DateMonth(Module, name="Date.Month", require=["fast_han"]):
    def match(self, x):
        x = self.Number(x)
        x = self.Char(x, "月")
        x = self.Char(x, "份", repeat="?")
        return x

class DateDay(Module, name="Date.Day", require=["fast_han"]):
    def match(self, x):
        x = self.Number(x)
        x = self.Char(x, "日")
        return x

class Date(Module, name="Date", short=False):
    def __init__(self):
        super().__init__()
        self.year = DateYear()
        self.month = DateMonth()
        self.day = DateDay()

    def match(self, x : 'MatchResult', greedy=True):
        if greedy:
            p1 = self.year(x)
            p2 = self.month(p1, repeat="?")
            p3 = self.day(p2, repeat="?")

            q1 = self.month(x.exclude(p1))
            q2 = self.day(q1, repeat="?")
            
            r1 = self.day(x.exclude(q1))
            return self.All(p3, q2, r1)
        else:
            p1 = self.year(x)
            p2 = self.month(p1, repeat=(0, 1), greedy=False)
            p3 = self.day(p2, repeat=(0, 1), greedy=False)

            q1 = self.month(x)
            q2 = self.day(q1, repeat=(0, 1), greedy=False)
            
            r1 = self.day(x)
            return self.All(p3, q2, r1)