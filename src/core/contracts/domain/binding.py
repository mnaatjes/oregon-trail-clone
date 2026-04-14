# src/core/contracts/domain/binding.py

from typing import Protocol, TypeVar, runtime_checkable
from .entity import DomainEntity
from .state import DomainState
from .blueprint import DomainBlueprint

# Generics to ensure the plug-shapes match
E = TypeVar("E", bound=DomainEntity)
S = TypeVar("S", bound=DomainState)
B = TypeVar("B", bound=DomainBlueprint)

@runtime_checkable
class DomainBinding(Protocol[E, S, B]):
    """
    The Protocol defining the structural interface for a Domain Pillar.
    It binds the Orchestrator (Service) to the Transformer (Logic).
    """
    def orchestrate(self, entity: E) -> None: 
        """Implementation found in the Domain Service."""
        ...

    def transform(self, state: S, blueprint: B) -> S:
        """Implementation found in the Domain Logic."""
        ...