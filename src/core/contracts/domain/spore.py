# src/core/contracts/domain/spore.py

from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True)
class DomainSpore(ABC):
    """
    Abstract base for all Domain Spores (DomainFamily.SPORE).
    
    - Spores are Value Objects defined by their data, not an ID. 
        - Two instances are considered identical if all their attributes are equal.
        - Data IS the ID (Value Equality).

    - Attributes are immutable (frozen) to ensure thread-safety and 
    domain integrity.

    - Identity (UID, Breed, etc.) is STRICTLY PROHIBITED.
    """
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        
        # Hardened Identity Purity Guard
        # Expanded to include project-specific taxonomy (breed) and common DB terms
        forbidden = {"id", "uid", "uuid", "slug", "breed", "pk", "pkey", "_id"}
        
        # Inspect all local attributes (fields, methods, properties)
        # annotations: caught dataclass fields and hinted vars
        # vars: caught methods, properties, and unhinted class vars
        found_in_annotations = set(getattr(cls, "__annotations__", {}).keys())
        found_in_vars = set(vars(cls).keys())
        all_defined_names = found_in_annotations | found_in_vars

        for name in all_defined_names:
            if name.lower() in forbidden:
                raise TypeError(
                    f"\n[IDENTITY VIOLATION] in DomainSpore subclass '{cls.__name__}':\n"
                    f"  -> Forbidden attribute found: '{name}'\n"
                    f"  -> REASON: Spores are identity-less Value Objects. Use of '{name}' suggests "
                    f"this should be a DomainRoot or DomainRecord instead."
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
