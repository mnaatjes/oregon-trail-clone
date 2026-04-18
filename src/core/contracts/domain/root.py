# src/core/contracts/domain/root.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, is_dataclass
from typing import Any, Dict, Self
from src.core.contracts.domain.record import DomainRecord
from src.core.contracts.domain.blueprint import DomainBlueprint

@dataclass(frozen=True)
class DomainRoot(ABC):
    """
    """
    uid: str    # Soveriegn Identity
    blueprint: DomainBlueprint  # Static Template
    records: Dict[str, DomainRecord] = field(default_factory=dict)

    def __init_subclass__(cls, **kwargs) -> None:
        """
        Enforces global and architectural rules:
        - Anemic Purity: dataclass and is frozen
        - Horizontal Isolation: DomainRoot CANNOT contain another DomainRoot
        """
        super().__init_subclass__(**kwargs)

        # Anemic Purity(
        if not is_dataclass(cls):
            raise TypeError(
                f"[ANEMIC VIOLATION] in '{cls.__name__}' MUST be a dataclass"
            )
        
        # Frozen state
        params = getattr(cls, "__dataclass_params__", None)
        print(params)


    @property
    def __species__(self) -> str:
        """"""
        return self.blueprint.__species__ 
    
    @abstractmethod
    def clone(self) -> Self:
        pass

