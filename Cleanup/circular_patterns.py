from Data.pattern import Pattern
from typing import List, Tuple
import clingo
from Miner import ENCODING_BASEPATH
from time import time
from Data.logger import cleanup_log
from .cleanup_base import CleanupBase


class CircularPatternCleanup(CleanupBase):
    # TODO: modify so that the result is the difference from all patterns - (not choosen circular)
    def run(self, timeout=None) -> Tuple[object, List]:
        ctl = clingo.Control()
        ctl.add('base', [], '\n'.join(self._str_patterns))
        ctl.load(str(ENCODING_BASEPATH.joinpath('./circular_pattern.lp')))
        time_s = time()
        ctl.ground([('base', [])])
        time_e = time()
        print(f'Grounding took: {time_e - time_s:.3}')

        cleanup_log.info("Starting cleanup by removing circular patterns")
        time_s = time()
        sat, models, tim, term = self._solve(ctl, timeout)
        time_e = time()
        print(f'Solving took: {time_e - time_s:.3}')
        cleanup_log.info(
            f"{'Finished' if term else 'Stopped'} after {tim-time():.1f}s")
        cleanup_log.info(f"Found {len(models)} circular patterns")

        cleaned_patterns = self._get_difference(models)

        print(
            f"Got {len(self._patterns)} and finished with {len(cleaned_patterns)}")
        return sat, cleaned_patterns
