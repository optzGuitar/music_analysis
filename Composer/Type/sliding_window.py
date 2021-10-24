from Composer.Service.sliding_window_rule_selector import SlidingWindowRuleSelectorService
from Composer.Type.incremental import Incremental
import clingo

class SlidingWindow(Incremental):
    def __init__(self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,
        key="(0,(major,ionian))",
        add_pattern_incrementally=False,
        max_window_size=None,
        ):
        super().__init__(range, random_heuristics=random_heuristics, composer_files=composer_files, parallel_mode=parallel_mode, key=key, add_pattern_incrementally=add_pattern_incrementally)
        self._rule_selector_service = SlidingWindowRuleSelectorService()
        self._max_window_size = max_window_size

    def ground(self, from_timestep: int, to_timestep: int):
        """Grounds the composition."""

        pattern_lengths = self._models_per_length.keys()
        max_len = max(pattern_lengths) if pattern_lengths else None

        rules = self._rule_selector_service.select(from_timestep, to_timestep)
        rules.extend(self._models_per_length[max_len][-1].get_notes() if max_len is not None else [])

        self._add_basic_atoms(from_timestep, to_timestep)

        if rules:
            self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", []), ("step", [clingo.Number(self._iteration)])])
        self._iteration += 1
