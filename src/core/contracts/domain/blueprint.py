# src/core/contracts/blueprint.py
from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True)
class DomainBlueprint(ABC):
    """
    Abstract base for all domain templates.
    - Slug Property ensures every blueprint has at least a unique identifier.
    - Read-only
    - Global Template
    - Shared accross many instances
    - Loaded from assets (e.g. assets/professions.json)
    """
    slug: str  # e.g., 'cholera', 'blizzard', 'farmer'
    