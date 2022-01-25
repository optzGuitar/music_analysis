from typing import List, Optional

from ASPI import ASP_to_MIDI
from Composer.Service.sliding_window_rule_selector import (
    SlidingWindowRuleSelectorService,
)
from Composer.Type.incremental import Incremental
import clingo
from Data.composer_model import ComposerModel


class SlidingWindow(Incremental):
    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,
        key="(0,(major,ionian))",
        add_pattern_incrementally=False,
        max_generation_window: int = None,
        max_view_window: int = None,
    ):
        super().__init__(
            range,
            random_heuristics=random_heuristics,
            composer_files=composer_files,
            parallel_mode=parallel_mode,
            key=key,
            add_pattern_incrementally=add_pattern_incrementally,
        )
        self._rule_selector_service = SlidingWindowRuleSelectorService()
        self._max_generation_size = max_generation_window
        self._max_view_window = max_view_window

        self._curr_model: Optional[ComposerModel] = None

    def _model_handler(self, model: clingo.Model):
        comp_model = ComposerModel(model)
        self._curr_model = comp_model
        self._models_per_length[comp_model.Length].append(comp_model)

    def ground(self):
        """Grounds the composition."""
        from_ = self._iteration * self._max_generation_size
        to_ = from_ + self._max_generation_size - 1

        pattern_lengths = self._models_per_length.keys()
        max_len = max(pattern_lengths) if pattern_lengths else None

        rules = self._rule_selector_service.select(to_)
        if max_len is not None:
            rules += (self._get_window_model(from_))

        self._add_basic_atoms(from_, to_)

        if rules:
            self._ctl.add("base", [], "".join(rules))
        self._ctl.ground(
            [("base", []), ("step", [clingo.Number(self._iteration)])])
        self._iteration += 1

    def _get_window_model(self, from_: int) -> List[str]:
        return [
            str(i)
            for i in self._curr_model.get_window(
                max([from_ - self._iteration * self._max_view_window, 0]),
                from_,
            )
        ]

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
            "".join([f"{s}." for s in self.Current_Model._raw_model]), quiet=True
        )
        mido_obj.save(path)
