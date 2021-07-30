from Data.sign_enumeration import SignEnumeration
from Data.item import Item
from Data.pattern import Pattern
from Miner.job import Job
from Miner.Cleanup.circular_patterns import CircularPatternCleanup
from Miner.strategy import (
    STRATEGY_FREQUENT,
    STRATEGY_NEGATIVE,
    STRATEGY_CONNECTED_MINIMAL_RARE,
)
from Data.pattern_type import PatternType
import os
from deepdiff import DeepDiff


mining_result = {
    STRATEGY_CONNECTED_MINIMAL_RARE: {
        5: [],
        6: [],
        -3: [
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "7", sign=SignEnumeration.POS),
                    Item(3, "7", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "7", sign=SignEnumeration.POS),
                    Item(3, "-5", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "2", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "-5", sign=SignEnumeration.POS),
                    Item(3, "-5", sign=SignEnumeration.POS),
                    Item(4, "-5", sign=SignEnumeration.POS),
                    Item(5, "-5", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "-7", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign=SignEnumeration.POS),
                    Item(2, "-5", sign=SignEnumeration.POS),
                    Item(3, "7", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "-5", sign=SignEnumeration.POS),
                    Item(2, "2", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "-7", sign=SignEnumeration.POS),
                    Item(2, "7", sign=SignEnumeration.POS),
                    Item(3, "7", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "2", sign=SignEnumeration.POS),
                    Item(2, "7", sign=SignEnumeration.POS),
                    Item(3, "-5", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
            Pattern(
                [
                    Item(1, "-5", sign=SignEnumeration.POS),
                    Item(2, "-5", sign=SignEnumeration.POS),
                    Item(3, "-5", sign=SignEnumeration.POS),
                    Item(4, "7", sign=SignEnumeration.POS),
                    Item(5, "-5", sign=SignEnumeration.POS),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
                True,
                3,
            ),
        ],
    },
    STRATEGY_FREQUENT: {
        5: [
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                    Item(7, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                5,
                False,
                None,
            ),
        ],
        6: [
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                    Item(7, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                    Item(7, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                    Item(7, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                6,
                False,
                None,
            ),
        ],
        -3: [
            Pattern(
                [
                    Item(1, "10", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "10", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                    Item(3, "-14", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "10", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                    Item(3, "9", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "3", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "3", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                    Item(3, "9", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "3", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                    Item(3, "-14", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-10", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-7", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-3", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "2", sign=SignEnumeration.POS),
                    Item(2, "-4", sign=SignEnumeration.POS),
                ],
                PatternType.POSITIVE,
                3,
                True,
                None,
            ),
        ],
    },
    STRATEGY_NEGATIVE: {
        5: [
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(1, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,2)", sign=SignEnumeration.POS),
                    Item(6, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,2)", sign=SignEnumeration.POS),
                    Item(5, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,2)", sign=SignEnumeration.POS),
                    Item(4, "(1,4)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                5,
                False,
                None,
            ),
        ],
        6: [
            Pattern(
                [
                    Item(1, "(1,2)", sign=SignEnumeration.POS),
                    Item(1, "(0,1)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(1, "(0,1)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(1, "(1,2)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign=SignEnumeration.POS),
                    Item(1, "(0,1)", sign=SignEnumeration.NEG),
                    Item(1, "(1,2)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(1, "(1,4)", sign=SignEnumeration.NEG),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(0,1)", sign=SignEnumeration.NEG),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(1, "(1,4)", sign=SignEnumeration.NEG),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(1, "(1,4)", sign=SignEnumeration.NEG),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(0,1)", sign=SignEnumeration.NEG),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(0,1)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(1, "(1,4)", sign=SignEnumeration.NEG),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(0,1)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(0,1)", sign=SignEnumeration.NEG),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign=SignEnumeration.POS),
                    Item(2, "(1,2)", sign=SignEnumeration.POS),
                    Item(2, "(0,1)", sign=SignEnumeration.NEG),
                    Item(3, "(1,2)", sign=SignEnumeration.POS),
                    Item(3, "(0,1)", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                6,
                False,
                None,
            ),
        ],
        -3: [
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "10", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "3", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "10", sign=SignEnumeration.NEG),
                    Item(1, "3", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "4", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "10", sign=SignEnumeration.NEG),
                    Item(1, "4", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "3", sign=SignEnumeration.NEG),
                    Item(1, "4", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "10", sign=SignEnumeration.NEG),
                    Item(1, "3", sign=SignEnumeration.NEG),
                    Item(1, "4", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "12", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "10", sign=SignEnumeration.NEG),
                    Item(1, "12", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
            Pattern(
                [
                    Item(1, "-14", sign=SignEnumeration.POS),
                    Item(1, "3", sign=SignEnumeration.NEG),
                    Item(1, "12", sign=SignEnumeration.NEG),
                ],
                PatternType.NEGATIVE,
                3,
                True,
                None,
            ),
        ],
    },
}


def test_basic_mining_and_cleanup():
    minejob = Job(positions=[3, 5, 6])
    minejob.Parameters["minneg"] = 1
    minejob.Parameters["maxneg"] = 3
    minejob.Parameters["minsup"] = 2
    minejob.Parameters["maxsup"] = 5
    minejob.Parameters["patlenmin"] = 2
    minejob.Parameters["patlenmax"] = 7
    minejob.Parameters["maxdist"] = 3

    minejob.Strategies.append(STRATEGY_CONNECTED_MINIMAL_RARE)
    minejob.Strategies.append(STRATEGY_FREQUENT)
    minejob.Strategies.append(STRATEGY_NEGATIVE)

    FILEPATH = "./test_examples/simple/"
    for (_, _, filenames) in os.walk(FILEPATH):
        minejob.MusicFiles.extend([os.path.join(FILEPATH, fn) for fn in filenames])
        break

    minejob.convert_pieces()
    minejob.convert_to_intervals()
    minejob.remove_note()
    minejob.run_methods([f"{10}"])

    dict_diff = DeepDiff(mining_result, minejob.Results)
    assert dict_diff.to_dict() == {}

    minejob.cleanup(CircularPatternCleanup, ignore_unsat=True)
