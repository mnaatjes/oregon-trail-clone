# src/core/kernel/contracts/discovery/payload.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Any, Union, List

@dataclass(frozen=True)
class DiscoveryPayload(ABC):
    content: Any                    # Primary product of interrogation
    identity: Union[str, object]    # Represents the "Screaming" name
    is_valid: bool                  # Allows BaseOrchestrator to filter

    @abstractmethod
    def validate(self) -> List[Exception]:
        """Detailed Architectural Audit"""
        pass