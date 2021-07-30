from Data.sign_enumeration import SignEnumeration


class Item:
    def __init__(
        self, pos: int, value, sign: SignEnumeration = SignEnumeration.POS
    ) -> None:
        self.position = pos
        self.sign = sign
        self.value = value

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
