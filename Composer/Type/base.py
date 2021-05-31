import clingo
import random
import re
from ASPI import ASP_to_MIDI
from Data.pattern_type import PatternType
import time

class Composition:
    """
    This is the main class for controling the composition process.
    """

    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,  # x,{split;compete}
        key="(0,(major,ionian))",
    ):
        """
        Creates a new composition.
        Parameters
        ----------
        range : iterable
            Any iterable with at least two entries. The first is used a the lower bound and the second as the upper bound for composing.
        random_heuristics : bool
            If true the solver will use random heuristics to find solutions.
        composer_files : list or None
            If None the default composer files will be loaded. Otherwise the files in the list will be loaded.
        """
        self._additional_rules = []
        self._general_atoms = []
        self._composer_files = (
            ["./Composer/asp/notes.lp"] if composer_files is None else composer_files
        )

        if random_heuristics:
            # stolen from Flavio Everado :D
            clingo_args = [
                "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s" % random.randint(0, 32767),
                "--restart-on-model",
                "--enum-mode=record",
            ]
        else:
            clingo_args = None

        self._ctl = clingo.Control(clingo_args)
       # self._ctl.configuration.solve.parallel_mode = (
       #     parallel_mode if parallel_mode != None else "1,compete"
       # )
        for file in self._composer_files:
            self._ctl.load(file)

        self._rand_heur = random_heuristics
        self._curr_model = []
        self._time_max = 16
        self._seq_distance = None
        self._range = (range[0], range[1])

        self._orig_pos_to_space = {
            3: "range",
            4: "velocities",
            5: "lengths",
            6: "distances",
        }
        self._key = key
        self.NumPatterns = 0

    @property
    def Current_Model(self):
        """The last found stable model."""
        return self._curr_model

    @property
    def Time_Max(self):
        """The number of notes to be composed"""
        return self._time_max

    @Time_Max.setter
    def Time_Max(self, value):
        """
        Sets the number of notes to be composed.
        Parameters
        ----------
        value : int
            The number of notes the composer should create.
        """
        self._time_max = value

    @property
    def SequenceLength(self):
        """
        The range of each pattern.
        """
        return self._seq_distance

    @SequenceLength.setter
    def SequenceLength(self, value):
        """
        Sets the range for each pattern
        Parameters
        ----------
        value : int
            The range for each pattern
        """
        self._seq_distance = value

    @property
    def Key(self):
        return self._key

    @Key.setter
    def Key(self, value):
        self._key = value

    def rules_from_file(self, path):
        self._ctl.load(path)

    def ground(self):
        """Grounds the composition."""

        self._general_atoms.append(f"positions(0..{self.Time_Max}).")
        self._general_atoms.append(f"track(0).")
        self._general_atoms.append(f"keys(0,0,{self.Time_Max},{self._key}).")
        self._general_atoms.append(f"range({self._range[0]}..{self._range[1]}).")

        rules = []
        pos_rules = 0
        for body, type in self._additional_rules:
            if type:
                rules.append(f":- {body}.")
            else:
                rules.append(f"z{pos_rules} :- {body}.")
                rules.append(f":- not z{pos_rules}.")
                pos_rules += 1

        self._ctl.add("base", [], "".join(self._general_atoms))
        self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", [])])

    def generate(self, timeout=None):
        """
        Generates a new musical piece.
        """
        #TODO: add found model as no-good and implement yield

        def model_handler(model):
            self._curr_model = model.symbols(shown=True)

        with self._ctl.solve(async_=True, on_model=model_handler) as handle:
            tim = time.time()
            condition = time.time() - tim < timeout if timeout else True
            while condition:
                print(f"Generating since {time.time() - tim:.0f}s", end="\r")
                term = handle.wait(1)
                condition = time.time() - tim < timeout if timeout else not term
            if not term:
                handle.cancel()
            
            print("                                        ", end="\r")
            return handle.get(), self._curr_model

    def save(self, path):
        """
        Saves the current model to a file.
        Parameters
        ----------
        path : str
            The path to a file for saving the current model.
        """
        with open(path, "w") as file:
            model_string = [f"{s}." for s in self._curr_model]
            file.writelines(model_string)

    def validate(self, timeout=120, remove=True):

        #TODO: remodel dependency tree
        optComp = OptimizedComposition(
            self._range,
            composer_files=self._composer_files,
            key=self._key,
            parallel_mode=self._ctl.configuration.solve.parallel_mode,
            random_heuristics=self._rand_heur,
            negative_optimized=True,
        )
        optComp.from_composition(self)

        rule_translate = optComp.ground(True)
        res, model = optComp.generate(timeout)

        if res.satisfiable:
            if remove:
                for symb in model:
                    if symb.match("error", 1):
                        self._additional_rules.remove(rule_translate[str(symb)])
            problem_rules = []
            m = []
            for symb in model:
                if symb.match("error", 1):
                    problem_rules.append(rule_translate[str(symb)])
                else:
                    m.append(symb)
            self._curr_model = m
            return problem_rules, res, m, optComp._ctl
        return [], None, [], optComp._ctl

    def from_composition(self, other):
        self._additional_rules = other._additional_rules
        self._general_atoms = other._general_atoms
        self.Time_Max = other.Time_Max
        self._key = other._key
        self._range = other._range

    def addPatterns(self, patterns, intervals, track=0, distance=None):
        for pattern in patterns:
            body = pattern.to_rule_body(track, intervals, self._seq_distance)
            if distance != None:
                body = self._to_connected(body, distance)
            self._additional_rules.append((body, bool(pattern.type & PatternType.NEGATIVE)))
        self.NumPatterns += len(patterns)

    def _to_connected(self, composer_pattern, distance=1):
        def get_pos(pattern):
            rgx = re.findall("P[0-9]+", " ".join(pattern))
            return sorted(list(set(rgx)))

        pos = get_pos(composer_pattern)

        for pos, pos2 in zip(pos[:-1], pos[1:]):
            composer_pattern.append(f"{pos2}-{pos}<={distance}")

        return composer_pattern

    def addFacts(self, facts):
        """
        Adds multiple facts to the composition.
        facts : str or list
            The facts to be added.
        """
        if type(facts) == str:
            facts = facts.split(".")[:-1]
            facts = [f.strip() + "." for f in facts]
        for fact in facts:
            if "(" in fact and "key" == fact.split("(")[0]:
                fact = "keyp" + fact[3:]
            elif "(" in fact and "note" == fact.split("(")[0]:
                fact = "notep" + fact[4:]
            elif "(" in fact and "track" == fact.split("(")[0]:
                fact = "trackp" + fact[5:]
            self._general_atoms.append(fact)

    def import_minejob(self, minejob, filter_patterns=False):
        """
        Easy and convnient way to import a finished job from the Miner packadge.
        Negative Patterns get recognised by "neg" in strategy.
        All pattern are used for track 0!
        Parameters
        ----------
        minejob : Job
            A finished Job from the Miner packadge.
        """
        added_patterns = []
        whole = 0
        self._seq_distance = minejob.SequenceLength
        for strat in minejob.Results:
            for pos in minejob.Results[strat]:
                patterns = minejob.Results[strat][pos]
                whole += len(patterns)

                if patterns:
                    if filter_patterns:
                        for pat in patterns:
                            if pat in added_patterns:
                                patterns.remove(pat)
                        added_patterns.extend(patterns)
                    self.addPatterns(
                        patterns,
                        pos < 0,
                        distance=minejob.Parameters["maxdist"]
                        if bool(strat[1] & PatternType.CONNECTED)
                        else None,
                    )

        for file in minejob.MidiAtoms:
            self.addFacts(minejob.MidiAtoms[file])

    def save_midi(self, path):
        """
        Saves a MIDI file of the Current_Model.
        Parameters
        ----------
        path : str
            The path to the file.
        """
        mido_obj = ASP_to_MIDI(
            "".join([f"{s}." for s in self.Current_Model]), quiet=True
        )
        mido_obj.save(path)