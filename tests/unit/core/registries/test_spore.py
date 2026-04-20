# tests/unit/core/registries/test_spore.py

import pytest
from src.core.registries import spores
from core.kernel.contracts.domain.spore import DomainSpore

@pytest.fixture(autouse=True)
def clear_registry():
    """Ensure a clean registry state before each test."""
    spores.all().clear()

class MockSpore(DomainSpore):
    """A valid mock spore for testing."""
    pass

def test_spores_singleton_import():
    """Verify that the spores registry is correctly exported via facade."""
    from src.core.registries import spores as exported_spores
    assert exported_spores is spores

def test_register_and_get_spore():
    """Verify registration and retrieval of a valid DomainSpore."""
    spores.register("mock_spore", MockSpore)
    
    retrieved = spores.get("mock_spore")
    assert retrieved is MockSpore
    assert issubclass(retrieved, DomainSpore)

def test_spore_existence():
    """Verify exists() logic."""
    spores.register("active", MockSpore)
    
    assert spores.exists("active") is True
    assert spores.exists("ghost") is False

def test_get_non_existent():
    """Verify that getting a missing spore returns None."""
    assert spores.get("missing") is None

def test_registry_all_access():
    """Verify that all() returns the internal dictionary."""
    spores.register("s1", MockSpore)
    assert len(spores.all()) == 1
    assert "s1" in spores.all()
