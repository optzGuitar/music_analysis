from Data.pattern_type import PatternType


class Type:
    def __init__(self, name:str, pattern_type: PatternType):
        self.__name = name
        self.__pattern_type = pattern_type

    @property
    def Name(self):
        return self.__name

    @property
    def PatternType(self):
        return self.__pattern_type

    def __hash__(self):
        return hash(f"{self.Name}{self.PatternType}")

    def __eq__(self, other):
        if isinstance(other, Type):
            return self.Name == other.Name and self.PatternType == other.PatternType
        
        return False

    def __repr__(self) -> str:
        return f"Type({self.__name}, {self.__pattern_type})"
        