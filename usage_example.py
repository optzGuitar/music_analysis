import argparse
import os
import time
from Composer.Type.incremental_sliding_window import IncrementalSlidingWindow
from Composer.Type.sliding_window import SlidingWindow

import Miner
from Composer.Type.optimizer import OptimizedComposition
from Miner.Cleanup.circular_patterns import CircularPatternCleanup
from Miner.strategy import STRATEGY_CONNECTED_MINIMAL_RARE, STRATEGY_FREQUENT, STRATEGY_MINIMAL_RARE, STRATEGY_NEGATIVE, STRATEGY_NEGATIVE_CONNECTED

parser = argparse.ArgumentParser()
parser.add_argument(
    "ans",
    help="the max number of answer sets for each pattern mining encoding",
    default=100,
)
args = parser.parse_args()

# (45, 75) means all notes between 45 and 75 can be chosen (MIDI equivalent)
# IncrementalSlidingWindow((45, 75), 10, 500, 1)
# OptimizedComposition((45, 75))
comp = OptimizedComposition((45, 75))
# the length of the composition
comp.Time_Max = 8

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
# frequent patterns
minejob.Strategies.append(STRATEGY_CONNECTED_MINIMAL_RARE)
# minejob.Strategies.append(STRATEGY_MINIMAL_RARE)
minejob.Strategies.append(STRATEGY_NEGATIVE_CONNECTED)

# adding example midi files
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

# this step cleans up the mining result
# sometimes it happens that the same pattern but with a different start is found
# this step remove those patterns
#
# also if you have anything to remove from the mined patterns do it here
#minejob.cleanup(CircularPatternCleanup, timeout=60, ignore_unsat=True)
print("finished mining process")

# import the mined sequences into the Composer and compose music
comp.import_minejob(minejob)
print("finished importing")

# this step ensures that the program is satisfiable by eliminating contradictory rules
comp.validate()
print('finished validating')

comp.save("./_validatedmodel.lp")

comp_ = IncrementalSlidingWindow((45, 75), 10, 500, 500)
comp_.from_composition(comp)
comp = comp_

start = time.time()
for _ in range(5):
    res, _ = comp.step()
    print(f"finished generating {res}")
    print(f"combined: {comp._last_step_time}")

    if res.unsatisfiable:
        break

end_time = time.time()
print(f"took: {end_time - start:.2f} to generate")
print(res)

if str(res) == "SAT":
    comp.save("./model.lp")
    comp.save_midi("./generated_piece.mid")
