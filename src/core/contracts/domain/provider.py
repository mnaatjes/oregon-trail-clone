# src/core/contracts/provider.py

from abc import ABC, abstractmethod
from src.core.container import ServiceContainer
#from src.storage.loaders import JSONLoader

class BaseServiceProvider(ABC):
    """
    Abstract Base for all Domain Wiring. 
    Follows a two-phase lifecycle: Register -> Boot.
    """

    def __init__(self, container: ServiceContainer):
        self.container = container

    @abstractmethod
    def register(self) -> None:
        """
        Phase 1: Bind classes or instances into the container.
        Do not look for other services here; they may not be registered yet.
        """
        pass

    @abstractmethod
    def boot(self) -> None:
        """
        Phase 2: Logic that requires other services or asset loading.
        Called only after all providers have finished register().
        """
        pass

    @abstractmethod
    def provides(self) -> list:
        """
        Optional: Return a list of service keys that this provider registers.
        Useful for testing and introspection.
        """
        return []