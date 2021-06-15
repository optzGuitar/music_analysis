from Composer.Type.base import Composition
import Miner
import argparse
import os
from Data.pattern_type import PatternType
from Miner.type import Type

parser = argparse.ArgumentParser()
parser.add_argument(
    "ans",
    help="the max number of answer sets for each pattern mining encoding (everything over 5 is currently impossible to ground!)",
    default=3,
)
args = parser.parse_args()

# (45, 75) means all notes between 50 and 90 can be chosen (MIDI equivalent)
comp = Composition((45, 75))
comp.Time_Max = 16

minejob = Miner.Job(positions=[3, 5, 6])
# parameters defined in the interface.lp
minejob.Parameters["minneg"] = 1
minejob.Parameters["maxneg"] = 3
minejob.Parameters["minsup"] = 2
minejob.Parameters["maxsup"] = 5
minejob.Parameters["patlenmin"] = 2
minejob.Parameters["patlenmax"] = 7
minejob.Parameters["maxdist"] = 3

# adding the following encodings to be used in pattern mining:
# minimum rare encoding
minejob.Strategies[Type("con_min_rare", PatternType.POSITIVE | PatternType.CONNECTED)] = [
    "./Miner/encodings/connected_candidate.lp",
    "./Miner/encodings/minimal_rare_pattern.lp",
]
# frequent patterns
minejob.Strategies[Type("frequent", PatternType.POSITIVE)] = ["./Miner/encodings/frequent.lp"]
# frequent negative patterns
minejob.Strategies[Type("neg_freq", PatternType.NEGATIVE)] = [
    "./Miner/encodings/negative_patterns.lp"
]

# adding my example midi files
FILEPATH = "./test_examples/simple/"
for (dirpath, dirnames, filenames) in os.walk(FILEPATH):
    minejob.MusicFiles.extend([os.path.join(FILEPATH, fn) for fn in filenames])
    break

# convert midi files into seq atoms and perform pattern mining
print("start of mining process")
minejob.convert_pieces()
minejob.convert_to_intervals()
minejob.remove_note()
minejob.run_methods([f"{args.ans}"])
print("finishhed mining process")

