from enum import Enum


class Adposition(Enum):
    """
    An enumeration of supported adpostions.
    """
    ON = 1
    UNDER = 2

    def __str__(self) -> str:
        return self.name
