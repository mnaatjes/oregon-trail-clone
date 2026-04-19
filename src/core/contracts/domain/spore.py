# src/core/contracts/value_object.py

from abc import ABC
from dataclasses import dataclass
from typing import get_type_hints

@dataclass(frozen=True)
class DomainSpore(ABC):
    """
    Abstract base for all Domain Value Objects (DomainFamily.SPORE).
    
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
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Identity Purity Guard
        forbidden = {"uid", "uuid", "id", "slug"}
        for f in get_type_hints(cls):
            if f.lower() in forbidden:
                raise TypeError(
                    f"[IDENTITY VIOLATION] in '{cls.__name__}' "
                    f"CANNOT use property '{f}' "
                    f"Use of Identification in DomainValueObjects PROHIBITED!"
                )

    def __post_init__(self) -> None:
        """Hook for structural validation."""
        self.validate()
    
    def validate(self) -> None:
        """
        Override this in subclasses to enforce rules.
        Should raise ValueError or TypeError if invalid.
        """
        pass