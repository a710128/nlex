from typing import Union, Tuple
class Structure(object):
    def __init__(self):
        pass
    
    def set_slot(self, slot : 'Slot') -> None:
        pass

    def is_slot(self, slot : 'Slot') -> bool:
        return False

    def get_value(self) -> Tuple[int, int]:
        return (0, 0)

    def last(self) -> Union[None, 'Structure']:
        return None
    