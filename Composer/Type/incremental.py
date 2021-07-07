from Data.pattern import Pattern
from Miner.strategy import Strategy
from Data.pattern_type import PatternType
from typing import List, Optional, Tuple
import clingo
from Composer.Type.base import CompositionBase
from collections import defaultdict


class Incremental(CompositionBase):
    def __init__(self, range, random_heuristics, composer_files, parallel_mode, key):
        super().__init__(
            range,
            random_heuristics=random_heuristics,
            composer_files=composer_files,
            parallel_mode=parallel_mode,
            key=key,
        )
        self._pattern_per_length = defaultdict(list)
        self._grounded_length = 0
        self._grounded_rules = 0

    def generate(
        self, yield_: bool, timeout: Optional[int]
    ) -> Tuple[clingo.SolveResult, Optional[clingo.Model]]:
        pass

    def ground(self, from_timestep: int, to_timestep: int):
        """Grounds the composition."""

        self._general_atoms.append(f"positions({from_timestep}..{to_timestep}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(
            f"keys(0,{from_timestep},{to_timestep},{self._key})."
        )
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")
        self._ctl.add(
            f"steps{from_timestep}{to_timestep}", [], "".join(self._general_atoms)
        )
        ground_programs = [(f"steps{from_timestep}{to_timestep}", [])]

        rules = []
        pattern_lengths_to_ground = filter(
            lambda x: self._grounded_length <= to_timestep and x <= to_timestep,
            self._pattern_per_length.keys(),
        )

        for pat_len in pattern_lengths_to_ground:
            for body, is_negative in self._pattern_per_length[pat_len]:
                if is_negative:
                    rules.append(f":- {body}.")
                else:
                    rules.append(f"z{self.__grounded_rules} :- {body}.")
                    rules.append(f":- not z{self.__grounded_rules}.")
                    self.__grounded_rules += 1

        if pattern_lengths_to_ground:
            prog_name = f"_".join([f"{i}" for i in pattern_lengths_to_ground])
            self._ctl.add(prog_name, [], "".join(rules))
            ground_programs.append((prog_name, []))
            self._grounded_length = max(pattern_lengths_to_ground)

        self._ctl.ground(ground_programs)

    def add_patterns(
        self, patterns: List[Pattern], areIntervals: bool, track=0, distance=None
    ):
        for pattern in patterns:
            body = pattern.to_rule_body(track, areIntervals, self._seq_distance)
            if distance != None:
                body = self._to_connected(body, distance)
            self._pattern_per_length[len(pattern.items)].append(
                (body, bool(pattern.type & PatternType.NEGATIVE))
            )
        self.NumPatterns += len(patterns)
