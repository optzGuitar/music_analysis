from ASPI import MIDI_to_ASP
import clingo
import time
from Data.pattern import Pattern
from .type import Type
from typing import Callable, Dict, List, Optional
from typing import Type as TType
from Miner.Cleanup.cleanup_base import CleanupBase
from Data.logger import miner_log

class Job:
    """
    This class handles the pattern mining step.
    """

    def __init__(self, seqlen=None, positions=[3, 4, 5, 6], additional_params={}):
        """
        Creates a new pattern mining job.
        Parameters
        ----------
        seqlen : int, None
            The length of the sequences to be constructed from the midi files. It is default to None. If seqlen is None a MIDI track is one sequence.
        positions : list
            The are the arguments of the note atom to perform pattern mining on. The int in the list describes to position of the argument inside the note atom.
        additional_params : dict
            This dict should always contain all parameters defined inside the interface.lp. If new ones are added they can be added here.
        """
        self.__parameters = {
            **{
                "patlenmin": 0,
                "patlenmax": 5,
                "minsup": 0,
                "maxsup": 5,
                "minneg": 0,
                "maxneg": 5,
                "maxdist": 5,
            },
            **additional_params,
        }
        self.__atoms = {}
        self.__midi_atoms = {}
        self.__strategies = {}
        self.__results = {}
        self.__seqlen = seqlen
        self.__positions = positions
        self.__music_files = []
        self._results_per_file = {}
        self.__seq_number_to_file = {}
        self.__midi_atoms_per_file = {}

    @property
    def Parameters(self):
        """The dict containing the parateters defined in interface.lp"""
        return self.__parameters

    @property
    def Strategies(self) -> Dict[Type, List[str]]:
        """
        A dict containing all strategies to be used for pattern mining. The key should be the name and the value is a list with all files needed for the strategy.
        The key should be a tuple of the following form: (name : str, pat_type : pattern_types.PatternType)
        """
        return self.__strategies

    @property
    def Results(self):
        """A dict containing the results ordered per strategy. Uses the same keys as Strategies."""
        return self.__results

    @property
    def SequenceLength(self):
        """The length of the to be constructed sequences. If seqlen is None a MIDI track is one sequence."""
        return self.__seqlen

    @property
    def MidiAtoms(self):
        """The MIDI atoms obtained by converting the input MIDI files with ASPI into ASP."""
        return self.__midi_atoms

    @property
    def MusicFiles(self):
        """A list containing all MIDI files needed for this pattern mining job."""
        return self.__music_files

    @property
    def SeqAtoms(self):
        return self.__atoms

    @property
    def SeqNumToFile(self):
        return self.__seq_number_to_file

    def __get_num_tracks(self, atoms):
        seen = []
        for atom in atoms.split("\n"):
            if "note" in atom:
                track = atom.split("(")[1].split(",")[0]
                if not track in seen:
                    seen.append(track)
        return len(seen)

    def convert_pieces(self, options={}) -> None:
        """
        Converts all added musical pieces into sequence atoms.
        Parameters
        ----------
        options : dict
                In this dict one can specifiy special parameters for the MIDI_to_ASP function. The standard is {quiet:True}.
                The keys of the dict are the paths for which one wants the options to be loaded. Each entry should be a list wich gets unpacked while calling MIDI_to_ASP.
                The path to the MIDI file cannot be input here (Add it to the MusicFiles list!).
        """
        for pos in self.__positions:
            self.__atoms[pos] = ""

        seq_number = 0
        for path in self.__music_files:
            self.__midi_atoms_per_file[path] = []
            if path in options:
                atoms = MIDI_to_ASP(path, **options[path])
            else:
                atoms = MIDI_to_ASP(path, quiet=True, **options)
            self.__midi_atoms[path] = atoms

            for pos in self.__positions:
                seq_atoms = self.__convert_index(
                    atoms,
                    pos,
                    self.__seqlen,
                    seq_number if self.__seqlen == None else None,
                )
                self.__midi_atoms_per_file[path] += seq_atoms.split(".")
                self.__atoms[pos] += seq_atoms

            num_tracks = self.__get_num_tracks(self.MidiAtoms[path])
            for i in range(seq_number, num_tracks + seq_number):
                self.__seq_number_to_file[i] = path
            seq_number += num_tracks

        miner_log.info('Converted all peices into atoms')

    def __convert_index(self, atoms, value, length, seq_number=None) -> str:
        """
        Converts note to sequence atoms. Each sequene is length elements long (except the last one!).
        Parameters:
        -----------
        atoms : list
            A list containing all the atoms to parse.
        value : int
            The position in the note atom to fill into the seq atom.
        length : int
            The length of the created sequences.
        Returns:
        --------
        seq_atoms : str
            A string ready to be passen on to clingo containing all sequence atoms.
        """

        if length == None:
            maxpos = 0
            for atm in atoms.split("."):
                if "," in atm:
                    satm = atm.split(",")[1]
                    if int(satm.strip()) > maxpos:
                        maxpos = int(satm.strip())
            length = maxpos + 1

        ctl = clingo.Control(["-c", f"slen={length}"])
        ctl.add("base", [], "#const slen=0.")
        pos_list = ["_" for i in range(7)]
        pos_list[0] = "T"
        pos_list[1] = "P"
        pos_list[value] = "I"
        pos_string = ",".join(pos_list)
        if seq_number == None:
            ctl.add("base", [], f"seq(P/slen+T, P\\slen, I) :- note({pos_string}).")
        else:
            ctl.add(
                "base", [], f"seq({seq_number}+T, P\\slen, I) :- note({pos_string})."
            )
        ctl.add("base", [], atoms)
        ctl.add("base", [], "#show seq/3.")
        ctl.ground([("base", [])])
        model = []
        ctl.solve(on_model=lambda m: model.append(m.symbols(shown=True)))
        if not model:
            model.append([])
        return ". ".join([str(s) for s in model[0]]) + "." if model[0] else ""

    def convert_to_intervals(self, position=3) -> str:
        """
        Converts the given sequence items into interval representation.
        Parameters:
        -----------
        seq_items : str
            The seq atoms to be converted into interval representation.
        Returns:
        --------
        int_atoms : str
            A string containing the new seq atoms ready to be passed on to clingo.
        """
        converter = "seq1(T,S,I'-I) :- seq(T,S,I), seq(T,S+1,I'). #show seq1/3."
        model = []
        ctl = clingo.Control()
        ctl.add("conv", [], converter)
        ctl.add("itms", [], self.__atoms[position])
        ctl.ground([("base", []), ("conv", []), ("itms", [])])
        ctl.solve(on_model=lambda m: model.append(m.symbols(shown=True)))
        model_str = ". ".join([str(i) for i in model[0]]) + "."
        self.__atoms[-1 * position] = model_str.replace("seq1(", "seq(")
        self.__positions.append(-1 * position)

    def remove_note(self):
        self.__atoms.pop(3)
        self.__positions.remove(3)

    def _run_method(
        self, name: Type, position: int, clingo_args:List=[], tout=None, quiet=False, stats=False
    ) -> list:
        result = []
        param_args = []
        for arg in self.Parameters:
            param_args.append("-c")
            param_args.append(f"{arg}={self.Parameters[arg]}")
        control = clingo.Control(clingo_args + param_args)
        control.add("midi", [], self.__atoms[position])
        control.add("base", [], "#show pat/2.")
        for file in self.Strategies[name]:
            control.load(file)
        control.ground([("base", []), ("midi", [])])
        isint = False
        try:
            int(clingo_args[0])
            isint = True
        except:
            pass
        if int(clingo_args[0]) == 0:
            with control.solve(
                on_model=lambda m: result.append(m.symbols(shown=True)), async_=True
            ) as handle:
                while tout > 0:
                    time.sleep(5)
                    tout -= 5
                    try:
                        if control.statistics["summary"]["exhausted"] == 1:
                            break
                    except RuntimeError:
                        pass
                handle.cancel()
                res = handle.get()
        else:
            with control.solve(
                on_model=lambda m: result.append(
                    Pattern(m.symbols(shown=True), name.PatternType, position)
                ),
                async_=True,
            ) as handle:
                handle.wait(tout)
                handle.cancel()
                res = handle.get()

        if not quiet:
            miner_log.info(f"finished {name.Name:9}. Found {len(result)}")

        if stats:
            return (result, control.statistics)
        return result

    def run_methods(
        self, clingo_args=[], timeout=None, stats=False
    ) -> dict:
        """
        Runs all methods and all positions.
        Parameters:
        -----------
        clingo_args : list
            A list containing extra arguments for clingo.
        """
        stat = []
        for strat in self.Strategies:
            self.__results[strat] = {}
            for pos in self.__positions:
                res = self._run_method(
                    strat, pos, clingo_args, tout=timeout, stats=stats
                )
                if stats:
                    self.__results[strat][pos] = res[0]
                    stat.append(res[1])
                else:
                    self.__results[strat][pos] = res

        miner_log.info('Finished all mining methods')
        if stats:
            return (self.Results, stat)
        return self.Results

    def cleanup(self, strategy: TType[CleanupBase], elimination_strategy:Optional[Callable]=None, timeout:Optional[float]=None, ignore_unsat: bool=False):
        miner_log.info('starting cleanup')
        for type, values in self.Results.items():
            for position in values:
                if not self.Results[type][position]:
                    continue
                strat = strategy(self.Results[type][position], type, position, elimination_strategy)
                sat, patterns = strat.run(timeout)
 
                if sat.satisfiable:
                    self.Results[type][position] = patterns
                elif not ignore_unsat:
                    raise RuntimeError("Got UNSAT on cleanup")

        miner_log.info('finished cleanup')
