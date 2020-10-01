from .main import NlpExp
from . import exp as __exp
from . import tagger as __tagger

__all__ = [
    "register_exp",
    "register_tagger",
    "Sentence",
] + [
    matcher_name for matcher_name in NlpExp._get_matchers().keys()
]

for name in __all__:
    if name.startswith('__'):
        continue
    globals()[name] = getattr(NlpExp, name)

del NlpExp
del main
del exp
del name
del tagger

from . import lib