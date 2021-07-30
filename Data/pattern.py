from collections import defaultdict
from Data.sign_enumeration import SignEnumeration
from Data.pattern_type import PatternType
from typing import Dict, List, Optional, Tuple
from .item import Item
from itertools import chain
_orig_pos_to_atom = {
    3: "chosennote",
    4: "chosenvel",
    5: "chosenlength",
    6: "chosendist",
}

class Pattern:
    def __init__(self, atoms: List, type: PatternType, position: int, are_intervals: bool, distance: Optional[int]) -> None:
        items = [] # type: List[Item]

        try:
            for atm in atoms:
                if atm.match("support", 1):
                    continue
                items.append(
                    Item(
                        int(str(atm.arguments[0])),
                        str(atm.arguments[1]),
                        SignEnumeration(str(atm).split("(")[0])
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
        atoms, pos, interv = self._to_full_rule_body_parts(track, pattern_max_distance)

        kept_data = []
        for atms, posiiton_rules, interval_rules in zip(atoms.items(), pos.items(), interv.items()):
            pos = atms[0]
            if length is None or pos < length:
                kept_data += atms[1] + posiiton_rules[1] + interval_rules[1]

        return ','.join(kept_data)
        
    def _to_full_rule_body_parts(self, track, pattern_max_distance) -> Tuple[Dict[int, List[str]], Dict[int, List[str]], Dict[int, List[str]]]:
        atoms: Dict[int, List[str]] = defaultdict(list)
        pos_restrictions: Dict[int, List[str]] = defaultdict(list)
        interval_restrictions: Dict[int, List[str]] = defaultdict(list)
        pos = 0
        i = 0
        last_neg = False
        ints = []
        last_pos_i = 0
        chooseatom = _orig_pos_to_atom[self.position]

        for l, itm in enumerate(self.items):
            atoms[pos], pos_restrictions[pos], interval_restrictions[pos]

            if itm.sign == SignEnumeration.POS and last_neg:
                pos += 1
                pos_restrictions[pos].append(f"P{pos-1}<P{pos}")
                if self.are_intervals:
                    interval_restrictions[pos].append(f"I{i+1}-I{i}={itm.value}")

            if not self.are_intervals:
                atoms[pos].append(f"{chooseatom}({track},P{pos},{itm.value})")
            else:
                atoms[pos].append(f"{chooseatom}({track},P{pos},I{i})")

            if itm.sign == SignEnumeration.POS:
                last_pos_i = i
                pos += 1
                if l != len(self.items) - 1:
                    pos_restrictions[pos].append(f"P{pos-1}<P{pos}")
                    if self.are_intervals:
                        if l != len(self.items):
                            interval_restrictions[pos].append(f"I{i+1}-I{i}={itm.value}")
                        for _i in ints:
                            interval_restrictions[pos].append(f"I{i}-I{_i}={itm.value}")
                        ints.clear()
                last_neg = False
            else:
                if self.are_intervals:
                    interval_restrictions[pos].append(f"I{i}-I{last_pos_i}={itm.value}")
                    ints.append(i)
                last_neg = True

            i += 1

        if pattern_max_distance is not None:
            pos_restrictions[pos].append(f"P{pos-1}-P0 <= {pattern_max_distance},P{pos-1}-P0>0")

        return atoms, pos_restrictions, interval_restrictions
