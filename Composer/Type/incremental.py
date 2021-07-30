from Composer.Service.incremental_rule_selector import IncrementalRuleSelector
from Data.composer_model import ComposerModel
from typing import DefaultDict, Dict, List, Optional, Tuple
import clingo

from clingo.solving import Model
from Data.pattern import Pattern
from Data.pattern_type import PatternType
from .simple import Composition
from collections import defaultdict


class Incremental(Composition):
    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,
        key="(0,(major,ionian))",
        add_pattern_incrementally=False,
    ):
        super().__init__(
            range,
            random_heuristics=random_heuristics,
            composer_files=composer_files,
            parallel_mode=parallel_mode,
            key=key,
        )
        self._composer_files = (
            ["./Composer/asp/keys.lp", "./Composer/asp/notes_incremental.lp"]
            if composer_files is None
            else composer_files
        )
        self.setup_ctl(parallel_mode, random_heuristics)

        self._pattern_per_length: DefaultDict[
            int, List[Tuple[Pattern, int]]
        ] = defaultdict(list)
        self._models_per_length: DefaultDict[int, List[ComposerModel]] = defaultdict(
            list
        )
        self._iteration = 0
        self._add_pattern_incrementally = add_pattern_incrementally
        # holds the pattern and their rule head, this enables me to chain incrementally added rules
        self._incrementally_grounded_patterns: Dict[Pattern, str] = []
        self._rule_selector_service = IncrementalRuleSelector()

    @property
    def ModelsPerLength(self):
        return self._models_per_length

    @property
    def SequenceLength(self):
        return super().SequenceLength

    @SequenceLength.setter
    def SequenceLength(self, value):
        """
        Sets the range for each pattern
        Parameters
        ----------
        value : int
            The range for each pattern
        """
        self._seq_distance = value
        self._rule_selector_service.max_pattern_internal_distance = value

    def _model_handler(self, model: Model):
        symb = model.symbols(shown=True)
        self._curr_model = symb

        comp_model = ComposerModel(model)
        self._models_per_length[comp_model.Length].append(comp_model)

    def ground(self, from_timestep: int, to_timestep: int):
        """Grounds the composition."""

        self._general_atoms.append(
            f"positions({self._iteration},{from_timestep}..{to_timestep})."
        )
        self._general_atoms.append(
            f"keys(0,{from_timestep}..{to_timestep},{self._key})."
        )
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")
        self._general_atoms.append(f"track(0).")

        for _, models in self._models_per_length.items():
            self._ctl.add("base", [], models[-1].to_rules())

        self._ctl.add("base", [], "".join(self._general_atoms))

        if self._add_pattern_incrementally:
            rules = self._rule_selector_service.get_rules_for_length_incremental(to_timestep)
        else:
            rules = self._rule_selector_service.get_rules_for_length(to_timestep)

        if rules:
            self._ctl.add("step", [], "".join(rules))

        self._ctl.ground([("base", []), ("step", [clingo.Number(self._iteration)])])
        self._iteration += 1
                
    def add_patterns(self, patterns: List[Pattern], track=0):
        for pattern in patterns:
            self._rule_selector_service.pattern_per_length[len(pattern.items)].append((pattern, track))
        self.NumPatterns += len(patterns)

    def generate(
        self, timeout=None
    ) -> Tuple[clingo.SolveResult, Optional[clingo.Model]]:
        """
        Generates a new musical piece.
        """

        with self._ctl.solve(
            async_=True, on_model=lambda model: self._model_handler(model)
        ) as handle:
            res = handle.wait(timeout)
            if not res:
                handle.cancel()
            return (handle.get(), self._curr_model)
