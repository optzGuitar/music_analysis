from collections import defaultdict
from typing import Dict, List, Tuple
from Miner.type import Type
from Data.pattern import Pattern
import time
from abc import ABC, abstractmethod


class CleanupBase(ABC):
    def __init__(self, patterns: Dict[Type, List], elimination_strategy=None):
        self._patterns_raw = patterns
        self._elimination_strategy = elimination_strategy if elimination_strategy is not None else self._take_lowest_id
        self._convert_to_pat_atoms()

    def _convert_to_pat_atoms(self):
        pat_atoms = []
        patterns: List[Pattern]
        for _, patterns in self.__patterns_raw.items():
            for pattern in patterns:
                pat_atoms.extend(pattern.to_pattern_with_id(len(pat_atoms)))

        self._patterns = pat_atoms

    @staticmethod
    def _take_lowest_id(model: List) -> List:
        sorted = defaultdict(lambda: [])
        for atom in model:
            sorted[int(str(atom.arguments[0]))].append(atom)

        return sorted[min(sorted.keys())]

    def _solve(self, ctl, timeout) -> Tuple[object, List, int, bool]:
        models = []
        with ctl.solve(async_=True, on_model=lambda model: models.append(model.symbols(shown=True))) as handle:
            tim = time.time()
            condition = time.time() - tim < timeout if timeout else True
            while condition:
                term = handle.wait(1)
                condition = time.time() - tim < timeout if timeout else not term
            if not term:
                handle.cancel()
        
            return handle.get(), models, tim, term

    @abstractmethod
    def run(self, timeout=None):
        pass

