from __future__ import annotations
from typing import List, Optional, Set
from clingo import Model
import clingo
from Data.composer_model import ComposerModel


class PartialComposerModel(ComposerModel):
    def __init__(self, model: Model, previous_model: Optional[PartialComposerModel]) -> None:
        super().__init__(model)
        self._previous_model = previous_model

    def get_complete_model(self) -> Set[clingo.Symbol]:
        data = set()
        if self._previous_model is not None:
            data = self._previous_model.get_complete_model()

        data.update(
            [i.symbol for i in self._notes] +
            self._keys +
            self._tracks
        )

        # TODO: some notes/positions are still doubled!

        return data
