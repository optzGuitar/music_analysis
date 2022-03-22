import time
from typing import Dict, Optional, Pattern

import clingo
from .base import CompositionBase


class OptimizedComposition(CompositionBase):
    """
    This handles the Positive and negative patterns as optimization criterias.
    Dosent work wont fix.
    """

    def __init__(
        self,
        range,
        composer_files=None,
        parallel_mode=None,  # x,{split;compete}
        key="(0,(major,ionian))",
        random_heuristics=False,
        positive_optimized=True,
        negative_optimized=False,
        intervals_optimized=True,
    ):
        """
        Creates a new composition with optimization.
        Parameters
        ----------
        random_heuristics  : bool
            If true the solver uses random heuristics
        positive_optimized : bool
            If true (default) the number of positive patterns used is optimized.
        negative_optimized : bool
            If true (defualt: false) the number of negative pattern used if optimized.
        """
        super().__init__(range, random_heuristics, composer_files, parallel_mode, key)
        self._curr_model = []
        self._positive_optimized = positive_optimized
        self._negative_optimized = negative_optimized
        self._intervals_optimized = intervals_optimized

    def ground(self, error_head=False) -> Optional[Dict[str, Pattern]]:
        self._general_atoms.append(f"positions(0..{self.Time_Max}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(f"keys(0,0..{self.Time_Max},{self._key}).")
        self._general_atoms.append(
            f"range({self._range[0]}..{self._range[1]}).")

        rules = []
        pos_rules = 0
        err_count = 0
        rule_translate = {}
        for pattern in self._patterns:
            body = pattern.to_rule_body()
            head = f"error({err_count})" if error_head else ""
            if pattern.is_negative:
                c = "~" if self._negative_optimized and not error_head else "-"
                end = "[-1]" if self._negative_optimized and not error_head else ""
                rules.append(f"{head}:{c} {body}. {end}")
            else:
                c = "~" if self._positive_optimized and not error_head else "-"
                end = "[-1]" if self._positive_optimized and not error_head else ""
                rules.append(f"z({pos_rules}) :- {body}.")
                rules.append(f"{head}:{c} not z({pos_rules}). {end}")
                pos_rules += 1

            if error_head:
                rule_translate[f"error({err_count})"] = pattern
                err_count += 1

        if error_head:
            rules.append("#minimize { 1,E : error(E) }.")
            rules.append("#show error/1.")

        self._ctl.add("base", [], "".join(self._general_atoms))
        self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", [])])

        if error_head:
            return rule_translate

    def generate(self, timeout):
        """
        Generates a new musical piece.
        """

        self._ctl.configuration.solve.models = 0
        self._ctl.configuration.solve.opt_mode = "opt"

        def model_handler(model):
            self._curr_model.append(model.symbols(shown=True))

        with self._ctl.solve(async_=True, on_model=model_handler) as handle:
            tim = time.time()
            while time.time() - tim < timeout:
                print(f"Optimizing since {time.time() - tim:.0f}s", end="\r")
                if handle.wait(1):
                    if handle.get().exhausted:
                        break
            handle.cancel()
            print(f"                                         ", end="\r")
            return handle.get(), self._curr_model[-1]

    def validate(self, timeout=120, remove=True):
        """
        self._range,
            composer_files=self._composer_files,
            key=self._key,
            parallel_mode=self._ctl.configuration.solve.parallel_mode,
            random_heuristics=self._rand_heur,
            negative_optimized=True
        """

        rule_translate = self.ground(True)
        res, model = self.generate(timeout)
        self.setup_ctl()

        if res.satisfiable:
            if remove:
                for symb in model:
                    if symb.match("error", 1):
                        self._patterns.remove(
                            rule_translate[str(symb)])
            problem_rules = []
            m = []
            for symb in model:
                if symb.match("error", 1):
                    problem_rules.append(rule_translate[str(symb)])
                else:
                    m.append(symb)
            self._curr_model = m
            return problem_rules, res, m, self._ctl
        return [], None, [], self._ctl
