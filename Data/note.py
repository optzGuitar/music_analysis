from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional
import clingo

from Data.note_atoms import NoteAtoms


@dataclass
class Note:
    track: int
    position: int
    channel: int
    pitch: int
    velocity: int
    length: Fraction
    distance: Fraction

    symbol: Optional[clingo.Symbol] = None

    @classmethod
    def from_symbol(cls, note: clingo.Symbol) -> Note:
        args = note.arguments
        return cls(
            track=args[0].number,
            position=args[1].number,
            channel=args[2].number,
            pitch=args[3].number,
            velocity=args[4].number,
            length=Fraction(args[5].arguments[0].number,
                            args[5].arguments[1].number),
            distance=Fraction(args[6].arguments[0].number,
                              args[5].arguments[1].number),
            symbol=note,
        )

    def __str__(self) -> str:
        return f"note({self.track},{self.position},{self.channel},{self.pitch},{self.velocity}," \
            f"({self.length.numerator},{self.length.denominator}),({self.distance.numerator},{self.distance.denominator}))."

    def to_individual_atoms(self) -> List[str]:
        return [
            self._construct_atom(NoteAtoms.NOTE_ATOM, str(self.pitch)),
            self._construct_atom(NoteAtoms.VELOCITY_ATOM, str(self.velocity)),
            self._construct_atom(
                NoteAtoms.LENGTH_ATOM, f"({self.length.numerator},{self.length.denominator})"),
            self._construct_atom(
                NoteAtoms.DISTANCE_ATOM, f"({self.distance.numerator},{self.distance.denominator})")
        ]

    def _construct_atom(self, atom: NoteAtoms, value: str) -> str:
        return f"{atom.value}({self.track},{self.position},{value})"

    def is_played_between(self, from_timestep: int, to_timestep: int) -> bool:
        return from_timestep <= self.position <= to_timestep
