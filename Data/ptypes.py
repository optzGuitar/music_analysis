import enum
from enum import Flag


class PatType(Flag):
    POSITIVE = enum.auto()
    NEGATIVE = enum.auto()
    CONNECTED = enum.auto()
