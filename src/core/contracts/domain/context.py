# src/core/contracts/domain/context.py

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Type, Any

from src.core.contracts.kernel import KernelSubsystem

# Declare Enums for Domain Family (leaf[DomainRecord] or root[DomainRoot])
class DomainFamily(Enum):
    ROOT = auto()
    LEAF = auto()
    SPORE = auto()

@dataclass(frozen=True)
class DomainContext:
    family: DomainFamily
    intent: str
    priority: int
    requirements: List[KernelSubsystem] = field(default_factory=list)
    service: Type[Any]|None = None

    def __post_init__(self) -> None:
        # Enforce values for Boot Priority
        if not (0 <= self.priority <= 100):
            raise ValueError(f"[CONTEXT VIOLATION] 'priority' MUST be between 0 and 100")
        
        # Enforce Intent for Sreaming MVC
        if not self.intent.strip():
            raise ValueError(
                f"[CONTEXT VIOLATION] property 'intent' CANNOT be empty"
            )
        
        # Enforce ALL DomainRoots have a Service
        if self.family == DomainFamily.ROOT and self.service is None:
            raise ValueError(
                f"[CONTEXT VIOLATION] Root Package '{self.intent}' MUST provide a Service! "
                f"ALL DomainRoot packages MUST have a Service associated with them."
            ) 