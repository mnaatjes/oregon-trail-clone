# src/core/kernel/contracts/scanner.py

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, List

from core.kernel.contracts.discovery.unit import DiscoveryUnit

# Declare Typevar
T = TypeVar("T", bound=DiscoveryUnit)

class BaseScanner(ABC, Generic[T]):
    @abstractmethod
    def scan(self, source:Any) -> List[T]:
        """Find all units of type T in the given path."""
        pass