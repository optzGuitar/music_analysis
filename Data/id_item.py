from dataclasses import dataclass
from Data.sign_enumeration import SignEnumeration
from .item import Item


class IdItem(Item):
    def __init__(self, id: int, pos: int, value, sign: SignEnumeration) -> None:
        super().__init__(pos, value, sign=sign)
        self.id = id

    def __eq__(self, o: object) -> bool:
        if isinstance(o, IdItem):
            return (
                self.position == o.position
                and self.value == o.value
                and self.sign == o.sign
                and self.id == o.id
            )
        return False

    def __str__(self) -> str:
        return f'IdItem({self.id}, {self.position}, {self.value}, sign="{self.sign}")'

    def __repr__(self) -> str:
        if isinstance(self.sign.value, str):
            print()
        return f"{self.sign.value}({self.id},{self.position},{self.value})"

    def to_atom(self):
        return f"{self.sign.value}({self.id},{self.position},{self.value})."
