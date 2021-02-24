from abc import ABCMeta, abstractmethod

from drawtomat.model.composition import PhysicalObject


class PhysicalObjectScaler(metaclass=ABCMeta):
    """
    TODO:
    """

    @abstractmethod
    def scale(self, sub: 'PhysicalObject', obj: 'PhysicalObject', pred: 'str') -> 'float':
        """
        TODO:

        Parameters
        ----------
        sub: PhysicalObject
            subject
        obj: PhysicalObject
            object
        pred: str
            predicate

        Returns
        -------
        float
        """
        pass
