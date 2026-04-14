# src/core/contracts/value_object.py

from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True)
class DomainValueObject(ABC):
    """
    Abstract base for all Domain Value Objects.
    
    - Value Objects have no identity (UID). 
        - Two instances are considered identical if all their attributes are equal.
        - Data IS the ID

    - Attributes are immutable (frozen) to ensure thread-safety and 
    domain integrity.

    - Specific Data Bundle unique to one instance but performs no action
        - e.g. CharacterIdentity("Jedediah")
        - Collections of Blueprints or values or both
        - Immutable State
        - Created in Logic
        - Saved to Storage
    """
    
    def __eq__(self, other):
        """
        Forces a comparison of the dict of the ValueObject
        - Allows Proper Comparison
        - e.g. value_obj_a == value_obj_b to return True
        """
        if not isinstance(other, DomainValueObject):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        # Allows Value Objects to be used as keys in dictionaries 
        # or elements in sets
        return hash(tuple(sorted(self.__dict__.items())))