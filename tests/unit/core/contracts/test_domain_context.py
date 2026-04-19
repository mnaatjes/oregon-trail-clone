# tests/unit/core/contracts/domain/test_domain_context.py

import pytest
from dataclasses import dataclass
from rich import inspect
from src.core.contracts.domain.context import DomainContext, DomainFamily

def test_init():
    context = DomainContext(
        family=DomainFamily.LEAF,
        intent="test-intent",
        priority=2,
        requirements=[]
    )

    inspect(context)