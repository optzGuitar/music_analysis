from typing import Iterator, Optional, Tuple, Union
import clingo
from clingo.solving import SolveHandle
import time
from .base import CompositionBase

class Composition(CompositionBase):
    """
    This is the most basic class for controling the composition process.
    """

    def ground(self):
        """Grounds the composition."""

        self._general_atoms.append(f"positions(0..{self.Time_Max}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(f"keys(0,0,{self.Time_Max},{self._key}).")
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")

        rules = []
        pos_rules = 0
        for body, type in self._additional_rules:
            if type:
                rules.append(f":- {body}.")
            else:
                rules.append(f"z{pos_rules} :- {body}.")
                rules.append(f":- not z{pos_rules}.")
                pos_rules += 1

        self._ctl.add("base", [], "".join(self._general_atoms))
        self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", [])])

    def generate(self, yield_=True, timeout=None) -> Union[Tuple[clingo.SolveResult, Optional[clingo.Model]], Iterator[clingo.Model]]:
        """
        Generates a new musical piece.
        """
        solve_control = clingo.SolveControl()

        with self._ctl.solve(async_=True, on_model=lambda model: self._model_handler(yield_, model, solve_control)) as handle:
            if yield_:
                for i in  self._iterate(handle, timeout):
                    yield i
            else:
                handle.wait(timeout)
                return handle.get(), handle.model()

    def _itarate(self, handle: SolveHandle, timeout: float) -> clingo.Model:
        tim = time.time()
        condition = time.time() - tim < timeout if timeout else True
        offset = 0
        while condition:
            term = handle.wait(1)
            offset += time.time() - tim
            model = handle.model()
            if model is not None:
                yield model
            offset -= time.time() - tim - offset
            condition = time.time() - tim - offset < timeout if timeout else not term
        if not term:
            handle.cancel()

        return handle.get(), self._curr_model
