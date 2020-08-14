from abc import ABCMeta, abstractmethod

from drawtomat.model.physical import PhysicalObject


class Constraint(metaclass=ABCMeta):
    """
    Abstract constraint class used for typing.

    Attributes
    ----------
    obj : PhysicalObject
        an object to which the constraint relates
    """

    def __init__(self):
        self.obj = None

    @abstractmethod
    def __call__(self, x: 'float', y: 'float') -> bool:
        """
        Determines whether given coordinates meet the condition given
        by the constraint.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate

        Returns
        -------
        bool
            True if (x,y) meet the condition
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.obj.entity.word})"
