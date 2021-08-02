from __future__ import annotations
from Data.sign_enumeration import SignEnumeration
from Data.id_item import IdItem
import clingo
from Data.pattern_type import PatternType
from typing import List
from .pattern import Pattern
from collections import defaultdict

class IdPattern(Pattern):
    def __init__(self, atoms: List[clingo.Symbol], type: PatternType, position: int) -> None:
        items: List[IdItem] = []
        for atm in atoms:
            if atm.match("support", 1):
                continue
            items.append(
                IdItem(
                    int(str(atm.arguments[0])),
                    int(str(atm.arguments[1])),
                    str(atm.arguments[2]),
                    SignEnumeration(str(atm).split("(")[0]),
                )
            )
        items.sort()
        self.items = items
        self.type = type
        self.position = position if position > 0 else position * -1
        self.id = int(str(atoms[0].arguments[0])) if atoms else None

    @staticmethod
    def from_model(model: List[clingo.Symbol], type: PatternType, position: int) -> List[IdPattern]:
        mapping = defaultdict(lambda: [])
        for atm in model:
            id = int(str(atm.arguments[0]))
            mapping[id].append(atm)

        patterns = []
        for _, atoms in mapping.items():
            patterns.append(IdPattern(atoms, type, position))

        return patterns

    @staticmethod
    def from_pattern(id: int, pattern: Pattern) -> IdPattern:
        idp = IdPattern([], pattern.type, pattern.position)
        for itm in pattern.items:
            idp.items.append(IdItem(id, itm.position, itm.value, itm.sign))
        idp.id = id

        return idp

    def __repr__(self) -> str:
        data = []
        for itm in self.items:
            data.append(itm.__repr__())
        return f"P[{self.id}," + ", ".join(data) + "]"

    def __str__(self) -> str:
        return " ".join([i.to_atom() for i in self.items])
