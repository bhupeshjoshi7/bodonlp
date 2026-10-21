"""
Convenience alias package for bodonlp.
Allows users to do `import bodo_lang` interchangeably with `import bodonlp`.
"""

import bodonlp
from bodonlp import *
from bodonlp import (
    numbers,
    grammar,
    lexicon,
    translator,
    culture,
    scraper,
    voice,
)

__all__ = bodonlp.__all__
