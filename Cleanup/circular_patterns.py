from typing import List, Tuple
import clingo
from Miner import ENCODING_BASEPATH
import time
from Data.logger import cleanup_log
from .cleanup_base import CleanupBase

class CircularPatternCleanup(CleanupBase):
    def _circular_pattern_cleanup(self, timeout=None) -> Tuple[object, List]:

        ctl = clingo.Control()
        ctl.add('pattern', [], '. '.join(self._patterns))
        ctl.load(str(ENCODING_BASEPATH.joinpath('./circular_pattern.lp')))

        cleanup_log.info("Starting cleanup by removing circular patterns")
        sat, models, tim, term = self.__solve(ctl, timeout)
        cleanup_log.info(f"{'Finished' if term else 'Stopped'} after {tim-time.time():.1f}s")
        cleanup_log.info(f"Found {len(models)} circular patterns")

        chosen_patterns = []
        for model in models:
            chosen_patterns.append(self._elimination_strategy(model))

        return sat, chosen_patterns

    def run(self, timeout=None) -> Tuple[object, List]:
        return self._circular_pattern_cleanup(timeout)