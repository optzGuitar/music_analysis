from ASPI import ASP_to_MIDI
from Composer.Service.incremental_rule_selector import IncrementalRuleSelector
from Composer.Type.base import CompositionBase
from Data.composer_model import ComposerModel
from typing import DefaultDict, List, Optional, Tuple
import clingo

from clingo.solving import Model
from Data.pattern import Pattern
from .simple import Composition
from collections import defaultdict


class Incremental(Composition):
    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode="1,compete",  # x,{split;compete},
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
        self.setup_ctl()

        self._models_per_length: DefaultDict[int, List[ComposerModel]] = defaultdict(
            list
        )
        self._iteration = 0
        self._add_pattern_incrementally = add_pattern_incrementally
        self._rule_selector_service = IncrementalRuleSelector()

        self._curr_model: Optional[ComposerModel] = None
        self._last_length: Optional[int] = None

    @property
    def ModelsPerLength(self):
        return self._models_per_length

    @property
    def SequenceLength(self):
        return super().SequenceLength

    @property
    def Current_Model(self) -> Optional[ComposerModel]:
        return super().Current_Model

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
        comp_model = ComposerModel(model, self._last_length)
        self._curr_model = comp_model

        self._models_per_length[comp_model.Length].append(comp_model)

    def ground(self, from_timestep: int, to_timestep: int, chain_models=True):
        """Grounds the composition."""

        if self._curr_model:
            self._last_length = self._curr_model.Length

        if self._add_pattern_incrementally:
            rules = self._rule_selector_service.get_rules_for_length_incremental(
                to_timestep)
        else:
            rules = self._rule_selector_service.get_rules_for_length(
                to_timestep)

        if not rules:
            x = 1

        self._add_basic_atoms(from_timestep, to_timestep)
        self._add_old_models(chain_models)

        if rules:
            self._ctl.add("step", [str(self._iteration)], "".join(rules))
        self._ctl.ground(
            [("base", []), ("step", [clingo.Number(self._iteration)])])
        self._iteration += 1

    def generate(self, timeout=None) -> Tuple[clingo.SolveResult, ComposerModel]:
        return super().generate(timeout)

    def _add_basic_atoms(self, from_timestep: int, to_timestep: int):
        self._ctl.add("base", [],
                      f"positions({self._iteration},{from_timestep}..{to_timestep})."
                      )
        self._ctl.add("base", [],
                      f"keys(0,{from_timestep}..{to_timestep},{self._key})."
                      )
        self._ctl.add("base", [],
                      f"range({self._range[0]}..{self._range[1]}).")
        self._ctl.add("base", [], "track(0).")

        self._ctl.add("base", [], "".join(self._general_atoms))

    def _add_old_models(self, chain: bool):
        if chain:
            for models in self._models_per_length.values():
                self._ctl.add("base", [], models[-1].to_rules())
        elif self._models_per_length:
            self._ctl.add("base", [], list(
                self._models_per_length.values())[-1][-1].to_rules(False))

    def add_patterns(self, patterns: List[Pattern], track=0):
        for pattern in patterns:
            self._rule_selector_service.pattern_per_length[len(
                pattern.items)].append((pattern, track))
        self.NumPatterns += len(patterns)
        self._patterns += patterns

    def from_composition(self, other: CompositionBase):
        self.add_patterns(other._patterns)
        super().from_composition(other)

    def save(self, path):
        """
        Saves the current model to a file.
        Parameters
        ----------
        path : str
            The path to a file for saving the current model.
        """
        with open(path, "w") as file:
            model_string = [
                f"{s}.\n" for s in self._curr_model._raw_model
            ]
            file.writelines(model_string)

    def save_midi(self, path):
        """
        Saves a MIDI file of the Current_Model.
        Parameters
        ----------
        path : str
            The path to the file.
        """
        mido_obj = ASP_to_MIDI(
            "".join([f"{s}." for s in self._curr_model._raw_model]), quiet=True
        )
        mido_obj.save(path)
