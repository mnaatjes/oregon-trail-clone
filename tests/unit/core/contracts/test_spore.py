import pytest
from dataclasses import dataclass
from src.core.contracts.domain.spore import DomainSpore

def test_valid_spore_definition():
    """Verify that a standard Spore with valid fields can be defined and instantiated."""
    @dataclass(frozen=True)
    class Money(DomainSpore):
        species = "money"
        amount: int
        currency: str

    m = Money(amount=100, currency="USD")
    assert m.amount == 100
    assert m.currency == "USD"
    assert m.species == "money"

def test_species_accessible_from_class():
    """Verify that species is accessible from the class reference (for Discovery)."""
    class Coord(DomainSpore):
        species = "coordinates"
        x: int
        y: int
    
    assert Coord.species == "coordinates"

def test_missing_species_raises_error():
    """Verify that a Spore cannot be instantiated if species is missing."""
    @dataclass(frozen=True)
    class IncompleteSpore(DomainSpore):
        value: int
    
    with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteSpore"):
        IncompleteSpore(value=10)

@pytest.mark.parametrize("forbidden_name", [
    "id", "uid", "uuid", "slug", "breed", "pk", "pkey", "_id", "ID", "uId", "BREED"
])
def test_identity_purity_guard_blocks_forbidden_fields(forbidden_name):
    """Verify that any attribute in the forbidden list triggers a TypeError at class definition."""
    with pytest.raises(TypeError) as excinfo:
        # Manually create the class to trigger __init_subclass__
        type("BadSpore", (DomainSpore,), {forbidden_name: "some-value", "species": "bad"})

    assert "[IDENTITY VIOLATION]" in str(excinfo.value)
    assert f"'{forbidden_name}'" in str(excinfo.value)

def test_guard_blocks_forbidden_properties():
    """Verify that properties with forbidden names are also blocked."""
    with pytest.raises(TypeError) as excinfo:
        class PropertySpore(DomainSpore):
            species = "property"
            @property
            def breed(self):
                return "forbidden"

    assert "[IDENTITY VIOLATION]" in str(excinfo.value)
    assert "'breed'" in str(excinfo.value)

def test_spore_immutability():
    """Verify that Spores are frozen and cannot be modified after creation."""
    @dataclass(frozen=True)
    class Point(DomainSpore):
        species = "point"
        x: int
        y: int

    p = Point(x=1, y=2)
    with pytest.raises(Exception): # FrozenInstanceError
        p.x = 10

def test_spore_validation_hook():
    """Verify that the validate() hook is called during post-init."""
    @dataclass(frozen=True)
    class PositiveNumber(DomainSpore):
        species = "number"
        value: int

        def validate(self):
            if self.value < 0:
                raise ValueError("Must be positive")

    with pytest.raises(ValueError, match="Must be positive"):
        PositiveNumber(value=-1)
    
    # Should work
    assert PositiveNumber(value=10).value == 10
