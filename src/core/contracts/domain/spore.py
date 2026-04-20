# src/core/contracts/domain/spore.py

from abc import ABC
from dataclasses import dataclass
from typing import get_type_hints

@dataclass(frozen=True)
class DomainSpore(ABC):
    """
    Abstract base for all Domain Spores (DomainFamily.SPORE).
    
    - Spores have no identity (UID). 
        - Two instances are considered identical if all their attributes are equal.
        - Data IS the ID (Value Equality).

    - Attributes are immutable (frozen) to ensure thread-safety and 
    domain integrity.

    - Specific Data Bundle unique to one instance but performs no action.
        - e.g. Coordinates(x=10, y=20)
        - Collections of Blueprints or values or both.
        - Immutable State used for semantic typing.
    """
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # Identity Purity Guard: Ensures Spores don't accidentally gain identity
        forbidden = {"uid", "uuid", "id", "slug"}
        for f in get_type_hints(cls):
            if f.lower() in forbidden:
                raise TypeError(
                    f"[IDENTITY VIOLATION] in '{cls.__name__}' "
                    f"CANNOT use property '{f}' "
                    f"Use of Identification in DomainSpores PROHIBITED!"
                )

    def __post_init__(self) -> None:
        """Hook for structural validation."""
        self.validate()
    
    def validate(self) -> None:
        """
        Override this in subclasses to enforce business rules.
        Should raise ValueError or TypeError if invalid.
        """
        pass