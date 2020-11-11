class Item:
    def __init__(self, pos, value, sign="pat") -> None:
        self.position = pos
        if sign != "pat" and sign != "neg":
            raise AttributeError(f"Sign needs to be either pos or neg (was {sign})")
        self.sign = sign
        self.value = value

    def __eq__(self, o: object) -> bool:
        if type(o) == Item:
            return (
                self.position == o.position
                and self.value == o.value
                and self.sign == o.sign
            )
        return False

    def __lt__(self, o: object):
        if type(o) == Item:
            if self.position == o.position:
                return self.sign == "pat"
            return self.position < o.position
        return False

    def __gt__(self, o: object):
        if type(o) == Item:
            if self.position == o.position:
                return self.sign == "neg"
            return self.position > o.position
        return False

    def __str__(self) -> str:
        return f'Item({self.position}, {self.value}, sign="{self.sign}")'

    def __repr__(self) -> str:
        return f"{self.sign}({self.position},{self.value})"


class Pattern:
    def __init__(self, atoms) -> None:
        items = []
        for atm in atoms:
            if atm.match("support", 1):
                continue
            items.append(
                Item(
                    int(str(atm.arguments[0])),
                    str(atm.arguments[1]),
                    str(atm).split("(")[0],
                )
            )
        items.sort()
        self.itmes = items

    def __eq__(self, o: object) -> bool:
        if type(o) == Pattern:
            length = len(self.itmes)
            if length != len(o.items):
                return False
            t = True
            for itm in range(length):
                t = True
                for itm2 in range(length):
                    index = (itm + itm2) % length
                    if self.itmes[index] != o.items[itm2]:
                        t = False
                        break
                if t:
                    return True

        return False

    def to_list(self) -> list:
        data = []
        for itm in self.items:
            data.append(str(itm))
        return data

    def __repr__(self) -> str:
        data = []
        for itm in self.itmes:
            data.append(itm.__repr__())
        return "P[" + ", ".join(data) + "]"

    def to_rule_body(
        self, chooseatom: str, track=0, intervals=False, seq_distance=None,
    ) -> str:
        """Converts the current pattern into a rule body used by the composer.

        Args:
            chooseatom (str): the choose... atom this pattern represents
            track (int, optional): the track this pattern belongs to. Defaults to 0.
            intervals (bool, optional): True if this pattern is in interval representation, False otherwise. Defaults to False.
            seq_distance ([type], optional): The distance for the whole sequence. Defaults to None.

        Returns:
            str: The rule body represented by this pattern
        """
        data = []
        pos = 0
        i = 0
        last_neg = False
        ints = []
        last_pos_i = 0

        for l, itm in enumerate(self.itmes):

            if itm.sign == "pat" and last_neg:
                data.append(f"P{pos}<P{pos+1}")
                pos += 1
                if intervals:
                    data.append(f"I{i+1}-I{i}={itm.value}")

            if not intervals:
                data.append(f"{chooseatom}({track},P{pos},{itm.value})")
            else:
                data.append(f"{chooseatom}({track},P{pos},I{i})")

            if itm.sign == "pat":
                last_pos_i = i
                if l != len(self.itmes) - 1:
                    data.append(f"P{pos}<P{pos+1}")
                    if intervals:
                        if l != len(self.itmes):
                            data.append(f"I{i+1}-I{i}={itm.value}")
                        for _i in ints:
                            data.append(f"I{i}-I{_i}={itm.value}")
                        ints.clear()
                pos += 1
                last_neg = False
            else:
                if intervals:
                    data.append(f"I{i}-I{last_pos_i}={itm.value}")
                    ints.append(i)
                last_neg = True

            i += 1

        if seq_distance != None:
            data.append(f"P{pos-1}-P0 <= {seq_distance},P{pos-1}-P0>0")

        return ",".join(data)

