# src/core/domain/entities/facade.py

from dataclasses import dataclass
from types import ModuleType
from importlib.machinery import ModuleSpec
from pathlib import Path
from core.domain.contracts.context import DomainContext

@dataclass(frozen=True)
class Facade:
    name: str
    spec: ModuleSpec
    module: ModuleType
    file: str
    context: DomainContext