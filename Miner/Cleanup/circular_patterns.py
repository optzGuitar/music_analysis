from typing import List, Tuple
import clingo
from Miner import ENCODING_BASEPATH
from Data.logger import cleanup_log
from .cleanup_base import CleanupBase


class CircularPatternCleanup(CleanupBase):
    def run(self, timeout=None) -> Tuple[object, List]:
        ctl = clingo.Control(['0'])
        ctl.add('base', [], '\n'.join(self._str_patterns))
        ctl.load(str(ENCODING_BASEPATH.joinpath('./circular_pattern.lp')))
        ctl.ground([('base', [])])

        cleanup_log.info(f"Starting cleanup of {self._type.Name} by removing circular patterns")
        sat, models, term = self._solve(ctl, timeout)
        cleanup_log.info(f"Found {len(models)} circular patterns in {ctl.statistics['summary']['times']['total']:.2f}s")

        cleaned_patterns = self._get_difference(models)

        cleanup_log.info(
            f"Got {len(self._patterns)} and finished with {len(cleaned_patterns)} patterns")
        return sat, cleaned_patterns
