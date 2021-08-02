from typing import Optional, Tuple
import clingo
from .base import CompositionBase

class Composition(CompositionBase):
    """
    This is the most basic class for controling the composition process.
    """

    def ground(self):
        """Grounds the composition."""

        self._general_atoms.append(f"positions(0..{self.Time_Max}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(f"keys(0,0..{self.Time_Max},{self._key}).")
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")

        rules = []
        for i, (body, type) in enumerate(self._additional_rules):
            if type:
                rules.append(f":- {body}.")
            else:
                rules.append(f"z{i} :- {body}.")
                rules.append(f":- not z{i}.")

        self._ctl.add("base", [], "".join(self._general_atoms))
        self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", [])])

    def generate(self, timeout=None) -> Tuple[clingo.SolveResult, Optional[clingo.Model]]:
        """
        Generates a new musical piece.
        """
        with self._ctl.solve(async_=True, on_model=lambda model: self._model_handler(model)) as handle:
            res = handle.wait(timeout)
            if not res:
                handle.cancel()
            return (handle.get(), self._curr_model)
