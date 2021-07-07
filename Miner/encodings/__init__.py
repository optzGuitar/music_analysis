import os
import pathlib

_parent_dir = pathlib.Path(__file__).parent

def _get_path(fname: str):
    return pathlib.Path(os.path.join(_parent_dir, fname))

CIRCULAR = _get_path('circular_pattern.lp')
FREQUENT = _get_path('frequent.lp')
MINIMAL_RARE = _get_path('minimal_rare_pattern.lp')
NEGATIVE_CONNECTED = _get_path('negative_connected.lp')
NEGATIVE = _get_path('negative.lp')
RARE = _get_path('rare_pattern.lp')
