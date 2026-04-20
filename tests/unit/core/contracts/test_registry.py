# tests/unit/core/contracts/test_registry.py

from dataclasses import dataclass

import pytest
from src.core.contracts.registry import BaseRegistry
from src.core.contracts.domain.blueprints.record import RecordBlueprint
from src.core.contracts.domain.blueprints.display import DisplayBlueprint
from src.core.contracts.domain.taxonomy import DomainFamily

@pytest.fixture
def display_bp():
    return DisplayBlueprint(
        asset_id="asset-id",
        label="Some label"
    )

@dataclass(frozen=True)
class MaladyBlueprint(RecordBlueprint):
    """Concrete implementation of a RecordBlueprint for testing."""
    name: str = ""
    description: str = ""
    symptoms: list[str] = None
    damage_per_day: int = 0
    recovery_time_days: int = 0

    @property
    def species(self) -> str:
        return "malady"

class MockMaladyRegistry(BaseRegistry[MaladyBlueprint]):
    def hydrate(self, raw_data: dict, display: DisplayBlueprint) -> None:
        for breed, data in raw_data.items():
            # Merge breed and display into the data dict for constructor
            init_data = {"breed": breed, "display": display, **data}
            blueprint = MaladyBlueprint(**init_data)
            self.register(breed, blueprint)

def test_registry_registration_and_retrieval(display_bp):
    registry = MockMaladyRegistry()
    
    # Sample data to hydrate the registry
    raw_data = {
        "cholera": {
            "name": "Cholera",
            "description": "An infectious disease causing severe diarrhea.",
            "symptoms": ["diarrhea", "dehydration", "vomiting"],
            "damage_per_day": 10,
            "recovery_time_days": 7
        },
        "blizzard": {
            "name": "Blizzard",
            "description": "A severe snowstorm with strong winds.",
            "symptoms": ["hypothermia", "frostbite"],
            "damage_per_day": 15,
            "recovery_time_days": 14
        }
    }
    
    registry.hydrate(raw_data, display_bp)
    
    cholera = registry.get("cholera")
    blizzard = registry.get("blizzard")
    
    assert cholera is not None
    assert cholera.name == "Cholera"
    assert cholera.family == DomainFamily.LEAF
    
    assert blizzard is not None
    assert blizzard.name == "Blizzard"
    assert blizzard.species == "malady"
    
    # Test retrieval of non-existent blueprint
    non_existent = registry.get("non_existent")
    assert non_existent is None

def test_registry_all(display_bp):
    registry = MockMaladyRegistry()
    
    raw_data = {
        "cholera": {
            "name": "Cholera",
            "damage_per_day": 10
        },
        "blizzard": {
            "name": "Blizzard",
            "damage_per_day": 15
        }
    }
    
    registry.hydrate(raw_data, display_bp)
    all_blueprints = registry.all()
    
    assert len(all_blueprints) == 2
    assert "cholera" in all_blueprints
    assert "blizzard" in all_blueprints
    assert all_blueprints["cholera"].name == "Cholera"

def test_registry_overwrite(display_bp):
    registry = MockMaladyRegistry()
    
    raw_data = {
        "cholera": {
            "name": "Cholera",
            "damage_per_day": 10
        }
    }
    
    registry.hydrate(raw_data, display_bp)
    
    # Overwrite existing blueprint
    new_cholera = MaladyBlueprint(
        breed="cholera",
        display=display_bp,
        name="Cholera Updated",
        damage_per_day=12
    )
    registry.register("cholera", new_cholera)
    
    cholera = registry.get("cholera")
    assert cholera is not None
    assert cholera.name == "Cholera Updated"
    assert cholera.damage_per_day == 12

def test_registry_empty():
    registry = MockMaladyRegistry()
    assert registry.all() == {}
    assert registry.get("non_existent") is None

def test_registry_exists(display_bp):
    registry = MockMaladyRegistry()
    blueprint = MaladyBlueprint(breed="test", display=display_bp)
    registry.register("test", blueprint)
    
    assert registry.exists("test") is True
    assert registry.exists("fake") is False

def test_registry_duplicate_registration(display_bp):
    registry = MockMaladyRegistry()
    
    blueprint1 = MaladyBlueprint(breed="cholera", display=display_bp, name="C1")
    blueprint2 = MaladyBlueprint(breed="cholera", display=display_bp, name="C2")
    
    registry.register("cholera", blueprint1)
    registry.register("cholera", blueprint2) # Overwrite
    
    cholera = registry.get("cholera")
    assert cholera.name == "C2"
