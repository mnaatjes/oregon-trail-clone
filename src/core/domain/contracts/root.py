# src/core/contracts/domain/root.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from uuid import UUID
from typing import Dict, Self, get_type_hints
from core.domain.contracts.record import DomainRecord
from core.domain.contracts.blueprints.base import BaseBlueprint

@dataclass(frozen=True)
class DomainRoot(ABC):
    """
    Sovereign Aggregate Root that anchors a Bounded Context.
    Enforces total serializability and strict vertical composition.
    """
    uid: UUID   # Soveriegn Identity
    blueprint: BaseBlueprint  # Static Template
    records: Dict[str, DomainRecord] = field(default_factory=dict)

    def __init_subclass__(cls, **kwargs) -> None:
        """
        Enforces global and architectural rules:
        - Anemic Purity: dataclass and is frozen
        - Horizontal Isolation: DomainRoot CANNOT contain another DomainRoot
        """
        super().__init_subclass__(**kwargs)

        # Check Horizontal Isolation
        # Ensure no other DomainRoots exist in object
        try:
            hints = get_type_hints(cls)
            for name, type_hint, in hints.items():
                if hasattr(type_hint, "__mro__") and DomainRoot in type_hint.__mro__:
                    raise TypeError(
                        f"[HORIZONTAL VIOLATION] in '{cls.__name__}': "
                        f"Field '{name}' is a DomainRoot "
                        f"Roots CANNOT aggregate in other DomainRoots!"
                    )
        except NameError:
            # TODO: Catch with Architectural Policing
            pass

    def __post_init__(self):
        # Ensure Identity Sovereignty
        if not isinstance(self.uid, UUID):
            raise TypeError(
                f"[SOVEREIGNTY VIOLATION] in '{self.__class__.__name__}': "
                f"Property 'uid' MUST be type UUID"
            )

        # Horizontal Isolation
        # Ensure DomainRoot NOT a property of class
        for f in fields(self):
            value = getattr(self, f.name)
            
            # Skip records
            if f.name == "records":
                continue

            # Search for instances of DomainRoot in properties
            if isinstance(value, DomainRoot):
                raise TypeError(
                    f"[HORIZONTAL VIOLATION] in '{self.__class__.__name__}': "
                    f"Field '{f.name}' contains DomainRoot instance! "
                    f"Roots CANNOT contain DomainRoot instances"
                )

        # Veritcal Composition
        # Ensure Records Dict ONLY contains DomainRecords
        for key, record in self.records.items():
            if not isinstance(record, DomainRecord):
                raise TypeError(
                    f"[VERTICAL VIOLATION] in '{self.__class__.__name__}': "
                    f"Key: '{key}' MUST be a DomainRecord!"
                )

    @property
    def __species__(self) -> str:
        """Exposes DomainBlueprint Species"""
        return self.blueprint.__species__ 
    
    @abstractmethod
    def clone(self) -> Self:
        """
        Must return a deep-copied version of the Root using dataclasses.replace.
        Example: return replace(self, records={k: v.clone() for k, v in self.records.items()})
        """
        pass

