from nlex import nlex, consts as cst, exp
def main():
    nlex.add(exp.Date)
    nlex.add(exp.Money)
    sent = nlex.Sentence("据彭博社7日报道，出于所谓“国家安全”担忧，特朗普政府在考虑对阿里旗下蚂蚁集团及腾讯支付平台实施限制。知情人士称，最近几周白宫高级官员正加快推动，关于如何及是否应实施相关限制的内部讨论，不过这还没有最终结论。")
    
    s = sent.slot()
    y = nlex.Date(sent, slot=s, greedy=True)
    # y = nlex.Money(sent, slot=s)
    
    for it in y:
        print(s.get_val(it))

if __name__ == "__main__":
    main()