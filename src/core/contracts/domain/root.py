# src/core/contracts/domain/root.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict
from src.core.contracts.domain.record import DomainRecord
from src.core.contracts.domain.blueprint import DomainBlueprint

@dataclass(frozen=True)
class DomainRoot(ABC):
    """
    """
    uid: str    # Soveriegn Identity
    blueprint: DomainBlueprint  # Static Template
    records: Dict[str, DomainRecord] = field(default_factory=dict)

    @property
    def __species__(self) -> str:
        """"""
        return self.blueprint.__species__ 

