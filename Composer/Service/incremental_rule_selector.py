from Composer.Service.rule_selector_base import RuleSelectorBase
from Data.pattern_type import PatternType
from collections import defaultdict
from Data.pattern import Pattern
from typing import DefaultDict, List, Tuple


class IncrementalRuleSelector(RuleSelectorBase):
    def get_rules_for_length(self, length: int) -> List[str]:
        rules = []
        pattern_lengths_to_ground = list(
            filter(
                lambda x: self._grounded_length <= length and x <= length,
                self.pattern_per_length.keys(),
            )
        )

        for pat_len in pattern_lengths_to_ground:
            for pattern, track in self.pattern_per_length[pat_len]:
                if pattern.type & PatternType.NEGATIVE:
                    rules.append(
                        f":- {pattern.to_rule_body(track, self.max_pattern_internal_distance)}."
                    )
                else:
                    rules.append(
                        f"z{self._grounded_rules} :- {pattern.to_rule_body(track, self.max_pattern_internal_distance)}."
                    )
                    rules.append(f":- not z{self._grounded_rules}.")
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
                if pattern.type & PatternType.NEGATIVE:
                    rules.append(
                        f":- {pattern.to_rule_body(track, self.max_pattern_internal_distance, length)}."
                    )
                else:
                    rule_head = f"z{self._grounded_rules}"
                    body = pattern.to_rule_body(
                        track, self.max_pattern_internal_distance, length,
                    )
                    rule = f"{rule_head} :- {body}."
                    rules.append(rule)
                    rules.append(f":- not {rule_head}.")

                self._grounded_rules += 1

        self._grounded_length = length

        return rules
