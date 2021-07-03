from typing import Iterator, Optional, Tuple, Union

import clingo
from Composer.Type.base import CompositionBase


class Incremental(CompositionBase):
    def __init__(self, range, random_heuristics, composer_files, parallel_mode, key):
        super().__init__(range, random_heuristics=random_heuristics, composer_files=composer_files, parallel_mode=parallel_mode, key=key)
        self._first_ground = True

    def generate(self, yield_: bool, timeout: Optional[int]) -> Tuple[clingo.SolveResult, Optional[clingo.Model]]:
        pass

    def ground(self, from_timestep: int, to_timestep: int):
        """Grounds the composition."""

        self._general_atoms.append(f"positions({from_timestep}..{to_timestep}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(f"keys(0,{from_timestep},{to_timestep},{self._key}).")
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")
        self._ctl.add(f"steps{from_timestep}{to_timestep}", [], "".join(self._general_atoms))
        ground_programs = [(f'steps{from_timestep}{to_timestep}', [])]

        if self._first_ground:
            rules = []
            pos_rules = 0
            for body, type in self._additional_rules:
                if type:
                    rules.append(f":- {body}.")
                else:
                    rules.append(f"z{pos_rules} :- {body}.")
                    rules.append(f":- not z{pos_rules}.")
                    pos_rules += 1

            self._ctl.add("base", [], "".join(rules))
            ground_programs.append(("base", []))
            self._first_ground = False

        self._ctl.ground(ground_programs)
        