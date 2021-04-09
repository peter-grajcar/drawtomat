from abc import ABCMeta, abstractmethod

import numpy as np

from drawtomat.model.composition import PhysicalObject


class Constraint(metaclass=ABCMeta):
    """
    Abstract constraint class used for typing. Relations in the relation graph
    (i.e. edges of the graph) define constraints which a position of an object
    must meet. These constraints are defined by binary functions (or callable
    objects) R^2 → {T, F} which for given coordinates return whether the
    constraint is satisfied.

    When placing an object a set of randomly generated points is produced. These
    points are tested and if a points meets all the constraints then it is used
    as a position of the object. If none of the generated points meets all the
    constraints then a point with the most of constraints satisfied is used as
    a position.

    See Also
    --------
    drawtomat.composer.constraint_composer.ConstraintComposer

    Attributes
    ----------
    obj : PhysicalObject
        An object to which the constraint relates
    pred: str
        Predicate which defines the constraint
    """

    def __init__(self):
        self.obj = None
        self.pred = None

    def init(self):
        """
        Initialises necessary constraint attributes. This method needs to be
        called before using the constraint.

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def __call__(self, xs: 'np.ndarray[float]', ys: 'np.ndarray[float]') -> 'np.ndarray[int]':
        """
        Determines whether given coordinates meet the condition given
        by the constraint.

        Parameters
        ----------
        xs : np.ndarray[float]
            X coordinates.
        ys : np.ndarray[float]
            Y coordinates.

        Returns
        -------
        np.ndarray[int]
            1 if (x,y) meets the condition otherwise 0
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.obj.entity.word})"
