# tests/unit/core/contracts/test_blueprint_guards.py

import pytest
from dataclasses import dataclass
from src.core.contracts.domain.blueprints.base import BaseBlueprint
from src.core.contracts.domain.blueprints.root import RootBlueprint
from src.core.contracts.domain.blueprints.record import RecordBlueprint
from src.core.contracts.domain.blueprints.display import DisplayBlueprint
from src.core.contracts.domain.taxonomy import DomainFamily

@dataclass(frozen=True)
class ValidRoot(RootBlueprint):
    @property
    def species(self) -> str: return "valid"

@dataclass(frozen=True)
class ValidRecord(RecordBlueprint):
    @property
    def species(self) -> str: return "valid"

def test_identity_purity_guard():
    """Verify that blueprints cannot have ID fields."""
    with pytest.raises(TypeError) as info:
        @dataclass(frozen=True)
        class BadBlueprint(RootBlueprint):
            id: str = "fail"
            @property
            def species(self) -> str: return "fail"
    
    assert "IDENTITY VIOLATION" in str(info.value)

def test_spore_prohibition_guard():
    """Verify that blueprints cannot claim to be Spores."""
    @dataclass(frozen=True)
    class SporeBlueprint(RootBlueprint):
        @property
        def species(self) -> str: return "fail"
        @property
        def family(self) -> DomainFamily: return DomainFamily.SPORE

    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        SporeBlueprint(breed="test", display=display)
    
    assert "TAXONOMY VIOLATION" in str(info.value)

def test_dna_audit_root_mismatch():
    """Verify that a RootBlueprint must report ROOT family."""
    @dataclass(frozen=True)
    class MismatchedRoot(RootBlueprint):
        @property
        def species(self) -> str: return "fail"
        @property
        def family(self) -> DomainFamily: return DomainFamily.LEAF

    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        MismatchedRoot(breed="test", display=display)
    
    assert "DNA MISMATCH" in str(info.value)
    assert "RootBlueprint" in str(info.value)

def test_dna_audit_record_mismatch():
    """Verify that a RecordBlueprint must report LEAF family."""
    @dataclass(frozen=True)
    class MismatchedRecord(RecordBlueprint):
        @property
        def species(self) -> str: return "fail"
        @property
        def family(self) -> DomainFamily: return DomainFamily.ROOT

    display = DisplayBlueprint(asset_id="any", label="any")
    with pytest.raises(TypeError) as info:
        MismatchedRecord(breed="test", display=display)
    
    assert "DNA MISMATCH" in str(info.value)
    assert "RecordBlueprint" in str(info.value)

def test_valid_instantiation():
    """Ensure valid blueprints still work."""
    display = DisplayBlueprint(asset_id="any", label="any")
    root = ValidRoot(breed="test", display=display)
    record = ValidRecord(breed="test", display=display)
    
    assert root.family == DomainFamily.ROOT
    assert record.family == DomainFamily.LEAF
