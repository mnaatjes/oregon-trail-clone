# src/core/contracts/domain/blueprints/record.py

from dataclasses import dataclass
from abc import ABC, abstractmethod

from core.domain.contracts.blueprints.base import BaseBlueprint
from core.domain.contracts.blueprints.display import DisplayBlueprint
from core.domain.contracts.taxonomy import DomainFamily

@dataclass(frozen=True)
class RecordBlueprint(BaseBlueprint):
    """
    Abstract base for RECORD/LEAF templates.
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
        return DomainFamily.LEAF