# src/core/contracts/registry.py

from typing import TypeVar, Dict, Optional, Generic, TypeAlias

# Registry Key Alias
RegistryKey: TypeAlias = str

T = TypeVar('T')

class BaseRegistry(Generic[T]):
    """
    Standardized container for system architecture.
    The caller is responsible for providing the key at registration.

    This is a concrete class that can be used directly:
    registry = BaseRegistry[MyItem]()
    """
    def __init__(self):
        self._items: Dict[RegistryKey, T] = {}

    def register(self, key:RegistryKey, item: T) -> None:
        """Explicit registration. Zero coupling between Item and Registry."""
        self._items[key] = item

    def get(self, key: RegistryKey) -> Optional[T]:
        """Retrieves an item by its key."""
        return self._items.get(key)

    def all(self) -> Dict[RegistryKey, T]:
        """Returns all registered items."""
        return self._items
    
    def exists(self, key:RegistryKey) -> bool:
        """Searches for key"""
        return key in self._items