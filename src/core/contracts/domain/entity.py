# src/core/contracts/entity.py

from abc import ABC
from uuid import uuid4, UUID
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from .blueprint import DomainBlueprint

# T represents the specific Blueprint type this Entity wraps
T = TypeVar('T', bound=DomainBlueprint)

@dataclass
class DomainEntity(ABC, Generic[T]):
    """
    Abstract base for all stateful game objects.
    Acts as the 'Actor' that holds a reference to its static 'Blueprint'.
    - Stateful Complement to the Blueprint
    - Should NOT inherit the Blueprint
    - Composition (has-a) Blueprint; e.g. for CharacterIdentity(Professor)
    """
    blueprint: T
    
    # Unique identifier for this specific instance (e.g., this specific 'Jedediah')
    uid: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self):
        """
        Validation hook to ensure the entity is created in a valid state.
        """
        pass