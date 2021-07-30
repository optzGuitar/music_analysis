from Data.pattern_type import PatternType
from Data.item import Item
from Data.pattern import Pattern
from Composer.Service.incremental_rule_selector import IncrementalRuleSelector

PATTERN_PER_LENGTH = {
    3: [
        (
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
        (
            Pattern(
                [Item(1, 3), Item(2, 5), Item(3, 6)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
    ],
    4: [
        (
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5), Item(4, 7)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
        (
            Pattern(
                [Item(1, 3), Item(2, 5), Item(3, 6), Item(4, 8)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
    ],
    5: [
        (
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5), Item(4, 7), Item(5, 9)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
        (
            Pattern(
                [Item(1, 3), Item(2, 5), Item(3, 6), Item(4, 8), Item(5, 9)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            0,
        ),
    ],
}

EXPECTED_SELECTION = {
    3: [
        "z0 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z0.",
        "z1 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z1.",
    ],
    4: [
        "z2 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z2.",
        "z3 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z3.",
        "z4 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3.",
        ":- not z4.",
        "z5 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3.",
        ":- not z5.",
    ],
    5: [
        "z6 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z6.",
        "z7 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z7.",
        "z8 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3.",
        ":- not z8.",
        "z9 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3.",
        ":- not z9.",
        "z10 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3,chosennote(0,P4,9),P3<P4.",
        ":- not z10.",
        "z11 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3,chosennote(0,P4,9),P3<P4.",
        ":- not z11.",
    ],
}

EXPECTED_INCREMENTAL = {
    3: [
        "z0 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z0.",
        "z1 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z1.",
        "z2 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z2.",
        "z3 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z3.",
        "z4 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z4.",
        "z5 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z5.",
    ],
    4: [
        "z6 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z6.",
        "z7 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z7.",
        "z8 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3.",
        ":- not z8.",
        "z9 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3.",
        ":- not z9.",
        "z10 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3.",
        ":- not z10.",
        "z11 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3.",
        ":- not z11.",
    ],
    5: [
        "z12 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2.",
        ":- not z12.",
        "z13 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2.",
        ":- not z13.",
        "z14 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3.",
        ":- not z14.",
        "z15 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3.",
        ":- not z15.",
        "z16 :- chosennote(0,P0,2),chosennote(0,P1,4),P0<P1,chosennote(0,P2,5),P1<P2,chosennote(0,P3,7),P2<P3,chosennote(0,P4,9),P3<P4.",
        ":- not z16.",
        "z17 :- chosennote(0,P0,3),chosennote(0,P1,5),P0<P1,chosennote(0,P2,6),P1<P2,chosennote(0,P3,8),P2<P3,chosennote(0,P4,9),P3<P4.",
        ":- not z17.",
    ],
}


def test_get_corrent_rules():
    incremental_rule_selector = IncrementalRuleSelector()
    incremental_rule_selector.max_pattern_internal_distance = 16
    incremental_rule_selector.pattern_per_length = PATTERN_PER_LENGTH

    for length in PATTERN_PER_LENGTH:
        rules = incremental_rule_selector.get_rules_for_length(length)

        assert rules == EXPECTED_SELECTION[length]


def test_get_correct_rules_incremental():
    incremental_rule_selector = IncrementalRuleSelector()
    incremental_rule_selector.max_pattern_internal_distance = 16
    incremental_rule_selector.pattern_per_length = PATTERN_PER_LENGTH

    for length in PATTERN_PER_LENGTH:
        rules = incremental_rule_selector.get_rules_for_length_incremental(length)

        assert rules == EXPECTED_INCREMENTAL[length]
