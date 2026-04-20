# src/core/contracts/domain/context.py

from dataclasses import dataclass, field
from typing import List, Type, Any

from src.core.contracts.domain.taxonomy import DomainFamily
from src.core.contracts.kernel import KernelSubsystem
from src.core.contracts.domain.blueprints.root import RootBlueprint
from src.core.contracts.domain.blueprints.record import RecordBlueprint
from src.core.contracts.domain.spore import DomainSpore

@dataclass(frozen=True)
class DomainContext:
    intent: Type[DomainSpore] | Type[RootBlueprint] | Type[RecordBlueprint]
    priority: int
    requirements: List[KernelSubsystem] = field(default_factory=list)
    service: Type[Any]|None = None

    def __post_init__(self) -> None:
        # Enforce values for Boot Priority
        if not (0 <= self.priority <= 100):
            raise ValueError(f"[CONTEXT VIOLATION] 'priority' MUST be between 0 and 100")
        
        # Enforce Intent for Sreaming MVC
        if not self.intent:
            raise ValueError(
                f"[CONTEXT VIOLATION] property 'intent' CANNOT be empty "
                f"MUST be implementation of DomainSpore, RootBlueprint, or RecordBlueprint"
            )
        
    @property
    def family(self) -> DomainFamily:
        """Derives DomainFamily from self.intent after initialization"""
        if issubclass(self.intent, DomainSpore):
            return DomainFamily.SPORE
        elif issubclass(self.intent, RootBlueprint):
            return DomainFamily.ROOT
        elif issubclass(self.intent, RecordBlueprint):
            return DomainFamily.LEAF
        else:
            raise TypeError(
                f"[CONTEXT VIOLATION] in '{self.intent}' "
                f"Unable to derive DomainFamily (ROOT, LEAF, SPORE) from DomainContext"
            )

    @property
    def species(self) -> str:
        """Explicitly reads the species from the intent class"""
        species = getattr(self.intent, "species", None)
        if not isinstance(species, str):
            raise ValueError(
                f"[CONTEXT VIOLATION] where DomainConetxt.intent = '{self.intent}' "
                f"intent derived property 'species' NOT FOUND"
            )
        return species