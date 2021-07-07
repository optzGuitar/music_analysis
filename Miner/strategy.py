import pathlib
from Data.pattern_type import PatternType
from .encodings import CIRCULAR, FREQUENT, MINIMAL_RARE, NEGATIVE_CONNECTED, NEGATIVE, RARE


class Strategy:
    def __init__(self, name: str, pattern_type: PatternType, file_path: pathlib.Path):
        self.__name = name
        self.__pattern_type = pattern_type
        self.__file_path = file_path

    @property
    def Name(self):
        return self.__name

    @property
    def PatternType(self):
        return self.__pattern_type

    @property
    def FilePath(self):
        return self.__file_path

    def __hash__(self):
        return hash(f"{self.Name}{self.PatternType}")

    def __eq__(self, other):
        if isinstance(other, Strategy):
            return self.Name == other.Name and self.PatternType == other.PatternType

        return False

    def __repr__(self) -> str:
        return f"Type({self.__name}, {self.__pattern_type}, {self.__file_path})"

STRATEGY_FREQUENT = Strategy('frequent', PatternType.POSITIVE, FREQUENT)
STRATEGY_MINIMAL_RARE = Strategy('minimum_rare', PatternType.POSITIVE, MINIMAL_RARE)
STRATEGY_NEGATIVE_CONNECTED = Strategy('negative_connected', PatternType.NEGATIVE | PatternType.CONNECTED, NEGATIVE_CONNECTED)
STRATEGY_NEGATIVE = Strategy('negative', PatternType.NEGATIVE, NEGATIVE)
STRATEGY_RARE = Strategy('rare', PatternType.POSITIVE, RARE)