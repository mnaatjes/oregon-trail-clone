# src/core/contracts/blueprint.py

from dataclasses import dataclass

@dataclass(frozen=True)
class DomainBlueprint:
    """
    Abstract base for all domain templates.
    Ensures every blueprint has at least a unique identifier.
    """
    slug: str  # e.g., 'cholera', 'blizzard', 'farmer'