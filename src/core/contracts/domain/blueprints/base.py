# src/core/contracts/blueprint.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DisplayBlueprint:
    """
    Defines the display characteristics for a Domain blueprint
    """
    asset_id: str         # Pointer to specific asset
    label: str            # Player-facing name for human readability
    description: str = "" # Text Description 

@dataclass(frozen=True)
class BaseBlueprint(ABC):
    """
    Abstract base for all domain templates.
    - Breed Property (fmr. "slug") ensures every blueprint has at least a unique identifier.
    - Read-only
    - Global Template
    - Shared accross many instances
    - Loaded from assets (e.g. assets/professions.json)
    """
    breed: str  # Variant: e.g., 'cholera', 'blizzard', 'farmer'
    display: DisplayBlueprint

    @property
    @abstractmethod
    def __species__(self) -> str:
        """Enforces abstration and identifies the blueprint species"""