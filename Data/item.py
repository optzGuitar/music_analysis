class Item:
    def __init__(self, pos, value, sign="pat") -> None:
        self.position = pos
        if sign != "pat" and sign != "neg":
            raise AttributeError(f"Sign needs to be either pos or neg (was {sign})")
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
                return self.sign == "pat"
            return self.position < o.position
        return False

    def __gt__(self, o: object):
        if isinstance(o, Item):
            if self.position == o.position:
                return self.sign == "neg"
            return self.position > o.position
        return False

    def __str__(self) -> str:
        return f'Item({self.position}, {self.value}, sign="{self.sign}")'

    def __repr__(self) -> str:
        return f"{self.sign}({self.position},{self.value})"
