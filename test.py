from nlpexp import nlex, consts as cst

def main():

    sent = nlex.Sentence("台媒消息称，解放军机舰频频“扰台”，台湾防务部门负责人严德发今天（7日）称，今年到目前为止，台“空军”战机针对台湾周遭“敌情”威胁，迄今共出动2972架次监侦拦截，耗费成本约255亿元（新台币，下同）。而此前台媒估计，今年迄今台军共派遣空中战巡兵力4132架次，如果根据战机每一架次飞行1小时约100万元成本计算，换算下来花费至少超过41亿元。而严德发今天公布台“空军”耗费成本大大超出了台媒的估算，是台媒估算的6倍多。")


    s = sent.slot()
    x = nlex.AnyWord(sent, repeat="*")
    x = nlex.Number(x, slot=s)
    y = nlex.Char(x, "元")
    
    for it in y:
        print(s.get_val(it))

if __name__ == "__main__":
    main()