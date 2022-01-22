from typing import List
from Composer.Service.rule_selector_base import RuleSelectorBase
from functools import lru_cache


class SlidingWindowRuleSelectorService(RuleSelectorBase):
    def select(self, end: int) -> List[str]:
        rules: List[str] = []
        pattern_lengths_to_ground = [
            x for x in self.pattern_per_length if x <= end
        ]

        for length in pattern_lengths_to_ground:
            rules += self._get_rules_for_length(length)

        return rules

    @lru_cache(maxsize=None)
    def _get_rules_for_length(self, length: int) -> List[str]:
        rules = []

        for pattern, track in self.pattern_per_length[length]:
            rules += self._create_rule(pattern, track, length)

        return rules
