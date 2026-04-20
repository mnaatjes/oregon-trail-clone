# tests/unit/core/contracts/root.py

from typing import Self, Dict, Any
import pytest
from dataclasses import dataclass, field, replace
from uuid import uuid4, UUID
from core.kernel.contracts.domain.blueprints.base import BaseBlueprint, DisplayBlueprint
from core.kernel.contracts.domain.root import DomainRoot
from core.kernel.contracts.domain.record import DomainRecord
from core.kernel.contracts.domain.taxonomy import DomainFamily

# --- Shared Mocks ---

display = DisplayBlueprint(
    asset_id="test-asset",
    label="Test Label",
    description="Test Description"
)

class MockBlueprint(BaseBlueprint):
    @property
    def species(self) -> str:
        return "mock_species"
    
    @property
    def family(self):
        return DomainFamily.ROOT

@dataclass(frozen=True)
class MockRecord(DomainRecord):
    val: int = 1
    def clone(self) -> Self:
        return MockRecord(val=self.val) #type: ignore
    def validate(self) -> bool:
        return True

@pytest.fixture
def bp():
    return MockBlueprint(breed="test-slug", display=display)

# --- Test Cases ---

def test_initialization_domain_root(bp):
    """Verify standard initialization of a DomainRoot."""
    @dataclass(frozen=True)
    class WagonRoot(DomainRoot):
        def clone(self) -> Self:
            return replace(self, records={k: v.clone() for k, v in self.records.items()})

    uid = uuid4()
    wagon = WagonRoot(uid=uid, blueprint=bp)
    
    assert wagon.uid == uid
    assert wagon.blueprint == bp
    assert wagon.records == {}

def test_horizontal_violation_declaration(bp):
    """Verify that DomainRoot cannot be used as a type hint in another Root."""
    with pytest.raises(TypeError) as info:
        @dataclass(frozen=True)
        class InvalidRoot(DomainRoot):
            other: DomainRoot # type: ignore
            def clone(self) -> Self: return self
            
    assert "HORIZONTAL VIOLATION" in str(info.value)

def test_horizontal_violation_runtime(bp):
    """Verify that DomainRoot cannot be snuck in via 'Any' type hints."""
    @dataclass(frozen=True)
    class TargetRoot(DomainRoot):
        def clone(self) -> Self: return self

    @dataclass(frozen=True)
    class AttackerRoot(DomainRoot):
        sneaky: Any = None # Added default to follow records=default
        def clone(self) -> Self: return self

    target = TargetRoot(uid=uuid4(), blueprint=bp)
    
    with pytest.raises(TypeError) as info:
        AttackerRoot(uid=uuid4(), blueprint=bp, sneaky=target)
        
    assert "HORIZONTAL VIOLATION" in str(info.value)

def test_vertical_violation(bp):
    """Verify that only DomainRecords can be added to the records registry."""
    @dataclass(frozen=True)
    class WagonRoot(DomainRoot):
        def clone(self) -> Self: return self

    with pytest.raises(TypeError) as info:
        WagonRoot(
            uid=uuid4(),
            blueprint=bp,
            records={"broken": "not-a-record"} # type: ignore
        )
    assert "VERTICAL VIOLATION" in str(info.value)

def test_sovereignty_violation(bp):
    """Verify that uid MUST be a UUID object."""
    @dataclass(frozen=True)
    class WagonRoot(DomainRoot):
        def clone(self) -> Self: return self

    with pytest.raises(TypeError) as info:
        WagonRoot(uid="not-a-uuid", blueprint=bp) # type:ignore
        
    assert "SOVEREIGNTY VIOLATION" in str(info.value)

def test_anemic_purity_violation(bp):
    """Verify that DomainRoot subclasses must be frozen dataclasses."""
    # Attempting to define a non-frozen dataclass should fail 
    # because the parent is already frozen.
    with pytest.raises(TypeError):
        @dataclass(frozen=False) # type: ignore
        class MutableRoot(DomainRoot):
            def clone(self) -> Self: return self

def test_deep_clone_mechanism(bp):
    """Verify that cloning produces a true deep copy of the records."""
    @dataclass(frozen=True)
    class WagonRoot(DomainRoot):
        def clone(self) -> Self:
            return replace(self, records={k: v.clone() for k, v in self.records.items()})

    rec = MockRecord(val=10)
    original = WagonRoot(uid=uuid4(), blueprint=bp, records={"r1": rec})
    cloned = original.clone()

    assert original is not cloned
    assert original.records["r1"] is not cloned.records["r1"]
    assert original.records["r1"].val == cloned.records["r1"].val # type:ignore
