from Data.pattern_type import PatternType
from Data.pattern import Pattern
from Data.item import Item
import pytest
from Composer.Type.incremental import Incremental


def _get_mining_result():
    return {
        3: [
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5), Item(4, 7)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
            Pattern(
                [Item(1, 2), Item(2, 4), Item(3, 5), Item(4, 7), Item(5, 9)],
                PatternType.POSITIVE,
                3,
                False,
                None,
            ),
        ]
    }


def _get_midi_atoms():
    return [
        "note(0,0,0,3,100,(1,4),(0,1)).",
        "note(0,0,0,4,100,(1,4),(1,4)).",
        "note(0,0,0,5,100,(1,4),(1,4)).",
        "note(0,0,0,6,100,(1,4),(1,4)).",
        "note(0,0,0,7,100,(1,4),(1,4)).",
        "note(0,0,0,8,100,(1,4),(1,4)).",
        "track(0).",
        "key(0,0,0,(major,aeolian)).",
    ]


def test_iterative_solving():
    composer = Incremental((0, 10))
    composer.Time_Max = 100
    composer.add_patterns(_get_mining_result()[3])
    composer.add_facts(_get_midi_atoms())
    composer.ground(0, 2)
    res = composer.generate()

    for i in range(3, composer.Time_Max, 4):
        assert res[0].satisfiable
        composer.ground(i, i + 3)
        res = composer.generate()

    assert composer.Current_Model != []


def test_interative_rule_adding():
    composer = Incremental((0, 10), add_pattern_incrementally=True)
    composer.Time_Max = 100
    composer.SequenceLength = 16
    composer.add_patterns(_get_mining_result()[3])
    composer.add_facts(_get_midi_atoms())
    composer.ground(0, 2)
    res = composer.generate()

    for i in range(3, composer.Time_Max, 4):
        assert res[0].satisfiable
        composer.ground(i, i + 3)
        res = composer.generate()

    assert composer.Current_Model != []
