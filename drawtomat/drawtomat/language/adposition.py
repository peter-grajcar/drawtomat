from enum import Enum


class Adposition(Enum):
    """
    An enumeration of supported adpostions.
    """
    UNKNOWN = 0
    ON = 1
    UNDER = 2
    IN = 3
    BETWEEN = 4
    NEXT_TO = 5
    ABOVE = 6
    BELOW = 7
    BEHIND = 8
    IN_FRONT_OF = 9
    INSIDE = 10

    def __str__(self) -> str:
        return self.name

    def for_name(name: str) -> 'Adposition':
        for adp in Adposition:
            if name.replace(' ', '_').upper() == adp.name:
                return adp
        return Adposition.UNKNOWN

