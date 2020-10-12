from nlex import nlex, consts as cst, Module, exp

def sent_cut(doc : str):
    return doc.splitlines()

class Lending(Module, name="Lending"):
    def lend_phrase(self, x):
        x1 = nlex.Word(x, ["借款", "抬款", "贷款"])
        x11 = nlex.Word(x1, "本金", repeat="?")
        x11 = nlex.Word(x11, ["现金", "人民币"], repeat="?")

        x12 = nlex.Word(x1, "人民币", repeat="?")
        x12 = nlex.Word(x12, "本金", repeat="?")
        x1 = nlex.All(x11, x12)

        x2 = nlex.Word(x, "借")
        x2 = nlex.Word(x2, ["现金", "人民币"], repeat="?")

        return nlex.All(x1, x2)

    def style1(self, x, slot_date, slot_money):
        x = nlex.Date(x, slot=slot_date)
        x = nlex.Word(x, ["归还", "还款", "偿还", "利息", "欠息"], neq=True, repeat="*")
        x = self.lend_phrase(x)
        x = nlex.Money(x, slot=slot_money)
        return x
    
    def style2(self, x, slot_date, slot_money):
        x = nlex.Date(x, slot=slot_date)
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "原告")
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "将")
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Money(x, slot=slot_money)
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "出借")
        x = nlex.Word(x, "给")
        x = nlex.Word(x, "了", repeat="*")
        x = nlex.Word(x, "被告")
        return x
    
    def style3(self, x, slot_date, slot_money):
        x = nlex.Date(x, slot=slot_date)
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "原告")
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "借给")
        x = nlex.Word(x, "被告")
        x = nlex.Word(x, "现金", repeat="?")
        x = nlex.Money(x, slot=slot_money)
        return x
    
    def style4(self, x, slot_date, slot_money):
        x = nlex.Date(x, slot=slot_date)
        x = nlex.AnyWord(x, repeat="*")
        x = nlex.Word(x, "欠")
        x = nlex.Word(x, "原告")
        x = nlex.Word(x, "现金", repeat="?")
        x = nlex.Money(x, slot=slot_money)
        return x

    def match(self, x, slot_date = None, slot_money = None):
        return nlex.All(
            self.style1(x, slot_date, slot_money),
            self.style2(x, slot_date, slot_money),
            self.style3(x, slot_date, slot_money),
            self.style4(x, slot_date, slot_money)
        )

def main():
    nlex.add(exp.Date)
    nlex.add(exp.Money)
    nlex.add(Lending)

    """
    for i in range(20):
        doc = open("data/%d.txt" % i, "r").read()
        res = []
        for sent in sent_cut(doc):
            sent = nlex.Sentence(sent)

            ss = sent.slot()
            sd = sent.slot()
            sm = sent.slot()

            for it in nlex.Lending(sent, slot=ss, slot_date=sd, slot_money=sm):
                res.append("时间：" + sd.get_val(it) + ", 金额：" + sm.get_val(it))
        print("=========== %d ===========" % i)
        for it in res:
            print(it)
    """

    sent = nlex.Sentence( input("请输入事实描述：") )
    ss = sent.slot()
    sd = sent.slot()
    sm = sent.slot()
    for it in nlex.Lending(sent, slot=ss, slot_date=sd, slot_money=sm):
        print("=" * 36)
        print( ss.get_val(it) )
        print( sd.get_val(it) )
        print( sm.get_val(it) )

if __name__ == "__main__":
    main()