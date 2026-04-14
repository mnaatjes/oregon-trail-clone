# tests/unit/core/contracts/test_registry.py

from dataclasses import dataclass

import pytest
from rich import inspect
from core.contracts.domain.registry import BaseRegistry
from core.contracts.domain.blueprint import DomainBlueprint

@dataclass(frozen=True)
class MaladyBlueprint(DomainBlueprint):
    # Properties from docs/design/characters.md
    slug: str
    name: str
    description: str
    symptoms: list[str]
    damage_per_day: int
    recovery_time_days: int

class MockMaladyRegistry(BaseRegistry[MaladyBlueprint]):
    def hydrate(self, raw_data: dict) -> None:
        for slug, data in raw_data.items():
            blueprint = MaladyBlueprint(**data)
            self.register(blueprint)

def test_registry_registration_and_retrieval():
    registry = MockMaladyRegistry()
    
    # Sample data to hydrate the registry
    raw_data = {
        "cholera": {
            "slug": "cholera",
            "name": "Cholera",
            "description": "An infectious disease causing severe diarrhea.",
            "symptoms": ["diarrhea", "dehydration", "vomiting"],
            "damage_per_day": 10,
            "recovery_time_days": 7
        },
        "blizzard": {
            "slug": "blizzard",
            "name": "Blizzard",
            "description": "A severe snowstorm with strong winds.",
            "symptoms": ["hypothermia", "frostbite"],
            "damage_per_day": 15,
            "recovery_time_days": 14
        }
    }
    
    registry.hydrate(raw_data)
    inspect(registry.all())  # Debug: Inspect the internal state of the registry
    cholera = registry.get("cholera")
    blizzard = registry.get("blizzard")
    
    assert cholera is not None
    assert cholera.name == "Cholera"
    assert cholera.damage_per_day == 10
    
    assert blizzard is not None
    assert blizzard.name == "Blizzard"
    assert blizzard.damage_per_day == 15
    
    # Test retrieval of non-existent blueprint
    non_existent = registry.get("non_existent")
    assert non_existent is None

def test_registry_all():
    registry = MockMaladyRegistry()
    
    raw_data = {
        "cholera": {
            "slug": "cholera",
            "name": "Cholera",
            "description": "An infectious disease causing severe diarrhea.",
            "symptoms": ["diarrhea", "dehydration", "vomiting"],
            "damage_per_day": 10,
            "recovery_time_days": 7
        },
        "blizzard": {
            "slug": "blizzard",
            "name": "Blizzard",
            "description": "A severe snowstorm with strong winds.",
            "symptoms": ["hypothermia", "frostbite"],
            "damage_per_day": 15,
            "recovery_time_days": 14
        }
    }
    
    registry.hydrate(raw_data)
    all_blueprints = registry.all()
    
    assert len(all_blueprints) == 2
    assert "cholera" in all_blueprints
    assert "blizzard" in all_blueprints
    assert all_blueprints["cholera"].name == "Cholera"
    assert all_blueprints["blizzard"].name == "Blizzard"

def test_registry_overwrite():
    registry = MockMaladyRegistry()
    
    raw_data = {
        "cholera": {
            "slug": "cholera",
            "name": "Cholera",
            "description": "An infectious disease causing severe diarrhea.",
            "symptoms": ["diarrhea", "dehydration", "vomiting"],
            "damage_per_day": 10,
            "recovery_time_days": 7
        }
    }
    
    registry.hydrate(raw_data)
    
    # Overwrite existing blueprint
    new_cholera_data = {
        "slug": "cholera",
        "name": "Cholera Updated",
        "description": "Updated description.",
        "symptoms": ["diarrhea", "dehydration"],
        "damage_per_day": 12,
        "recovery_time_days": 5
    }
    
    new_cholera_blueprint = MaladyBlueprint(**new_cholera_data)
    registry.register(new_cholera_blueprint)
    
    cholera = registry.get("cholera")
    assert cholera is not None
    assert cholera.name == "Cholera Updated"
    assert cholera.damage_per_day == 12

def test_registry_empty():
    registry = MockMaladyRegistry()
    assert registry.all() == {}
    assert registry.get("non_existent") is None

def test_registry_invalid_hydration():
    registry = MockMaladyRegistry()
    
    # Invalid data (missing required fields)
    invalid_data = {
        "invalid_malady": {
            "slug": "invalid_malady",
            "name": "Invalid Malady"
            # Missing description, symptoms, damage_per_day, recovery_time_days
        }
    }
    
    with pytest.raises(TypeError):
        registry.hydrate(invalid_data)

def test_registry_duplicate_registration():
    registry = MockMaladyRegistry()
    
    blueprint1 = MaladyBlueprint(
        slug="cholera",
        name="Cholera",
        description="An infectious disease causing severe diarrhea.",
        symptoms=["diarrhea", "dehydration", "vomiting"],
        damage_per_day=10,
        recovery_time_days=7
    )
    
    blueprint2 = MaladyBlueprint(
        slug="cholera",
        name="Cholera Duplicate",
        description="Duplicate entry.",
        symptoms=["diarrhea"],
        damage_per_day=8,
        recovery_time_days=5
    )
    
    registry.register(blueprint1)
    registry.register(blueprint2)  # This should overwrite the first blueprint
    
    cholera = registry.get("cholera")
    assert cholera is not None
    assert cholera.name == "Cholera Duplicate"
    assert cholera.damage_per_day == 8
