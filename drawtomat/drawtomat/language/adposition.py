from enum import Enum


class Adposition(Enum):
    """
    An enumeration of supported adpostions.
    """
    ON = 1
    UNDER = 2

    def __str__(self) -> str:
        return self.name

    def for_name(name: str) -> 'Adposition':
        for adp in Adposition:
            if name.upper() == adp.name:
                return adp
        return None

