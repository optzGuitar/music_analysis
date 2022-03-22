import os
import pathlib

_parent_dir = pathlib.Path(__file__).parent


def _get_path(fname: str) -> str:
    return str(pathlib.Path(os.path.join(_parent_dir, fname)).resolve())


CIRCULAR = _get_path('circular_pattern.lp')
FREQUENT = _get_path('frequent.lp')
MINIMAL_RARE = _get_path('minimal_rare_pattern.lp')
NEGATIVE_CONNECTED = _get_path('negative_connected.lp')
NEGATIVE = _get_path('negative.lp')
RARE = _get_path('rare_pattern.lp')
CANDIDATE = _get_path('candidate.lp')
CONNECTED_CANDIDATE = _get_path('connected_candidate.lp')
