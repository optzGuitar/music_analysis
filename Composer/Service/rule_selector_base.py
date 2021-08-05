from abc import ABC
from collections import defaultdict
from typing import List, Pattern, Tuple


class RuleSelectorBase(ABC):
    def __init__(self) -> None:
        self._grounded_rules: int = 0
        self.pattern_per_length: defaultdict[
            int, List[Tuple[Pattern, int]]
        ] = defaultdict(list)
        self._grounded_length: int = 0
        self.max_pattern_internal_distance = None
