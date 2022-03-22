from collections import defaultdict
from curses import window
import time
from typing import List, Optional, Tuple

import clingo
from ASPI import ASP_to_MIDI
from Composer.Type.base import CompositionBase

from Composer.Type.incremental import Incremental
from Composer.Type.sliding_window import SlidingWindow
from Data.composer_model import ComposerModel
from Miner.job import Job


class IncrementalSlidingWindow(Incremental):
    def __init__(self, range, step_window: int, reset_window: int, max_generation_time: Optional[float] = None, random_heuristics=False, composer_files=None, parallel_mode="1,compete", key="(0,(major,ionian))", add_pattern_incrementally=False):
        super().__init__(range, random_heuristics, composer_files,
                         parallel_mode, key, add_pattern_incrementally)

        self._step_window = step_window
        self._reset_window = reset_window
        self._max_generation_time = max_generation_time

        self._iteration = 0
        self._delta_iteration = 0

        self._last_step_time = 0
        self._just_resetted = True, True

        self._models: List[ComposerModel] = []
        self._curr_model: Optional[ComposerModel] = None

    def step(self, solve_timeout=None) -> Tuple[clingo.SolveResult, Optional[ComposerModel]]:
        from_ = self._iteration * self._step_window
        to_ = (self._iteration + 1) * self._step_window - 1

        if self._models:
            self._models.pop()

        if self._should_reset():
            self._models.append(self._curr_model)
            self._reset()

            individual_atoms = self._get_window_model(from_)
            self._ctl.add('base', [], "".join(individual_atoms))

        start = time.perf_counter()

        self.ground(from_, to_, False)
        res, self._curr_model = self.generate(solve_timeout)
        self._models.append(self._curr_model)

        stop = time.perf_counter()
        self._last_step_time = stop - start

        self._iteration += 1
        self._delta_iteration += 1
        self._just_resetted = self._just_resetted[1], False

        return res, self._curr_model

    def _should_reset(self) -> bool:
        base = False

        if self._max_generation_time is not None and not self._just_resetted[0]:
            base = base or self._max_generation_time < self._last_step_time

        return base or self._reset_window <= self._delta_iteration * self._step_window

    def _add_old_models(self, chain: bool):
        pass

    def _reset(self):
        self.setup_ctl()
        self._rule_selector_service._grounded_rules = 0
        self._rule_selector_service._grounded_length = self._reset_window
        self._last_step_time = 0
        self._delta_iteration = 0
        self._just_resetted = True, True

    def _get_window_model(self, from_: int) -> List[str]:
        window_notes = [
            i
            for i in self._curr_model.get_window(
                max([from_ - self._iteration * self._reset_window, 0]),
                from_,
            )
        ]

        return [i for note in window_notes for i in note.to_individual_atoms()]

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
                f"{s}.\n" for model in self._models for s in model._raw_model
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
            "".join([f"{s}." for model in self._models for s in model._raw_model]), quiet=True
        )
        mido_obj.save(path)
