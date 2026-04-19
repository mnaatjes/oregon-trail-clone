# tests/unit/core/contracts/domain/context.py

import pytest
from dataclasses import dataclass
from rich import inspect
from src.core.contracts.domain.context import DomainContext

def test_init():
    context = DomainContext(
        family="LEAF",
        intent="test-intent",
        priority=2,
        pillars=[],
        provider=None
    )