import clingo
import random
import re
from ASPI import ASP_to_MIDI
import Miner
from Miner.ptypes import PatType
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
            ["./Composer/new/notes.lp"] if composer_files == None else composer_files
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
        self._ctl.configuration.solve.parallel_mode = (
            parallel_mode if parallel_mode != None else "1,compete"
        )
        for file in self._composer_files:
            self._ctl.load(file)

        self._curr_model = []
        self._time_max = 16
        self._seq_distance = None
        self._range = (range[0], range[1])
        self._orig_pos_to_atom = {
            3: "chosennote",
            4: "chosenvel",
            5: "chosenlength",
            6: "chosendist",
        }
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
            joined_body = ",".join(body)
            if type:
                rules.append(f":- {joined_body}.")
            else:
                rules.append(f"z{pos_rules} :- {joined_body}.")
                rules.append(f":- not z{pos_rules}.")
                pos_rules += 1

        #with open("./add_rules.lp", "w") as file:
        #    file.writelines(rules)
        #    file.writelines(self._general_atoms)

        self._ctl.add("base", [], "".join(self._general_atoms))
        self._ctl.add("base", [], "".join(rules))
        self._ctl.ground([("base", [])])

    def generate(self, timeout=None):
        """
        Generates a new musical piece.
        """

        def model_handler(model):
            self._curr_model = model.symbols(shown=True)

        with self._ctl.solve(async_=True, on_model=model_handler) as handle:
            term = handle.wait(timeout)
            if not term:
                handle.cancel()
            # yield in future with .resume()? How does .resume work??
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
        rules = []
        pos_rules = 0
        err_count = 0
        rule_translate = {}
        for body, type in self._additional_rules:
            joined_body = ",".join(body)
            if type:
                rules.append(f"error({err_count}) :- {joined_body}.")
                rule_translate[f"error({err_count})"] = (body, True)
                err_count += 1
            else:
                rules.append(f"z{pos_rules} :- {joined_body}.")
                rules.append(f"error({err_count}) :- not z{pos_rules}.")
                rule_translate[f"error({err_count})"] = (body, False)
                err_count += 1
                pos_rules += 1

        rules.append(f"positions(0..{self.Time_Max}).")
        rules.append(f"track(0).")
        rules.append(f"keys(0,0,{self.Time_Max},{self._key}).")
        rules.append(f"range({self._range[0]}..{self._range[1]}).")
        rules.append("#minimize { 1,E : error(E) }.")
        rules.append("#show error/1.")
        #with open("./val_rules.lp", "w") as file:
        #    file.writelines(rules)
        #    file.writelines(self._general_atoms)
        val_ctl = clingo.Control(["0", "--opt-mode=opt"])
        val_ctl.add("base", [], "".join(rules))
        val_ctl.add("base", [], "".join(self._general_atoms))
        for file in self._composer_files:
            val_ctl.load(file)

        models = []
        val_ctl.ground([("base", [])])
        with val_ctl.solve(
            on_model=lambda x: models.append(x.symbols(shown=True)), async_=True
        ) as handle:
            while timeout > 0:
                time.sleep(5)
                timeout -= 5
                try:
                    if val_ctl.statistics["summary"]["exhausted"] == 1:
                        break
                except RuntimeError:
                    pass
            handle.cancel()
            res = handle.get()
        # with val_ctl.solve(
        #     on_model=lambda x: models.append(x.symbols(shown=True)),
        #     yield_=True,
        #     async_=True,
        # ) as handle:
        # time1 = time()
        # wres = handle.wait(timeout - (time() - time1))
        # for model in handle:
        #     models.append(model)
        #     wres = handle.wait(timeout - (time() - time1))
        #     print(f"{wres}  {timeout - (time() - time1):2f}")

        # handle.cancel()
        # res = handle.get()
        # print(f"Number of found models: {len(models)}")
        if res.satisfiable:
            if remove:
                for symb in models[-1]:
                    if symb.match("error", 1):
                        self._additional_rules.remove(rule_translate[str(symb)])
            problem_rules = []
            m = []
            for symb in models[-1]:
                if symb.match("error", 1):
                    problem_rules.append(rule_translate[str(symb)])
                else:
                    m.append(symb)
            self._curr_model = m
            return problem_rules, res, m, val_ctl
        return [], None, [], val_ctl

    def addPositivePatterns(self, patterns, orig_pos, track=0, distance=None):
        """
        Adds a list of positive patterns to the composition.
        Parameters
        ----------
        patterns : list
            A list containing multiple patterns
        orig_pos : int
            The position inside the original note atom for which these patterns were generated.
        """
        for pattern in patterns:
            joined_pattern = self._pos_pattern_to_composer(pattern, orig_pos, track)
            if distance != None:
                joined_pattern = self._to_connected(joined_pattern, distance)
            self._additional_rules.append((joined_pattern, False))
        self.NumPatterns += len(patterns)

    def addNegativePatterns(self, patterns, orig_pos, track=0, distance=None):
        """
        Adds a list of negative patterns to the composition.
        Parameters
        ----------
        patterns : list
            A list containing multiple patterns
        orig_pos : int
            The position inside the original note atom for which these patterns were generated.
        """

        for pattern in patterns:
            joined_pattern = self._neg_pattern_to_composer(pattern, orig_pos, track)
            if distance != None:
                joined_pattern = self._to_connected(joined_pattern, distance)
            self._additional_rules.append((joined_pattern, True))
        self.NumPatterns += len(patterns)

    def addIntervalPatterns(
        self, patterns, orig_pos, track=0, neg=False, distance=None
    ):
        for pattern in patterns:
            if neg:
                body = self._neg_pattern_to_composer(
                    pattern, orig_pos, track, intervals=True
                )
                if distance != None:
                    body = self._to_connected(body, distance)
                self._additional_rules.append((body, True))
            else:
                body = self._pos_pattern_to_composer(
                    pattern, orig_pos, track, intervals=True
                )
                if distance != None:
                    body = self._to_connected(body, distance)
                self._additional_rules.append((body, False))
        self.NumPatterns += len(patterns)

    def _pos_pattern_to_composer(self, pattern, orig_pos, track=0, intervals=False):
        """
        Converts the pat atoms into play atoms. Play atoms get generated by the composition encoding.
        pattern : list
            The pattern to be converted into play atoms
        orig_pos : int
            The position inside the original note atom for which this pattern was generated.
        """
        sorted_pattern = sorted(pattern)
        p = 0
        body = []

        for atom in sorted_pattern:
            if atom.match("support", 1):
                continue
            atom_info = str(atom.arguments[1])

            if not intervals:
                body.append(
                    f"{self._orig_pos_to_atom[orig_pos]}({track},P{p},{atom_info})"
                )
            else:
                body.append(f"{self._orig_pos_to_atom[orig_pos]}({track},P{p},I{p})")
                body.append(f"I{p+1}-I{p}={atom_info}")
            body.append(f"P{p}<P{p+1}")

            p += 1

        del body[-1]
        if intervals:
            del body[-1]
        if self._seq_distance != None:
            body.append(f"P{p-1}-P0 <= {self._seq_distance},P{p-1}-P0>0")

        return body

    def _neg_pattern_to_composer(self, pattern, orig_pos, track=0, intervals=False):
        def split_atoms():
            pos = []
            neg = []
            for i in pattern:
                if i.match("pat", 2):
                    pos.append(i)
                elif i.match("neg", 2):
                    neg.append(i)

            pos = sorted(pos)
            neg = sorted(neg)
            combined = []
            for i in pos:
                combined.append(i)
                p = str(i.arguments[0])
                while len(neg) != 0 and str(neg[0].arguments[0]) == p:
                    combined.append(neg.pop())

            return combined

        sorted_pattern = split_atoms()
        p = 0
        body = []
        curr_neg_pos = []

        for atom in sorted_pattern:
            if atom.match("support", 1):
                continue
            atom_s = str(atom)

            atm = str(atom.arguments[1]) if not intervals else f"I{p}"
            if atom.match("pat", 2):
                if not curr_neg_pos:
                    if p > 0:
                        body.append(f"P{p}>P{p-1}")
                    if intervals and p > 0:
                        body.append(f"I{p}-I{p-1}={atm}")
                else:
                    for pos in curr_neg_pos:
                        body.append(f"P{p}>P{pos}")
                        if intervals:
                            body.append(f"I{p}-I{p-1}={atm}")
                    curr_neg_pos.clear()

                body.append(f"{self._orig_pos_to_atom[orig_pos]}({track},P{p},{atm})")

            elif atom.match("neg", 2):
                atm = str(atom.arguments[1]) if not intervals else f"I{p}"
                if not curr_neg_pos:
                    body.append(
                        f"{self._orig_pos_to_atom[orig_pos]}({track},P{p},{atm})"
                    )
                    body.append(f"P{p}>P{p-1}")
                    if intervals:
                        body.append(f"I{p}-I{p-1}={atm}")
                    curr_neg_pos.append(p)
                else:
                    body.append(
                        f"{self._orig_pos_to_atom[orig_pos]}({track},P{p},{atm})"
                    )
                    min_pos = min(curr_neg_pos) - 1
                    body.append(f"P{p}>P{min_pos}")
                    if intervals:
                        body.append(f"I{p}-I{min_pos}={atm}")
                    curr_neg_pos.append(p)

            p += 1

        if self._seq_distance != None:
            body.append(f"P{p-1}-P0 <= {self._seq_distance},P{p-1}-P0>0")

        return body

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

    def import_minejob(self, minejob):
        """
        Easy and convnient way to import a finished job from the Miner packadge.
        Negative Patterns get recognised by "neg" in strategy.
        All pattern are used for track 0!
        Parameters
        ----------
        minejob : Job
            A finished Job from the Miner packadge.
        """
        self._seq_distance = minejob.SequenceLength
        for strat in minejob.Results:
            for pos in minejob.Results[strat]:
                if minejob.Results[strat][pos]:
                    if pos < 0:
                        self.addIntervalPatterns(
                            minejob.Results[strat][pos],
                            pos * -1,
                            0,
                            bool(strat[1] & PatType.NEGATIVE),
                            minejob.Parameters["maxdist"]
                            if bool(strat[1] & PatType.CONNECTED)
                            else None,
                        )
                    elif strat[1] & PatType.NEGATIVE in strat:
                        self.addNegativePatterns(
                            minejob.Results[strat][pos],
                            pos,
                            distance=minejob.Parameters["maxdist"]
                            if bool(strat[1] & PatType.CONNECTED)
                            else None,
                        )
                    else:
                        self.addPositivePatterns(
                            minejob.Results[strat][pos],
                            pos,
                            distance=minejob.Parameters["maxdist"]
                            if bool(strat[1] & PatType.CONNECTED)
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


class OptimizedComposition(Composition):
    """
    This handles the Positive and negative patterns as optimization criterias.
    Dosent work wont fix.
    """

    def __init__(
        self,
        random_heuristics=False,
        positive_optimized=True,
        negative_optimized=False,
        intervals_optimized=True,
    ):
        """
        Creates a new composition with optimization.
        Parameters
        ----------
        random_heuristics  : bool
            If true the solver uses random heuristics
        positive_optimized : bool
            If true (default) the number of positive patterns used is optimized.
        negative_optimized : bool
            If true (defualt: false) the number of negative pattern used if optimized.
        """
        super().__init__(random_heuristics)
        self._positive_optimized = positive_optimized
        self._negative_optimized = negative_optimized
        self._intervals_optimized = intervals_optimized

    def addPositivePattern(self, pattern, orig_pos, track=0):
        """
        Adds a positive pattern to the composition.
        Parameters
        ----------
        pattern : list
            A list of all the pat atoms of the pattern.
        orig_pos : int
            The position inside the original note atom for which this pattern was generated.
        """
        joined_pattern = self._pos_pattern_to_composer(pattern, orig_pos, track)
        c = "~" if self._positive_optimized else "-"
        end = "[-1]" if self._positive_optimized else ""
        self._additional_rules.append((joined_pattern, False))

    def addNegativePattern(self, pattern, orig_pos, track=0):
        """
        Adds a negative pattern to the composition.
        Parameters
        ----------
        pattern : list
            A list of all the pat atoms of the pattern.
        orig_pos : int
            The position inside the original note atom for which this pattern was generated.
        """
        joined_pattern = self._neg_pattern_to_composer(pattern, orig_pos, track)
        c = "~" if self._negative_optimized else "-"
        end = "[1]" if self._negative_optimized else ""
        self._additional_rules.append([f":{c} {joined_pattern}. {end}"])

    def addIntervalPattern(self, pattern, orig_pos, track=0, neg=False):
        pos = len(self._additional_atoms)
        if neg:
            body = self._neg_pattern_to_composer(
                pattern, orig_pos, track, intervals=True
            )
            if self._intervals_optimized:
                self._additional_rules([f":~ {body}. [1]"])
            else:
                self._additional_rules.append([f":- {body}."])
        else:
            body = self._pos_pattern_to_composer(
                pattern, orig_pos, track, intervals=True
            )
            symb = "~" if self._intervals_optimized else "-"
            end = "[-1]" if self._intervals_optimized else ""
            self._additional_rules.append(
                [f"y{pos} :- {body}.", f":{symb} not y{pos}. {end}"]
            )


class DistanceComposition(Composition):
    def std_distance(l1, l2):
        l3 = list(set(l1) & set(l2))  # Intersect
        l4 = list(set(l1) - set(l3))  # Difference
        l5 = list(set(l2) - set(l3))  # Difference
        return len(l4) + len(l5)

    def __init__(
        self,
        range,
        random_heuristics=False,
        composer_files=None,
        parallel_mode=None,  # x,{split;compete}
        key="(0,(major,ionian))",
        norm=std_distance,
    ):
        super().__init__(range, random_heuristics, composer_files, parallel_mode, key)
        self.__norm = norm
        self._distances = {}
        self.__files = []
        self.__midi_atoms = {}
        self.__rules = {}
        self.__rules_per_file = {}
        self.__seq_num_to_file = {}
        self.__reduced_rules = {}

    @property
    def Distances(self):
        return self._distances

    def calculate_distances(self, model=True, normalize=True) -> dict:
        def normalize(atoms):
            normallized = []
            key = 0
            for atm in atoms.split("\n"):
                if "key" in atm:
                    key = int(atm.split(",")[2].strip())
            for atm in atoms.split("\n"):
                mod_atm = atm
                if "note" in atm:
                    sp = atm.split(",")
                    norm_note = int(sp[3].strip()) - key
                    norm_note = (norm_note + 12) if norm_note < 0 else norm_note
                    norm_note %= 12
                    mod_atm = (
                        norm_note,
                        int(sp[4].strip()),
                        (int(sp[5][1:].strip()), int(sp[6][:-1].strip())),
                        (
                            int(sp[7][1:].strip()),
                            int(sp[8].replace(".", "")[:-2].strip()),
                        ),
                    )
                    normallized.append(mod_atm)
            return normallized

        if not model:
            for fl in self.__files:
                self._distances[fl] = {}
                self._distances[fl][fl] = 0
            for i in range(0, len(self.__files)):
                for j in range(i + 1, len(self.__files)):
                    norm = self.__norm(
                        normalize(self.__midi_atoms[self.__files[i]]),
                        normalize(self.__midi_atoms[self.__files[j]]),
                    )
                    self._distances[self.__files[i]][self.__files[j]] = norm
                    self._distances[self.__files[j]][self.__files[i]] = norm
        else:
            self._distances["model"] = {}
            self._distances["model"]["model"] = 0
            for fl in self.__files:
                norm = self.__norm(
                    normalize("\n".join([str(i) for i in self._curr_model])),
                    normalize(self.__midi_atoms[fl]),
                )
                self._distances[fl]["model"] = norm
                self._distances["model"][fl] = norm

        return self.Distances

    def reduce_presence(
        self, file, ammount=10, pos_chooser=lambda x: random.randrange(0, len(x))
    ):
        if ammount:
            for itm in range(ammount):
                pos = pos_chooser(self.__rules_per_file[file])
                red_itm = self.__rules_per_file[file].pop(pos)
                self.__reduced_rules[file].append(red_itm)
        else:
            pos = pos_chooser(self.__rules_per_file[file])
            while pos != None:
                red_itm = self.__rules_per_file[file].pop(pos)
                self.__reduced_rules[file].append(red_itm)
                pos = pos_chooser(self.__rules_per_file[file])
        self.NumPatterns -= ammount

    def increase_preasence(self, file, ammount=10, allow_mining=True):
        remaining = ammount
        if self.__reduced_rules[file]:
            for itm in range(
                len(self.__reduced_rules[file])
                if len(self.__reduced_rules[file]) < ammount
                else ammount
            ):
                self.__rules_per_file[file].append(self.__reduced_rules[file].pop())
            remaining -= itm
        if remaining:
            if allow_mining:
                pass
        self.NumPatterns += ammount

    def ground(self):
        for file in self.__rules_per_file:
            self._additional_rules += self.__rules_per_file[file]
        for file in self.__midi_atoms:
            self._general_atoms += self.__midi_atoms[file]
        super().ground()

    def validate(self, timeout=300, remove=True):
        for file in self.__rules_per_file:
            self._additional_rules += self.__rules_per_file[file]
        problem_rules, res, model, control = super().validate(
            timeout=timeout, remove=False
        )
        if remove:
            for rule in problem_rules:
                for file in self.__rules_per_file:
                    if rule in self.__rules_per_file[file]:
                        self.__rules_per_file[file].remove(rule)
        self.calculate_distances()
        return problem_rules, res, model, control

    def addPositivePatterns(self, patterns, orig_pos, supports, track=0):
        for i in range(len(patterns)):
            body = self._pos_pattern_to_composer(patterns[i], orig_pos, track)
            for supp in supports[i]:
                self.__rules_per_file[self.__seq_num_to_file[supp]].append(
                    (body, False)
                )
        self.NumPatterns += len(patterns)

    def addNegativePatterns(self, patterns, orig_pos, supports, track=0):
        for i in range(len(patterns)):
            body = self._pos_pattern_to_composer(patterns[i], orig_pos, track)
            for supp in supports[i]:
                self.__rules_per_file[self.__seq_num_to_file[supp]].append((body, True))
        self.NumPatterns += len(patterns)

    def addIntervalPatterns(self, patterns, orig_pos, supports, track=0, neg=False):
        for i in range(len(patterns)):
            if neg:
                body = self._neg_pattern_to_composer(patterns[i], orig_pos, track, True)
                for sup in supports[i]:
                    self.__rules_per_file[self.__seq_num_to_file[sup]].append(
                        (body, True)
                    )
            else:
                body = self._pos_pattern_to_composer(patterns[i], orig_pos, track, True)
                for sup in supports[i]:
                    self.__rules_per_file[self.__seq_num_to_file[sup]].append(
                        (body, False)
                    )
        self.NumPatterns += len(patterns)

    def import_minejob(self, minejob):
        def filter_supports(anssets):
            supps = []
            other = []
            pos = 0
            for ansset in anssets:
                supps.append([])
                other.append([])
                for symb in ansset:
                    if symb.match("support", 1):
                        supps[pos].append(int(str(symb.arguments[0])))
                    else:
                        other[pos].append(symb)
                pos += 1
            return other, supps

        self.__files = minejob.MusicFiles
        for file in self.__files:
            self.__rules_per_file[file] = []
            self.__reduced_rules[file] = []

        self.__midi_atoms = minejob.MidiAtoms
        self.calculate_distances(model=False)
        self._seq_distance = minejob.SequenceLength
        self.__seq_num_to_file = minejob.SeqNumToFile

        for strat in minejob.Results:
            for pos in minejob.Results[strat]:
                pat, supp = filter_supports(minejob.Results[strat][pos])
                if minejob.Results[strat][pos]:
                    if pos < 0:
                        self.addIntervalPatterns(
                            pat, pos * -1, supp, neg="neg" in strat
                        )
                    elif "neg" in strat:
                        self.addNegativePatterns(pat, pos, supp)
                    else:
                        self.addPositivePatterns(pat, pos, supp)

        for file in minejob.MidiAtoms:
            self.addFacts(minejob.MidiAtoms[file])

    def plot_distances(self, save_figure=None):
        def filter_split(st):
            if "/" in st:
                st = "".join(st.split("/")[-1])
            if "." in st:
                st = "".join(st.split(".")[:-1])
            return st

        import matplotlib.pyplot as plt
        import networkx as nx

        graph = nx.Graph()
        for file in self.Distances:
            fl = filter_split(file)
            for weight in self.Distances[file]:
                wei = filter_split(weight)
                graph.add_edge(
                    fl, wei, weight=self.Distances[file][weight],
                )
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=1000)
        nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")
        nx.draw_networkx_edges(graph, pos, width=6)
        nx.draw_networkx_edge_labels(graph, pos)
        plt.axis("off")
        if save_figure:
            plt.savefig(save_figure)
        plt.show()

