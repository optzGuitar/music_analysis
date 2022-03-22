from typing import Any, Optional
from Data.sign_enumeration import SignEnumeration
from dataclasses import dataclass
from Data.position_to_atom import original_position_to_atom


@dataclass
class Item:
    position: int
    value: Any
    sign: SignEnumeration = SignEnumeration.POS

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Item):
            return (
                self.position == o.position
                and self.value == o.value
                and self.sign == o.sign
            )
        return False

    def __lt__(self, o: object):
        if isinstance(o, Item):
            if self.position == o.position:
                return self.sign == SignEnumeration.POS
            return self.position < o.position
        return False

    def __gt__(self, o: object):
        if isinstance(o, Item):
            if self.position == o.position:
                return self.sign == SignEnumeration.NEG
            return self.position > o.position
        return False

    def __repr__(self) -> str:
        return f'Item({self.position}, "{self.value}", sign={self.sign})'

    def __str__(self) -> str:
        return f"{self.sign.value}({self.position},{self.value})"

    def to_full_atom(self, atom: int, track: int, position: int, intervals: bool, i: Optional[int] = None) -> str:
        if intervals:
            if i is None:
                raise RuntimeError(
                    f"Cannot convert {self} to interval atom without i")
            return f"{original_position_to_atom[atom]}({track},P{position},I{i})"
        return f"{original_position_to_atom[atom]}({track},P{position},{self.value})"
