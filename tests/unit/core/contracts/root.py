# tests/unit/core/contracts/root.py

from typing import Self

import pytest
from dataclasses import dataclass
from rich import inspect
from src.core.contracts.domain.blueprint import DomainBlueprint, DisplayBlueprint
from src.core.contracts.domain.root import DomainRoot
from src.core.contracts.domain.record import DomainRecord

display = DisplayBlueprint(
    asset_id="test-asset-id",
    label="test-label",
    description="test-description"
)

class WheelBP(DomainBlueprint):
    axel:int

    @property
    def __species__(self) -> str: return "part"


@pytest.fixture
def bp():
    return WheelBP(
        slug="Conestoga",
        display=display
    )

def test_initialization_domain_root(bp):

    class WagonRoot(DomainRoot):

        def clone(self) -> Self:
            return super().clone()

    wagon = WagonRoot(
        uid="test-uuid-string",
        blueprint=bp,
        records={}
    )

    #inspect(wagon)