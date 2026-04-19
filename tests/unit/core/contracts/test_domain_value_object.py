# tests/unit/core/contracts/test_domain_value_object.py
import pytest
from dataclasses import dataclass, FrozenInstanceError
from typing import Any
from core.contracts.domain.spore import DomainSpore

# --- Shared Mocks ---

@dataclass(frozen=True)
class Money(DomainSpore):
    amount: float
    denomination: str = "USD"

    def validate(self) -> None:
        if self.amount < 0:
            raise ValueError("[VALUE ERROR] amount CANNOT be negative!")            

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            return NotImplemented
        return Money(amount=(self.amount + other.amount))

@dataclass(frozen=True)
class Coordinate(DomainSpore):
    x: float
    y: float

# --- Test Cases ---

def test_equality():
    """Verify that two distinct instances with same data are equal."""
    assert Money(0.50, "USD") == Money(0.50, "USD")
    assert Money(2) != Money(1)

def test_type_strict_equality():
    """Verify that different ValueObject types are never equal even with same data."""
    @dataclass(frozen=True)
    class Point(DomainSpore):
        x: float
        y: float
    
    assert Coordinate(1.0, 2.0) != Point(1.0, 2.0)

def test_validation():
    """Verify that internal validation triggers during instantiation."""
    with pytest.raises(ValueError) as info:
        Money(-0.1)
    assert "[VALUE ERROR]" in str(info.value)

def test_addition():
    """Verify that arithmetic operators return new instances."""
    m1 = Money(2)
    m2 = Money(2)
    result = m1 + m2

    assert isinstance(result, Money)
    assert result.amount == 4
    assert result is not m1
    assert result is not m2

def test_hashability():
    """Verify that Value Objects can be used as dictionary keys (requires being frozen)."""
    m1 = Money(10)
    m2 = Money(10)
    coord = Coordinate(1.0, 1.0)
    
    # Same data must result in same hash
    assert hash(m1) == hash(m2)
    
    # Usable as keys
    registry = {m1: "Found"}
    assert registry.get(m2) == "Found"
    assert coord in {coord}

def test_immutability():
    """Verify that fields cannot be modified after instantiation."""
    m = Money(10)
    with pytest.raises(FrozenInstanceError):
        # This should be blocked by the 'frozen=True' on DomainValueObject
        m.amount = 20 # type: ignore

def test_identity_guard():
    """Verify that identity fields (uid, id, etc) are prohibited at definition time."""
    with pytest.raises(TypeError) as info:        
        @dataclass(frozen=True)
        class House(DomainSpore):
            id: str
    assert "IDENTITY VIOLATION" in str(info.value)

def test_identity_guard_case_insensitive():
    """Verify that identity guard catches variations like UUID or Id."""
    with pytest.raises(TypeError) as info:
        @dataclass(frozen=True)
        class Token(DomainSpore):
            Uuid: str
    assert "IDENTITY VIOLATION" in str(info.value)
