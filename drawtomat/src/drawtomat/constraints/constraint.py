from abc import ABCMeta, abstractmethod

import numpy as np

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

    def init(self):
        pass

    @abstractmethod
    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        """
        Determines whether given coordinates meet the condition given
        by the constraint.

        Parameters
        ----------
        xs : np.ndarray[float]
            x coordinates
        ys : np.ndarray[float]
            y coordinates

        Returns
        -------
        np.ndarray[int]
            1 if (x,y) meets the condition otherwise 0
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.obj.entity.word})"
