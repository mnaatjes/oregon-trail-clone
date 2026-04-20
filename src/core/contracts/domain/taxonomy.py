# src/core/contracts/domain/taxonomy.py

from enum import Enum, auto

class DomainFamily(Enum):
    ROOT = auto()
    LEAF = auto()
    SPORE = auto()