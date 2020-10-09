from typing import Optional, AnyStr
from .abc import Structure

class Slot(object):
    def __init__(self, sent : Optional['Sentence'] = None):
        self.sent = sent
    
    def get_val(self, single_result : 'SingleResult') -> Optional[AnyStr]:
        v = single_result._get_slot(self)
        if (self.sent is None) or (v is None):
            return v
        sent = self.sent.get_sentence()
        st, ed = v.get_value()
        return sent[st:ed]
    
    def get_object(self, single_result : 'SingleResult') -> Structure:
        return single_result._get_slot(self)
    

            