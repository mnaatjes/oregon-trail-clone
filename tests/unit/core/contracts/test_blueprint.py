import pytest
from abc import ABC
from dataclasses import dataclass, FrozenInstanceError
from src.core.contracts.domain.blueprint import DomainBlueprint, DisplayBlueprint

# --- Test Helpers ---

@dataclass(frozen=True)
class MockBlueprint(DomainBlueprint):
    """Concrete implementation for testing purposes."""
    @property
    def __species__(self) -> str:
        return "mock"

@pytest.fixture
def valid_display():
    return DisplayBlueprint(
        asset_id="asset.test",
        label="Test Item",
        description="A test item for verification."
    )

# --- Tests ---

def test_abstraction_guard(valid_display):
    """Verify that DomainBlueprint cannot be instantiated even with valid data."""
    with pytest.raises(TypeError) as exc_info:
        # Attempting to instantiate the ABC directly
        DomainBlueprint(slug="test-slug", display=valid_display) # type: ignore
        
    assert "Can't instantiate abstract class DomainBlueprint" in str(exc_info.value)
    assert "__species__" in str(exc_info.value)

def test_species_enforcement(valid_display):
    """Verify that subclasses MUST implement __species__ to be instantiated."""
    class BrokenBlueprint(DomainBlueprint):
        pass # Missing __species__ implementation
        
    with pytest.raises(TypeError) as exc_info:
        BrokenBlueprint(slug="test", display=valid_display) # type: ignore
    
    assert "__species__" in str(exc_info.value)

def test_immutability_guard(valid_display):
    """Verify that blueprints are frozen and cannot be modified after creation."""
    bp = MockBlueprint(slug="stable-slug", display=valid_display)
    
    with pytest.raises(FrozenInstanceError):
        bp.slug = "mutated-slug" # type: ignore

def test_deep_freeze_guard(valid_display):
    """Verify that nested display metadata is also frozen."""
    bp = MockBlueprint(slug="test", display=valid_display)
    
    with pytest.raises(FrozenInstanceError):
        bp.display.label = "Attempted Hack" # type: ignore

def test_blueprint_equality(valid_display):
    """Verify that two blueprints with identical data are considered equal."""
    bp1 = MockBlueprint(slug="standard", display=valid_display)
    bp2 = MockBlueprint(slug="standard", display=valid_display)
    
    assert bp1 == bp2           # Data equality should be True
    assert bp1 is not bp2       # Instance identity should be False

def test_blueprint_slug_integrity(valid_display):
    """Verify the slug is correctly stored and accessible."""
    bp = MockBlueprint(slug="domain.test.item", display=valid_display)
    assert bp.slug == "domain.test.item"
    assert bp.__species__ == "mock"
