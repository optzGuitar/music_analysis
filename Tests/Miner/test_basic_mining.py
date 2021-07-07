from Data.item import Item
from Data.pattern import Pattern
from Miner.job import Job
from Miner.Cleanup.circular_patterns import CircularPatternCleanup
from Miner.strategy import Strategy
from Data.pattern_type import PatternType
import os
from deepdiff import DeepDiff
from Miner.strategy import 


mining_result = {
    Strategy('con_min_rare', PatternType.CONNECTED | PatternType.POSITIVE): {
        5: [],
        6: [],
        -3: [
            Pattern(
                [
                    Item(1, "-5", sign="pat"),
                    Item(2, "-5", sign="pat"),
                    Item(3, "-5", sign="pat"),
                    Item(4, "7", sign="pat"),
                    Item(5, "-5", sign="pat"),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "-7", sign="pat"), Item(2, "-5", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "2", sign="pat"),
                    Item(2, "-5", sign="pat"),
                    Item(3, "-5", sign="pat"),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "7", sign="pat"),
                    Item(2, "-5", sign="pat"),
                    Item(3, "7", sign="pat"),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "2", sign="pat"),
                    Item(2, "-5", sign="pat"),
                    Item(3, "7", sign="pat"),
                ],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "-5", sign="pat"), Item(2, "-7", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "-5", sign="pat"), Item(2, "2", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "-7", sign="pat"), Item(2, "-7", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "7", sign="pat"), Item(2, "-7", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "7", sign="pat"), Item(2, "2", sign="pat")],
                PatternType.CONNECTED | PatternType.POSITIVE,
                3,
            ),
        ],
    },
    Strategy('frequent', PatternType.POSITIVE): {
        5: [
            Pattern(
                [Item(1, "(1,4)", sign="pat"), Item(2, "(1,2)", sign="pat")],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [Item(1, "(1,2)", sign="pat"), Item(2, "(1,2)", sign="pat")],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                    Item(7, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                5,
            ),
        ],
        6: [
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                    Item(7, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                    Item(7, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                    Item(7, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                ],
                PatternType.POSITIVE,
                6,
            ),
        ],
        -3: [
            Pattern(
                [Item(1, "10", sign="pat"), Item(2, "-4", sign="pat")],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "10", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "-14", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "10", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "9", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "3", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "9", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "3", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "-14", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "3", sign="pat"), Item(2, "-4", sign="pat")],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-10", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "9", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [Item(1, "-10", sign="pat"), Item(2, "-4", sign="pat")],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-3", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "9", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-3", sign="pat"),
                    Item(2, "-4", sign="pat"),
                    Item(3, "-14", sign="pat"),
                ],
                PatternType.POSITIVE,
                3,
            ),
        ],
    },
    Strategy('neg_freq', PatternType.NEGATIVE): {
        5: [
            Pattern(
                [Item(1, "(1,2)", sign="pat"), Item(1, "(1,4)", sign="neg")],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(3, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(4, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(5, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(6, "(1,2)", sign="pat"),
                    Item(6, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(3, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(5, "(1,2)", sign="pat"),
                    Item(5, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
            Pattern(
                [
                    Item(1, "(1,2)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(4, "(1,2)", sign="pat"),
                    Item(4, "(1,4)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                5,
            ),
        ],
        6: [
            Pattern(
                [Item(1, "(1,2)", sign="pat"), Item(1, "(0,1)", sign="neg")],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [Item(1, "(1,4)", sign="pat"), Item(1, "(0,1)", sign="neg")],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [Item(1, "(1,4)", sign="pat"), Item(1, "(1,2)", sign="neg")],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(1,4)", sign="pat"),
                    Item(1, "(0,1)", sign="neg"),
                    Item(1, "(1,2)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(1, "(1,4)", sign="neg"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(0,1)", sign="neg"),
                    Item(3, "(1,2)", sign="pat"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(1, "(1,4)", sign="neg"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(1, "(1,4)", sign="neg"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(0,1)", sign="neg"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(3, "(0,1)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(1, "(1,4)", sign="neg"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(3, "(0,1)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(0,1)", sign="neg"),
                    Item(3, "(1,2)", sign="pat"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
            Pattern(
                [
                    Item(1, "(0,1)", sign="pat"),
                    Item(2, "(1,2)", sign="pat"),
                    Item(2, "(0,1)", sign="neg"),
                    Item(3, "(1,2)", sign="pat"),
                    Item(3, "(0,1)", sign="neg"),
                ],
                PatternType.NEGATIVE,
                6,
            ),
        ],
        -3: [
            Pattern(
                [Item(1, "-14", sign="pat"), Item(1, "10", sign="neg")],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [Item(1, "-14", sign="pat"), Item(1, "3", sign="neg")],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "10", sign="neg"),
                    Item(1, "3", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [Item(1, "-14", sign="pat"), Item(1, "12", sign="neg")],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "10", sign="neg"),
                    Item(1, "12", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "3", sign="neg"),
                    Item(1, "12", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "10", sign="neg"),
                    Item(1, "3", sign="neg"),
                    Item(1, "12", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [Item(1, "-14", sign="pat"), Item(1, "4", sign="neg")],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "10", sign="neg"),
                    Item(1, "4", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
            ),
            Pattern(
                [
                    Item(1, "-14", sign="pat"),
                    Item(1, "3", sign="neg"),
                    Item(1, "4", sign="neg"),
                ],
                PatternType.NEGATIVE,
                3,
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

    #TODO: cleanup refactor; change FilePath to FilePaths in Strategy; finish incremental solving; write test
    minejob.Strategies[
        Strategy("con_min_rare", PatternType.POSITIVE | PatternType.CONNECTED)
    ] = [
        "./Miner/encodings/connected_candidate.lp",
        "./Miner/encodings/minimal_rare_pattern.lp",
    ]
    minejob.Strategies[Strategy("frequent", PatternType.POSITIVE)] = [
        "./Miner/encodings/frequent.lp"
    ]
    minejob.Strategies[Strategy("neg_freq", PatternType.NEGATIVE)] = [
        "./Miner/encodings/negative_patterns.lp"
    ]

    FILEPATH = "./test_examples/simple/"
    for (dirpath, dirnames, filenames) in os.walk(FILEPATH):
        minejob.MusicFiles.extend([os.path.join(FILEPATH, fn) for fn in filenames])
        break

    minejob.convert_pieces()
    minejob.convert_to_intervals()
    minejob.remove_note()
    minejob.run_methods([f"{10}"])

    dict_diff = DeepDiff(minejob.Results, mining_result)
    assert dict_diff.to_dict() == {}

    minejob.cleanup(CircularPatternCleanup, ignore_unsat=True)
