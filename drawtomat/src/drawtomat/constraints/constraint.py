from abc import ABCMeta, abstractmethod


class Constraint(metaclass=ABCMeta):
    """
    Abstract constraint class used for typing.
    """
    @abstractmethod
    def __call(self, x: 'float', y: 'float') -> bool:
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
