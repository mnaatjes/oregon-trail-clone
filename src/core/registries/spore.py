# src/core/registries/spore.py

from src.core.contracts.registry import BaseRegistry, RegistryKey
from src.core.contracts.domain.spore import DomainSpore

class SporeRegistry(BaseRegistry[type[DomainSpore]]):
    """Global Registry for all DomainSpore instances"""

    def register(self, key: str, item: type[DomainSpore]) -> None:
        """Enforces that only DomainSpore classes can be registered."""
        return super().register(key, item)
    
    def get(self, key: RegistryKey) -> type[DomainSpore] | None:
        return super().get(key)

# Singleton Export Global Handle
spores = SporeRegistry()