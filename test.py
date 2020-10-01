import nlpexp

def main():

    sent = nlpexp.Sentence("我今天就早点下播了。")
    # 我 今天 就 早点 下播 了

    s = sent.slot()

    x = nlpexp.word(sent, repeat=[2, 3, 5])
    x = nlpexp.word(x, slot=s)

    correct_val = [ "就", "早点", "了" ]
    for it, gt in zip(x, correct_val):
        print(it, s.get_val(it), gt, s.get_val(it) == gt)

if __name__ == "__main__":
    main()