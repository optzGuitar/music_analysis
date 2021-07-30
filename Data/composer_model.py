from clingo import Model


class ComposerModel:
    def __init__(self, model: Model) -> None:
        self._raw_model = model
        self._notes = []
        self._keys = []
        self._tracks = []

        for symbol in model.symbols(shown=True):
            if symbol.match('note', 7):
                self._notes.append(symbol)
            elif symbol.match('keys', 3):
                self._keys.append(symbol)
            elif symbol.match('track', 1):
                self._tracks.append(symbol)

    @property
    def Length(self) -> int:
        return len(self._notes)

    def to_rules(self):
        return f'm({self.Length}) :- {", ".join([str(i) for i in self._notes])}.:- not m({self.Length}).'
