from typing import Optional, AnyStr
class Slot(object):
    def __init__(self, sent : Optional['Sentence'] = None):
        self.sent = sent
    
    def get_val(self, single_result : 'SingleResult') -> Optional[AnyStr]:
        v = single_result.get_slot(self)
        if (self.sent is None) or (v is None):
            return v
        sent = self.sent.get_sentence()
        st, ed = v
        return sent[st:ed]
            