from typing import List

from drawtomat.constraints import Constraint
from drawtomat.model.physical import PhysicalEntity


def place_object(obj: 'PhysicalEntity', constraints: 'List[Constraint]') -> None:
    """
    Places object using Monte Carlo algorithm in such way that the position of
    the object will meet the most of the constraints.

    Parameters
    ----------
    obj : PhysicalEntity
        Object to place
    constraints : List[Constraint]
        Constraints to meet

    Returns
    -------
    None
    """
    pass