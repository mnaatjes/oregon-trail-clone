# tests/unit/core/contracts/test_blueprint.py

import pytest
from dataclasses import dataclass, FrozenInstanceError
from src.core.contracts.domain.blueprints.base import BaseBlueprint
from src.core.contracts.domain.blueprints.root import RootBlueprint
from src.core.contracts.domain.blueprints.record import RecordBlueprint
from src.core.contracts.domain.blueprints.display import DisplayBlueprint
from src.core.contracts.domain.taxonomy import DomainFamily

# --- Test Helpers ---

@dataclass(frozen=True)
class MockBlueprint(BaseBlueprint):
    """Concrete implementation for testing purposes."""
    
    @property
    def species(self) -> str:
        return "mock-species"

    @property
    def family(self) -> DomainFamily:
        return DomainFamily.ROOT

@dataclass(frozen=True)
class MockRoot(RootBlueprint):
    @property
    def species(self) -> str:
        return "root-species"

@dataclass(frozen=True)
class MockRecord(RecordBlueprint):
    @property
    def species(self) -> str:
        return "record-species"

# --- BaseBlueprint Tests ---

def test_base_blueprint_abstraction():
    """Ensure BaseBlueprint cannot be instantiated directly as it is an ABC."""
    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        # pylint: disable=abstract-class-instantiated
        instance = BaseBlueprint(breed="test", display=display) # type: ignore
    
    assert "Can't instantiate abstract class BaseBlueprint" in str(info.value)

def test_base_blueprint_fields():
    """Verify standard fields are correctly inherited and stored."""
    display = DisplayBlueprint(asset_id="asset-1", label="Mock Label")
    blueprint = MockBlueprint(breed="mock-breed", display=display)

    assert blueprint.breed == "mock-breed"
    assert blueprint.display.label == "Mock Label"
    assert blueprint.display.asset_id == "asset-1"

def test_base_blueprint_immutability():
    """Ensure BaseBlueprint fields are frozen."""
    display = DisplayBlueprint(asset_id="asset-1", label="Mock Label")
    blueprint = MockBlueprint(breed="mock-breed", display=display)

    with pytest.raises(FrozenInstanceError):
        blueprint.breed = "new-breed" # type: ignore

    with pytest.raises(FrozenInstanceError):
        blueprint.display = DisplayBlueprint(asset_id="new", label="new") # type: ignore

# --- RootBlueprint Tests ---

def test_root_blueprint_abstraction():
    """Ensure RootBlueprint cannot be instantiated directly."""
    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        instance = RootBlueprint(breed="test", display=display) # type: ignore
    assert "Can't instantiate abstract class RootBlueprint" in str(info.value)

def test_root_blueprint_implementation():
    """Verify RootBlueprint provides family and inherits fields."""
    display = DisplayBlueprint(asset_id="r1", label="Root")
    blueprint = MockRoot(breed="breed1", display=display)

    assert blueprint.family == DomainFamily.ROOT
    assert blueprint.species == "root-species"
    assert blueprint.breed == "breed1"
    assert isinstance(blueprint, RootBlueprint)

# --- RecordBlueprint Tests ---

def test_record_blueprint_abstraction():
    """Ensure RecordBlueprint cannot be instantiated directly."""
    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        instance = RecordBlueprint(breed="test", display=display) # type: ignore
    assert "Can't instantiate abstract class RecordBlueprint" in str(info.value)

def test_record_blueprint_implementation():
    """Verify RecordBlueprint provides family and inherits fields."""
    display = DisplayBlueprint(asset_id="rec1", label="Record")
    blueprint = MockRecord(breed="breed2", display=display)

    assert blueprint.family == DomainFamily.LEAF
    assert blueprint.species == "record-species"
    assert blueprint.breed == "breed2"
    assert isinstance(blueprint, RecordBlueprint)
