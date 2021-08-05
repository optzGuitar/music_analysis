from Composer.Service.sliding_window_rule_selector import SlidingWindowRuleSelectorService
from Composer.Type.incremental import Incremental

class SlidingWindow(Incremental):
    def __init__(self, range, random_heuristics, composer_files, parallel_mode, key, add_pattern_incrementally):
        super().__init__(range, random_heuristics=random_heuristics, composer_files=composer_files, parallel_mode=parallel_mode, key=key, add_pattern_incrementally=add_pattern_incrementally)
        self._rule_selector_service = SlidingWindowRuleSelectorService()

    def ground(self, from_timestep: int, to_timestep: int):
        # TODO: implement
        pass
