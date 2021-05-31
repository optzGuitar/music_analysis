import enum
from enum import Flag


class PatternType(Flag):
    POSITIVE = enum.auto()
    NEGATIVE = enum.auto()
    CONNECTED = enum.auto()
