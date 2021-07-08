import pathlib
from typing import List, Union
from Data.pattern_type import PatternType
from .encodings import FREQUENT, MINIMAL_RARE, NEGATIVE_CONNECTED, NEGATIVE, RARE, CANDIDATE, CONNECTED_CANDIDATE


class Strategy:
    def __init__(self, name: str, pattern_type: PatternType, file_paths: List[Union[pathlib.Path, str]]):
        self.__name = name
        self.__pattern_type = pattern_type
        self.__file_paths = file_paths

    @property
    def Name(self):
        return self.__name

    @property
    def PatternType(self):
        return self.__pattern_type

    @property
    def FilePaths(self):
        return self.__file_paths

    def __hash__(self):
        return hash(f"{self.Name}{self.PatternType}")

    def __eq__(self, other):
        if isinstance(other, Strategy):
            return self.Name == other.Name and self.PatternType == other.PatternType

        return False

    def __repr__(self) -> str:
        return f"Strategy({self.__name}, {self.__pattern_type}, {self.__file_paths})"

STRATEGY_FREQUENT = Strategy('frequent', PatternType.POSITIVE, [FREQUENT])
STRATEGY_MINIMAL_RARE = Strategy('minimum_rare', PatternType.POSITIVE, [MINIMAL_RARE, CANDIDATE])
STRATEGY_NEGATIVE_CONNECTED = Strategy('negative_connected', PatternType.NEGATIVE | PatternType.CONNECTED, [NEGATIVE_CONNECTED])
STRATEGY_NEGATIVE = Strategy('negative', PatternType.NEGATIVE, [NEGATIVE])
STRATEGY_RARE = Strategy('rare', PatternType.POSITIVE, [CANDIDATE, RARE])
STRATEGY_CONNECTED_MINIMAL_RARE = Strategy('connected_minimum_rare', PatternType.CONNECTED | PatternType.POSITIVE, [CONNECTED_CANDIDATE, MINIMAL_RARE])
STRATEGY_CONNECTED_RARE = Strategy('connected_rare', PatternType.CONNECTED | PatternType.POSITIVE, [CONNECTED_CANDIDATE, RARE])
