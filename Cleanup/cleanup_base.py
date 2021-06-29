from Data.id_pattern import IdPattern
import clingo
from Data.pattern_type import PatternType
from collections import defaultdict
from typing import Dict, List, Tuple
from Miner.type import Type
from Data.pattern import Pattern
import time
from abc import ABC, abstractmethod


class CleanupBase(ABC):
    def __init__(self, patterns: List[Pattern], type: PatternType, position: int, elimination_strategy=None):
        self._elimination_strategy = elimination_strategy if elimination_strategy is not None else self._take_lowest_id
        self._type = type
        self._position = position
        self._models = []

        self._str_patterns = []
        self._patterns = []
        for i, p in enumerate(patterns):
            pattern = IdPattern.from_pattern(i, p)
            self._str_patterns.append(str(pattern))
            self._patterns.append(pattern)

    @staticmethod
    def _take_lowest_id(model: List) -> List:
        sorted = defaultdict(lambda: [])
        for atom in model:
            sorted[int(str(atom.arguments[0]))].append(atom)

        return sorted[min(sorted.keys())]

    def _model_handler(self, model: clingo.Model):
        self._models.append(model.symbols(shown=True))

    def _solve(self, ctl, timeout) -> Tuple[object, List, int, bool]:
        with ctl.solve(async_=True, on_model=self._model_handler) as handle:
            tim = time.time()
            condition = time.time() - tim < timeout if timeout else True
            while condition:
                term = handle.wait(1)
                condition = time.time() - tim < timeout if timeout else not term
            if not term:
                handle.cancel()
        
            return handle.get(), self._models, tim, term

    @abstractmethod
    def run(self, timeout=None) -> List[Pattern]:
        raise NotImplementedError("The run method needs to be implemented by the subclass!")

    def _get_difference(self, models) -> List[Pattern]:
        all_pattern_set = set(self._patterns)
        if models and models[0]:
            for model in models:
                chosen_pattern = IdPattern(self._elimination_strategy(model), self._type, self._position)
                chosen = set([chosen_pattern])
                model_set = set(IdPattern.from_model(model, self._type, self._position))
                unselected = model_set - chosen
                all_pattern_set -= unselected
        else:
            return self._patterns

        return list(all_pattern_set)

