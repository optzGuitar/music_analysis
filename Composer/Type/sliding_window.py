from typing import List
from Composer.Service.sliding_window_rule_selector import (
    SlidingWindowRuleSelectorService,
)
from Composer.Type.incremental import Incremental
import clingo


class SlidingWindow(Incremental):
    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,
        key="(0,(major,ionian))",
        add_pattern_incrementally=False,
        max_generation_window: int = None,
        max_view_window: int = None,
    ):
        super().__init__(
            range,
            random_heuristics=random_heuristics,
            composer_files=composer_files,
            parallel_mode=parallel_mode,
            key=key,
            add_pattern_incrementally=add_pattern_incrementally,
        )
        self._rule_selector_service = SlidingWindowRuleSelectorService()
        self._max_generation_size = max_generation_window
        self._max_view_window = max_view_window

    # TODO: implement true window
    # TODO: override model handler to handle the generated partial compositions

    def ground(self):
        """Grounds the composition."""
        from_ = self._iteration * self._max_generation_size
        to_ = from_ + self._max_generation_size

        pattern_lengths = self._models_per_length.keys()
        max_len = max(pattern_lengths) if pattern_lengths else None

        rules = self._rule_selector_service.select(to_)
        if max_len is not None:
            rules += self._get_window_model(max_len)

        self._add_basic_atoms(from_, to_)

        if rules:
            self._ctl.add("base", [], "".join(rules))
        self._ctl.ground(
            [("base", []), ("step", [clingo.Number(self._iteration)])])
        self._iteration += 1

    def _get_window_model(self, model_length: int) -> List[str]:
        return [
            str(i)
            for i in self._models_per_length[model_length][-1].get_window(
                (self._iteration - 1) * self._max_view_window,
                self._iteration * self._max_view_window,
            )
        ]
