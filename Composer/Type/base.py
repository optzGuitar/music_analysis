from Data.pattern import Pattern
from Miner.job import Job
from Miner.strategy import Strategy
from typing import Iterator, List, Optional, Tuple, Union
import clingo
import random
import re
from clingo.solving import Model
from ASPI import ASP_to_MIDI
from Data.pattern_type import PatternType
from abc import ABC, abstractmethod


class CompositionBase(ABC):
    """
    This is the main class for controling the composition process.
    """

    def __init__(
        self,
        range: Tuple[int, int],
        random_heuristics: bool = False,
        composer_files: Optional[List[str]] = None,
        parallel_mode: Optional[str] = None,  # x,{split;compete}
        key: str = "(0,(major,ionian))",
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
        self._additional_rules: List[Tuple[str, bool]] = []
        self._general_atoms: List[str] = []
        self._composer_files = (
            ["./Composer/asp/keys.lp", "./Composer/asp/notes.lp"]
            if composer_files is None
            else composer_files
        )

        # TODO: remove call here as it is of no benefit
        self.setup_ctl(parallel_mode, random_heuristics)

        self._rand_heur = random_heuristics
        self._parallel_mode = parallel_mode
        self._curr_model: List[clingo.Symbol] = []
        self._time_max: int = 16
        self._seq_distance: Optional[int] = None
        self._range = (range[0], range[1])

        self._orig_pos_to_space = {
            3: "range",
            4: "velocities",
            5: "lengths",
            6: "distances",
        }
        self._key = key
        self.NumPatterns: int = 0

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

    def setup_ctl(self, parallel_mode: Optional[str], random_heuristics: bool):
        if random_heuristics:
            # stolen from Flavio Everado :D
            self._clingo_args = [
                "--warn=none",
                "--sign-def=rnd",
                "--sign-fix",
                "--rand-freq=1",
                "--seed=%s" % random.randint(0, 32767),
                "--restart-on-model",
                "--enum-mode=record",
            ]
        else:
            self._clingo_args = []

        self._ctl = clingo.Control(self._clingo_args)
        self._ctl.configuration.solve.parallel_mode = (
            parallel_mode if parallel_mode != None else "1,compete"
        )
        for file in self._composer_files:
            self._ctl.load(file)

    def rules_from_file(self, path):
        self._ctl.load(path)

    @abstractmethod
    def ground(self, *args, **kwargs):
        raise NotImplementedError(
            "This is an abstract method. It has to be implemented in all subclasses."
        )

    def _model_handler(self, model: Model):
        self._curr_model = model.symbols(shown=True)

    @abstractmethod
    def generate(
        self, yield_: bool = True, timeout: Optional[int] = None
    ) -> Union[
        Tuple[clingo.SolveResult, Optional[clingo.Model]], Iterator[clingo.Model]
    ]:
        raise NotImplementedError(
            "This is an abstract method. It has to be implemented in all subclasses."
        )

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

    def from_composition(self, other):
        self._additional_rules = other._additional_rules
        self._general_atoms = other._general_atoms
        self.Time_Max = other.Time_Max
        self._key = other._key
        self._range = other._range

    def add_patterns(self, patterns: List[Pattern], track=0):
        for pattern in patterns:
            body = pattern.to_rule_body(track, self._seq_distance)
            if pattern.distance != None:
                body = self._to_connected(body, pattern.distance)
            self._additional_rules.append(
                (body, pattern.type & PatternType.NEGATIVE))
        self.NumPatterns += len(patterns)

    def _to_connected(self, composer_pattern, distance=1):
        def get_pos(pattern):
            rgx = re.findall("P[0-9]+", " ".join(pattern))
            return sorted(list(set(rgx)))

        pos = get_pos(composer_pattern)

        for pos, pos2 in zip(pos[:-1], pos[1:]):
            composer_pattern.append(f"{pos2}-{pos}<={distance}")

        return composer_pattern

    def add_facts(self, facts):
        """
        Adds multiple facts to the composition.
        facts : str or list
            The facts to be added.
        """
        if isinstance(facts, str):
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

    def import_minejob(self, minejob: Job):
        """
        Easy and convenient way to import a finished job from the Miner package.
        Negative Patterns get recognized by "neg" in strategy.
        All pattern are used for track 0!
        Parameters
        ----------
        minejob : Job
            A finished Job from the Miner package.
        """
        self._seq_distance = minejob.SequenceLength
        strategy: Strategy
        for strategy in minejob.Results:
            for pos in minejob.Results[strategy]:
                patterns = minejob.Results[strategy][pos]

                if patterns:
                    self.add_patterns(
                        patterns,
                    )

        for file in minejob.MidiAtoms:
            self.add_facts(minejob.MidiAtoms[file])

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
