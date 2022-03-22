from collections import defaultdict
from Data.note_atoms import NoteAtoms
from Data.sign_enumeration import SignEnumeration
from Data.pattern_type import PatternType
from typing import Dict, List, Optional, Tuple
from .item import Item
from Data.position_to_atom import original_position_to_atom


class Pattern:
    def __init__(self, atoms: List, type: PatternType, position: int, are_intervals: bool, distance: Optional[int]) -> None:
        items: List[Item] = []

        try:
            for atm in atoms:
                if atm.match("support", 1):
                    continue
                items.append(
                    Item(
                        position=int(str(atm.arguments[0])),
                        value=str(atm.arguments[1]),
                        sign=SignEnumeration(str(atm).split("(")[0])
                    )
                )
        except AttributeError:
            items = atoms

        items.sort()
        self.items = items
        self.type = type
        self.position = position if position > 0 else position * -1
        self.are_intervals = are_intervals
        self.distance = distance

    @property
    def is_negative(self):
        return self.type & PatternType.NEGATIVE

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Pattern):
            return self.__hash__() == o.__hash__()
        return False

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def to_list(self) -> list:
        data = []
        for itm in self.items:
            data.append(str(itm))
        return data

    def __repr__(self) -> str:
        data = []
        for itm in self.items:
            data.append(itm.__repr__())
        return f"Pattern([{', '.join(data)}], {self.type}, {self.position}, {self.are_intervals}, {self.distance})"

    def to_rule_body(self, track=0, pattern_max_distance=None, length=None) -> str:
        """Converts the current pattern into a rule body used by the composer."""
        atoms, pos, interv = self._to_full_rule_body_parts(
            track, pattern_max_distance)

        kept_data = []
        for atms, posiiton_rules, interval_rules in self.clever_zip(atoms, pos, interv):
            position = atms[0]
            if length is None or position < length:
                kept_data += atms[1] + posiiton_rules[1] + interval_rules[1]

        return ','.join(kept_data)

    def _to_full_rule_body_parts(self, track, pattern_max_distance=None) -> Tuple[Dict[int, List[str]], Dict[int, List[str]], Dict[int, List[str]]]:
        atoms: Dict[int, List[str]] = defaultdict(list)
        pos_restrictions: Dict[int, List[str]] = defaultdict(list)
        interval_restrictions: Dict[int, List[str]] = defaultdict(list)
        pos = 0
        ints: List[int] = []
        last_pos_i = 0

        for i, itm in enumerate(self.items):
            full_atom = itm.to_full_atom(
                atom=self.position,
                track=track,
                position=pos,
                intervals=self.are_intervals,
                i=i
            )
            # "neg " if ...
            prior = "" if self.is_negative and itm.sign == SignEnumeration.POS else ""
            atoms[pos].append(f"{prior}{full_atom}")

            if i == 0:
                pos += 1
                continue

            if itm.sign == SignEnumeration.POS:
                last_pos_i = i
                pos_restrictions[pos].append(f"P{pos-1}<P{pos}")
                if self.are_intervals:
                    if ints:
                        for _i in ints:
                            interval_restrictions[pos].append(
                                f"I{i}-I{_i}={itm.value}"
                            )
                        ints.clear()
                    else:
                        interval_restrictions[pos].append(
                            f"I{i}-I{i-1}={itm.value}"
                        )
                pos += 1
            elif itm.sign == SignEnumeration.NEG:
                if self.are_intervals:
                    interval_restrictions[pos].append(
                        f"I{i}-I{last_pos_i}={itm.value}")
                    ints.append(i)
            else:
                raise ValueError(
                    f"{itm} sign has a unhandled value {itm.sign}")

        if pattern_max_distance is not None:
            pos_restrictions[pos].append(
                f"P{pos-1}-P0 <= {pattern_max_distance},P{pos-1}-P0>0")
        elif self.distance is not None:
            pos_restrictions[pos].append(
                f"P{pos-1}-P0 <= {self.distance},P{pos-1}-P0>0")

        if self.are_intervals:
            atoms[pos].append(
                Item.to_full_atom(
                    None,
                    atom=self.position,
                    track=track,
                    position=pos,
                    intervals=self.are_intervals,
                    i=len([itm for itm in self.items if itm.sign ==
                          SignEnumeration.POS])
                )
            )

        return atoms, pos_restrictions, interval_restrictions

    def clever_zip(self, *args: List[Dict]):
        max_len = max([max(i.keys(), default=-1) for i in args])
        for i in range(max_len + 1):
            data = []
            for di in args:
                if i in di:
                    data.append((i, di[i]))
                else:
                    data.append((i, []))

            yield tuple(data)
