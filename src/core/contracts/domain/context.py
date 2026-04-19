# src/core/contracts/domain/context.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Type, Any

# Declare Enums for Domain Family (leaf[DomainRecord] or root[DomainRoot])
class DomainFamily(Enum):
    ROOT = auto()
    LEAF = auto()

@dataclass(frozen=True)
class DomainContext:
    family: DomainFamily
    intent: str
    priority: int
    pillars: List[str] = field(default_factory=list)
    provider: Type[Any]|None = None

    def __post_init__(self) -> None:
        if self.priority < 0 or self.priority > 100:
            raise ValueError(f"[CONTEXT VIOLATION] 'priority' MUST be between 0 and 100")