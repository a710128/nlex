from nlpexp.lib.abc import Package, Token, Tagger, Sentence
from nlpexp.lib import TokenMatcher

class NumberToken(Token):
    def __init__(self, val, num, start, end):
        self.val = val
        self.num = num
        self.__start = start
        self.__end = end
    
    def start(self):
        return self.__start
    
    def end(self):
        return self.__end

CHN_CHAR = {
    u"\uff2f": 0,
    u"\u3007": 0,
    u"\u25cb": 0,
    u"\uff10": 0,
    u"\u039f": 0,
    u'零': 0,
    u"O": 0,
    u"０": 0,
    u"0": 0,
    u"1": 1,
    u"１": 1,
    u"一": 1,
    u"壹": 1,
    u"二": 2,
    u"2": 2,
    u"２": 2,
    u"贰": 2,
    u"两": 2,
    u'三': 3,
    u"3": 3,
    u"３": 3,
    u"叁": 3,
    u'四': 4,
    u"4": 4,
    u"４": 4,
    u"肆": 4,
    u'五': 5,
    u"5": 5,
    u"５": 5,
    u"伍": 5,
    u'六': 6,
    u"6": 6,
    u"６": 6,
    u"陆": 6,
    u'七': 7,
    u"7": 7,
    u"７": 7,
    u"柒": 7,
    u'八': 8,
    u"8": 8,
    u"８": 8,
    u"捌": 8,
    u'九': 9,
    u"9": 9,
    u"９": 9,
    u"玖": 9,
    u'十': 10,
    u"拾": 10,
    u'百': 100,
    u"佰": 100,
    u'千': 1000,
    u"仟": 1000,
    u'万': 10000,
    u"亿": 100000000,
}
def parse_ge(sent : str):
    if len(sent) == 0:
        return None
    if CHN_CHAR[sent[0]] == 10:
        if len(sent) > 2:
            return None
        elif len(sent) == 2:
            return CHN_CHAR[sent[0]] + CHN_CHAR[sent[1]]
        else:
            return 10
    
    ret = 0
    num = 0
    for it in sent:
        if CHN_CHAR[it] < 10:
            num = CHN_CHAR[it]
        else:
            ret += num * CHN_CHAR[it]
            num = 0
    ret += num
    return ret

def parse_wan(sent : str):
    if len(sent) == 0:
        return None
    idx = None
    for i, it in enumerate(sent):
        if CHN_CHAR[it] == 10000:
            idx = i
            break
    if idx is not None:
        v_fore = parse_ge(sent[: idx])
        v_rear = parse_ge(sent[idx + 1 :]) if idx + 1 < len(sent) else 0
        if v_fore is None or v_rear is None:
            return None
        return v_fore * 10000 + v_rear
    else:
        return parse_ge(sent)

def parse_number(sent : str):
    no_pow = True
    for it in sent:
        if CHN_CHAR[it] >= 10:
            no_pow = False
            break

    if no_pow:
        num = 0
        for it in sent:
            num = num * 10 + CHN_CHAR[it]
        return num
    else:
        idx = None
        for i, it in enumerate(sent):
            if CHN_CHAR[it] == 100000000:
                idx = i
                break
        if idx is not None:
            v_fore = parse_wan(sent[: idx])
            v_rear = parse_wan(sent[idx + 1 :]) if idx + 1 < len(sent) else 0
            if v_fore is None or v_rear is None:
                return None
            return v_fore * 100000000 + v_rear
        else:
            return parse_wan(sent)

def sanitize(sent):
    ret = ""
    for it in sent:
        if it == "." or it in CHN_CHAR:
            ret += it
    return ret

class NumberTagger(Tagger):
    def __init__(self, chn):
        self.chn = chn
    
    def tag(self, sentence : Sentence) -> None:
        sent = sentence.get_sentence()
        if self.chn:
            lst = []
            lst_index = []
            first = True
            for i in range(len(sent)):
                if sent[i] in CHN_CHAR:
                    if first:
                        first = False
                        lst.append(sent[i])
                        lst_index.append(i)
                    else:
                        lst[-1] += sent[i]
                else:
                    first = True
            for idx, it in zip(lst_index, lst):
                sentence.add_token( 
                    NumberToken( it, parse_number( sanitize(it) ), idx, idx + len(it) )
                )
        # Arabic
        vis = set(lst_index)
        lst = []
        lst_index = []
        first = True
        for i, it in enumerate(sent):
            if it in "0123456789" or (not first and (it in ",. ")):
                if first:
                    first = False
                    lst.append(it)
                    lst_index.append(i)
                else:
                    lst[-1] += it
            else:
                first = True
        for idx, it in zip(lst_index, lst):
            if (idx in vis) and (it.find(".") == -1):
                continue
            try:
                clean_it = sanitize(it)
                if clean_it.find(".") == -1:
                    v = int( clean_it )
                else:
                    v = float(clean_it)
            except ValueError:
                v = None
            sentence.add_token( 
                NumberToken( it, v, idx, idx + len(it) )
            )


class NumberMatcher(TokenMatcher):
    def __init__(self):
        super().__init__(NumberToken)

    def match(self, token : NumberToken, cmp=None):
        if super().match(token):
            if cmp is not None:
                return cmp(token.num)
            return True
        return False

class NumberPack(Package, name="number"):
    def __init__(self, chn=True):
        self.chn = chn
    
    def init(self, nlex):
        nlex._add_tagger("NumberTagger", NumberTagger(self.chn))
        nlex._add_method("Number", NumberMatcher())