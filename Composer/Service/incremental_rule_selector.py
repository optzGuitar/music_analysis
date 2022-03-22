from Composer.Service.rule_selector_base import RuleSelectorBase
from typing import List


class IncrementalRuleSelector(RuleSelectorBase):
    def get_rules_for_length(self, length: int) -> List[str]:
        rules = []
        pattern_lengths_to_ground = [i for i in self.pattern_per_length.keys()
                                     ]  # if self._grounded_length < i <= length]

        for pat_len in pattern_lengths_to_ground:
            for pattern, track in self.pattern_per_length[pat_len]:
                rules += self._create_rule(pattern, track, length)

                self._grounded_rules += 1

        max_len = self._grounded_length
        if pattern_lengths_to_ground:
            max_len = max(pattern_lengths_to_ground)
            self._grounded_length = max_len

        return rules

    def get_rules_for_length_incremental(self, length: int) -> List[str]:
        rules = []
        for _, patterns in self.pattern_per_length.items():
            for pattern, track in patterns:
                rules += self._create_rule(pattern, track, length)

                self._grounded_rules += 1

        self._grounded_length = length

        return rules
