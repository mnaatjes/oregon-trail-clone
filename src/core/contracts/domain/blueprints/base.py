# src/core/contracts/domain/blueprints/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.contracts.domain.taxonomy import DomainFamily
from src.core.contracts.domain.blueprints.display import DisplayBlueprint


@dataclass(frozen=True)
class BaseBlueprint(ABC):
    """
    Abstract base for all domain templates.
    - Breed Property (fmr. "slug") ensures every blueprint has at least a unique identifier.
    - Read-only
    - Global Template
    - Shared across many instances
    - Loaded from assets (e.g. assets/professions.json)
    """
    breed: str # Variant: e.g., 'cholera', 'blizzard', 'farmer'
    display: DisplayBlueprint # Display Blueprint for asset resolution

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Identity Purity Guard
        forbidden = {"id", "uid", "uuid"}
        
        # Check annotations (dataclass fields) and class attributes
        found_fields = set(getattr(cls, "__annotations__", {}).keys()) | set(cls.__dict__.keys())
        
        for field_name in found_fields:
            if field_name.lower() in forbidden:
                raise TypeError(
                    f"[IDENTITY VIOLATION] Blueprint '{cls.__name__}' "
                    f"cannot have identity field '{field_name}'"
                )

    def __post_init__(self):
        # Spore Prohibition
        if self.family == DomainFamily.SPORE:
            raise TypeError(
                f"[TAXONOMY VIOLATION] Blueprint '{self.__class__.__name__}' "
                f"cannot belong to the SPORE family."
            )

        # DNA Audit (Using MRO to avoid circular imports)
        class_names = [c.__name__ for c in self.__class__.__mro__]
        
        if "RootBlueprint" in class_names and self.family != DomainFamily.ROOT:
            raise TypeError(
                f"[DNA MISMATCH] {self.__class__.__name__} is a RootBlueprint "
                f"but reports family {self.family}"
            )
            
        if "RecordBlueprint" in class_names and self.family != DomainFamily.LEAF:
            raise TypeError(
                f"[DNA MISMATCH] {self.__class__.__name__} is a RecordBlueprint "
                f"but reports family {self.family}"
            )

    @property
    @abstractmethod
    def species(self) -> str:
        """The taxonomic branch (e.g., "wagon", "character")"""
        pass

    @property
    @abstractmethod
    def family(self) -> DomainFamily:
        """The architectural role (ROOT or LEAF)."""
        pass
