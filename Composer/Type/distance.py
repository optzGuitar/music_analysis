from .base import Composition
import random

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