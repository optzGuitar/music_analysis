from typing import List
from clingo import Model

from Data.note import Note


class ComposerModel:
    def __init__(self, model: Model) -> None:
        self._raw_model = model.symbols(shown=True)
        self._notes: List[Note] = []
        self._keys = []
        self._tracks = []

        for symbol in model.symbols(shown=True):
            if symbol.match('note', 7):
                self._notes.append(Note.from_symbol(symbol))
            elif symbol.match('keys', 3):
                self._keys.append(symbol)
            elif symbol.match('track', 1):
                self._tracks.append(symbol)

    @property
    def Length(self) -> int:
        return len(self._notes)

    def to_rules(self) -> str:
        return f'm({self.Length}) :- {", ".join([str(i) for i in self._notes])}.:- not m({self.Length}).'

    def to_individual_note_atoms(self) -> List[str]:
        return [atm for atm in (note.to_individual_atoms() for note in self._notes)]

    def get_notes(self) -> List[str]:
        return [f'{i}.' for i in self._notes]

    def get_window(self, from_timestep: int, to_timestep: int) -> List[Note]:
        return [i for i in self._notes if i.is_played_between(from_timestep, to_timestep)]
