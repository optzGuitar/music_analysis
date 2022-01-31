import time
from typing import List, Optional, Tuple

import clingo
from ASPI import ASP_to_MIDI

from Composer.Type.incremental import Incremental
from Composer.Type.sliding_window import SlidingWindow
from Data.composer_model import ComposerModel
from Miner.job import Job


class IncrementalSlidingWindow:
    def __init__(self, range: Tuple[int, int], step_window: int, reset_window: int, max_generation_time: Optional[float] = None, **kwargs) -> None:
        self._step_window = step_window
        self._reset_window = reset_window
        self._max_generation_time = max_generation_time

        self._iteration = 0
        self._delta_iteration = 0

        self._custom_args = kwargs
        self._incremental = Incremental(range, **kwargs)
        self._sliding_window = SlidingWindow(
            range, max_generation_window=step_window, max_view_window=reset_window
        )

        self._last_step_time = 0

        self._curr_model: Optional[clingo.Model] = None

    def step(self, solve_timeout=None) -> Tuple[clingo.SolveResult, Optional[ComposerModel]]:
        from_ = self._iteration * self._step_window
        to_ = (self._iteration + 1) * self._step_window - 1

        # BUG: reset results in unsat
        if self._should_reset():
            self._reset()

            notes = self._sliding_window._get_window_model(from_)
            self._incremental._ctl.add('base', [], "".join(notes))

        start = time.perf_counter()

        self._incremental.ground(from_, to_)
        res, self._curr_model = self._incremental.generate(solve_timeout)

        stop = time.perf_counter()
        self._last_step_time = stop - start

        self._iteration += 1
        self._delta_iteration += 1
        self._sync_sliding_window()

        return res, self._curr_model

    def _should_reset(self) -> bool:
        base = False

        if self._max_generation_time is not None:
            base = base or self._max_generation_time < self._last_step_time

        return base or self._reset_window <= self._delta_iteration * self._step_window

    def _reset(self):
        args = {
            'parallel_mode': self._custom_args.get('parallel_mode', None),
            'random_heuristics': self._custom_args.get('random_heuristics', None)
        }

        self._incremental.setup_ctl(**args)
        self._incremental._rule_selector_service._grounded_length = 0
        self._last_step_time = 0
        self._delta_iteration = 0

    def _sync_sliding_window(self):
        self._sliding_window._iteration = self._iteration
        self._sliding_window._curr_model = self._curr_model

    def save(self, path: str):
        self._incremental.save(path)

    def save_midi(self, path: str):
        self._incremental.save_midi(path)

    def import_minejob(self, minejob: Job):
        self._incremental.import_minejob(minejob)
