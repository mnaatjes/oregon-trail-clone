# src/core/contracts/domain/record.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import get_type_hints, Self

@dataclass(frozen=True)
class DomainRecord(ABC):
    """
    Characteristics:
    - Immutable
    - PROHIBITED from importing a Sibling Record
    - MUST be able to perform deep self-copy
    - MUST enforce specific constraints on properties
    """

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        """
        Isolation Guard: Metaprogrammatically audits new children the moment
        of definition - fail fast - and ensures NO Sibling Record can appear
        as property
        """
        # Get type hints for new subclass
        annotations = get_type_hints(cls)

        for field_name, field_type in annotations.items():
            # Check for Structural Sibling / Horizontal Violations
            if hasattr(field_type, "__mro__") and DomainRecord in field_type.__mro__:
                raise TypeError(
                    f"[STRUCTURAL SIBLING CONFLICT] in {cls.__name__}: "
                    f"Field '{field_name}' is a DomainRecord. "
                    f"Leaf Models MUST remain Horizontally Isolated"
                )

            # Check for id, uuid, uid properties
            # DomainRecord should NOT contain identity information
            invalid_id_props = ["id", "uuid", "uid"]
            if field_name in invalid_id_props:
                raise ValueError(
                    f"[ANONYMITY VIOLATION] in '{cls.__name__}': "
                    f"DomainRecords CANNOT contain identification information "
                    f"Including {", ".join(invalid_id_props)}"
                )
    
    @abstractmethod
    def clone(self) -> Self:
        """
        Supports a deep-copy mechanism for safe Logic transformation
        Returns:
            - New instance of the SAME class
        """
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Must self-validate
        - Define specific constraints; e.g. hp cannot be negative

        """
