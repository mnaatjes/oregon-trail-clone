# src/core/contracts/registry.py

from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Generic, Optional
from .blueprint import DomainBlueprint

# T represents a specific subclass of DomainBlueprint
T = TypeVar('T', bound=DomainBlueprint)

class BaseRegistry(ABC, Generic[T]):
    """
    Standardized container for Domain Blueprints.
    """
    def __init__(self):
        self._items: Dict[str, T] = {}

    def register(self, item: T) -> None:
        """Adds a blueprint to the internal map."""
        self._items[item.slug] = item

    def get(self, slug: str) -> Optional[T]:
        """Retrieves a blueprint by its slug."""
        return self._items.get(slug)

    @abstractmethod
    def hydrate(self, raw_data: dict) -> None:
        """
        Logic to transform raw JSON/Dict into concrete Blueprints.
        Must be implemented by the specific Domain Registry.
        """
        pass