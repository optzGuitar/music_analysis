from typing import List
from Miner.strategy import STRATEGY_CONNECTED_MINIMAL_RARE, STRATEGY_CONNECTED_RARE, STRATEGY_FREQUENT, STRATEGY_MINIMAL_RARE, STRATEGY_NEGATIVE, STRATEGY_NEGATIVE_CONNECTED, STRATEGY_RARE
from Miner.strategy import Strategy
from Miner.job import Job
import os
import pathlib
import pytest

EXAMPLE_PATH = os.path.join(pathlib.Path(
    __file__).parent.parent, "/test_examples/simple/")

strategy_data_provider = [
    ([STRATEGY_FREQUENT], False, False),
    ([STRATEGY_FREQUENT], True, False),
    ([STRATEGY_FREQUENT], True, True),

    ([STRATEGY_MINIMAL_RARE], False, False),
    ([STRATEGY_MINIMAL_RARE], True, False),
    ([STRATEGY_MINIMAL_RARE], True, True),

    ([STRATEGY_NEGATIVE], False, False),
    ([STRATEGY_NEGATIVE], True, False),
    ([STRATEGY_NEGATIVE], True, True),

    ([STRATEGY_NEGATIVE_CONNECTED], False, False),
    ([STRATEGY_NEGATIVE_CONNECTED], True, False),
    ([STRATEGY_NEGATIVE_CONNECTED], True, True),

    ([STRATEGY_RARE], False, False),
    ([STRATEGY_RARE], True, False),
    ([STRATEGY_RARE], True, True),

    ([STRATEGY_CONNECTED_RARE], False, False),
    ([STRATEGY_CONNECTED_RARE], True, False),
    ([STRATEGY_CONNECTED_RARE], True, True),

    ([STRATEGY_CONNECTED_MINIMAL_RARE], False, False),
    ([STRATEGY_CONNECTED_MINIMAL_RARE], True, False),
    ([STRATEGY_CONNECTED_MINIMAL_RARE], True, True),
]


@pytest.mark.parametrize(["strategies", "as_intervals", "remove_notes"], strategy_data_provider)
def test_can_mine_strategy(strategies: List[Strategy], as_intervals: bool, remove_notes: bool):
    job = Job()
    job.Strategies.extend(strategies)

    for (_, _, filenames) in os.walk(EXAMPLE_PATH):
        job.MusicFiles.extend([os.path.join(EXAMPLE_PATH, fn)
                              for fn in filenames])
        break

    job.convert_pieces()
    if as_intervals:
        job.convert_to_intervals()
    if remove_notes:
        job.remove_note()
    job.run_methods([f"10"])
