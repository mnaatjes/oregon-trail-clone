# src/core/contracts/domain/blueprints/display.py

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class DisplayBlueprint:
    """
    Defines the display characteristics for a Domain blueprint
    """
    asset_id: str         # Pointer to specific asset
    label: str            # Player-facing name for human readability
    description: str = "" # Text Description 