# src/core/contracts/state.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace

@dataclass
class DomainState(ABC):
    """
    Abstract base for all mutable state containers.
    Unlike Value Objects, these change over time.
    """
    
    def clone(self, **changes):
        """
        Returns a new instance of the state with updated values.
        Useful for 'Time-Travel' debugging or preventing accidental 
        mutation in sensitive logic.
        """
        return replace(self, **changes)

    @abstractmethod
    def validate(self) -> bool:
        """
        Ensures the state hasn't reached an impossible 
        mathematical condition (e.g., negative weight).
        """
        pass