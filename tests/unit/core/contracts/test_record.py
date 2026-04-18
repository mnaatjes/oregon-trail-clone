# tests/unit/core/contracts/test_record.py

from typing import Self

import pytest
from rich import inspect
from dataclasses import dataclass, FrozenInstanceError, replace
from src.core.contracts.domain.record import DomainRecord

@dataclass(frozen=True)
class WheelRecord(DomainRecord):
    axel:int = 1
    pegs: int = 4

    def clone(self, **changes) -> 'WheelRecord':
        return replace(self, **changes)

    def validate(self) -> bool:
        if self.axel > 1:
            raise ValueError(f"[INVALID] {self.axel} cannot be more than 1")
        # return default
        return True

def test_instance_creation():
    """Ensure proper instantiation and heritability"""
    instance = WheelRecord()

    assert isinstance(instance, DomainRecord)
    assert isinstance(instance, WheelRecord)

def test_horizontal_isolation_guard():
    """Verify __init_subclass__ catches illegal DomainRecord
    property creations"""
    with pytest.raises(TypeError) as info:

        class FailRecord(DomainRecord):
            title: str = "Structural Failure"
            violation: DomainRecord = WheelRecord()

            def clone(self):
                return self
            
            def validate(self) -> bool:
                return False
    
    assert "STRUCTURAL SIBLING CONFLICT" in str(info.value)

def test_immutable_properties():
    """Ensure frozen properties cannot be changed"""
    instance = WheelRecord()

    with pytest.raises(FrozenInstanceError) as info:
        instance.axel = 4 #type: ignore

    assert "cannot assign" in str(info.value)

def test_clone_method():
    """Ensure deep copy clone executes successfully and
    typing for DomainRecord corresponds to outputs"""
    original = WheelRecord()
    copy = original.clone(pegs=8)
    
    assert original is not copy
    assert original != copy
    assert isinstance(copy, WheelRecord)
    assert hasattr(copy, "pegs")
    assert hasattr(copy, "axel")
    assert copy.pegs == 8

def test_self_validation():
    wheel = WheelRecord(axel=4)

    with pytest.raises(ValueError) as info:
        result = wheel.validate()
        assert result == None
        assert result != True

    assert "INVALID" in str(info.value)

    new_wheel = WheelRecord(axel=1)
    result = new_wheel.validate()
    assert result == True

def test_identity_property_violation():

    with pytest.raises(ValueError) as info:

        class FailRecord(DomainRecord):
            id:str = "will-fail"

            def clone(self) -> Self:
                return super().clone()
            
            def validate(self) -> bool:
                return super().validate()
            
    assert "ANONYMITY VIOLATION" in str(info.value)

def test_abstraction_guard():

    with pytest.raises(TypeError) as info:

        instance = DomainRecord() # type: ignore

    assert "Can't instantiate" in str(info.value)