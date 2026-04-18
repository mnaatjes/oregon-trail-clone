# tests/unit/core/contracts/test_blueprint.py
import pytest
from rich import inspect
from src.core.contracts.domain.blueprint import DomainBlueprint, DisplayBlueprint
from dataclasses import FrozenInstanceError

def test_immutability():
    """Create an instance and attempt to change slug"""
    bp = DomainBlueprint(
        slug="mySlug",
        display=DisplayBlueprint(
            asset_id="some-asset-id",
            label="label"
        )
    )

    # check created
    assert type(bp) is DomainBlueprint

    # Fail slug change
    with pytest.raises(FrozenInstanceError) as info:
        bp.slug = "New Slug Faiure" # type: ignore

    # Fail Nested immutability
    with pytest.raises(FrozenInstanceError):
        bp.display.label = "New Label" # type: ignore

def test_abstraction_guard():
    """DomainBlueprint cannot exist on its own"""
    