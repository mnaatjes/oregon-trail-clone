# src/core/kernel/contracts/scanner.py

from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, List

from core.kernel.contracts.discovery import DiscoveryUnit

# Declare Typevar
T = TypeVar("T", bound=DiscoveryUnit)

class BaseScanner(ABC, Generic[T]):
    @abstractmethod
    def scan(self, path:str) -> List[T]:
        """Find all units of type T in the given path."""
        pass