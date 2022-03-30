from abc import ABC
from collections import defaultdict
from typing import List, Tuple

from Data.pattern import Pattern
from Data.pattern_type import PatternType


class RuleSelectorBase(ABC):
    def __init__(self) -> None:
        self._grounded_rules: int = 0
        self.pattern_per_length: defaultdict[
            int, List[Tuple[Pattern, int]]
        ] = defaultdict(list)
        self._grounded_length: int = 0
        self.max_pattern_internal_distance = None

    def _create_positive_constraint(self, pattern: Pattern, track: int, length: int) -> Tuple[str, str]:
        rule_head = f"z{self._grounded_rules}"
        body = pattern.to_rule_body(
            track, self.max_pattern_internal_distance, length,
        )

        rule = f"{rule_head} :- {body}."
        force = f":- not {rule_head}."

        return rule, force

    def _create_negative_constraint(self, pattern: Pattern, track: int, length: int) -> str:
        return f":- {pattern.to_rule_body(track, self.max_pattern_internal_distance, length)}."

    def _create_rule(self, pattern: Pattern, track: int, length: int) -> List[str]:
        if pattern.type & PatternType.NEGATIVE:
            return [self._create_negative_constraint(pattern, track, length)]
        else:
            rule, force = self._create_positive_constraint(
                pattern, track, length)
            return [rule, force]

    def reset(self, grounded_length: int):
        self._grounded_rules = 0
        self._grounded_length = grounded_length
