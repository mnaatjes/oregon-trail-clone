# src/core/contracts/domain/blueprints/root.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.core.contracts.domain.blueprints.base import BaseBlueprint
from src.core.contracts.domain.blueprints.display import DisplayBlueprint
from src.core.contracts.domain.taxonomy import DomainFamily

@dataclass(frozen=True)
class RootBlueprint(BaseBlueprint):
    """
    Abstract base for all ROOT templates.
    - Breed Property (fmr. "slug") ensures every blueprint has at least a unique identifier.
    - Read-only
    - Global Template
    - Shared across many instances
    - Loaded from assets (e.g. assets/professions.json)
    """

    @property
    @abstractmethod
    def species(self) -> str:
        """The taxonomic branch (e.g., "wagon", "character")"""
        pass

    @property
    def family(self) -> DomainFamily:
        """The architectural role (ROOT or LEAF)."""
        return DomainFamily.ROOT