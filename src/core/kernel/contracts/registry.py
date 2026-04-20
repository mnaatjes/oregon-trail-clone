# src/core/contracts/registry.py
from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Optional, Generic, TypeAlias

# Registry Key Alias
RegistryKey: TypeAlias = str

T = TypeVar('T')

class BaseRegistry(ABC, Generic[T]):
    """
    Standardized container for system architecture.
    The caller is responsible for providing the key at registration.

    This is an Abstract class that MUST be inherited
    registry = BaseRegistry[MyItem]()
    """
    def __init__(self):
        self._items: Dict[RegistryKey, T] = {}

    @abstractmethod
    def register(self, key:RegistryKey, item: T) -> None:
        """Explicit registration. Zero coupling between Item and Registry."""
        self._items[key] = item

    @abstractmethod
    def get(self, key: RegistryKey) -> Optional[T]:
        """Retrieves an item by its key."""
        return self._items.get(key)

    def all(self) -> Dict[RegistryKey, T]:
        """Returns all registered items."""
        return self._items
    
    def exists(self, key:RegistryKey) -> bool:
        """Searches for key"""
        return key in self._items