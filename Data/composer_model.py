from typing import List, Optional
from clingo import Model

from Data.note import Note


class ComposerModel:
    def __init__(self, model: Model, previous_length: Optional[int] = None) -> None:
        self._raw_model = model.symbols(shown=True)
        self._notes: List[Note] = []
        self._keys = []
        self._tracks = []
        self._previous_length = previous_length

        for symbol in model.symbols(shown=True):
            if symbol.match('note', 7):
                self._notes.append(Note.from_symbol(symbol))
            elif symbol.match('keys', 3):
                self._keys.append(symbol)
            elif symbol.match('track', 1):
                self._tracks.append(symbol)

        self._length = max((note.position for note in self._notes))

    @property
    def Length(self) -> int:
        return self._length

    def to_rules(self) -> str:
        relevant_notes = self._notes
        previous_head = ''

        if self._previous_length:
            relevant_notes = [
                note for note in self._notes if note.position > self._previous_length]
            previous_head = f'm({self._previous_length}),'

        return f'm({self.Length}) :- {previous_head} {", ".join([str(i.symbol) for i in relevant_notes])}.:- not m({self.Length}).'

    def to_individual_note_atoms(self) -> List[str]:
        return [atm for atm in (note.to_individual_atoms() for note in self._notes)]

    def get_notes(self) -> List[str]:
        return [f'{i}.' for i in self._notes]

    def get_window(self, from_timestep: int, to_timestep: int) -> List[Note]:
        return [i for i in self._notes if i.is_played_between(from_timestep, to_timestep)]
