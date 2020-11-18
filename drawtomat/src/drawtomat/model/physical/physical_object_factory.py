from abc import ABCMeta, abstractmethod


class PhysicalObjectFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_physical_object(self, word: str, **kwargs):
        pass
