from abc import ABCMeta, abstractmethod

from drawtomat.model.composition import PhysicalObject


class PhysicalObjectScaler(metaclass=ABCMeta):
    """
    Base object scaler class.
    """

    @abstractmethod
    def scale(self, sub: 'PhysicalObject', obj: 'PhysicalObject', pred: 'str') -> 'float':
        """
        Scales the subject according to the object and predicate.

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
