# tests/unit/core/kernel/contracts/test_base_factory.py

import pytest
from typing import Any, Dict, Type
from src.core.kernel.contracts.factory import BaseFactory

# --- STUB IMPLEMENTATIONS ---

class Product:
    def __init__(self, name: str):
        self.name = name
        self.finalized = False

class WrongProduct:
    """Used to test the Type Guard."""
    pass

class StubFactory(BaseFactory[Product]):
    @property
    def specification(self) -> Dict[str, Any]:
        return {"name": str}

    @property
    def target(self) -> Type[Product]:
        return Product

    def prepare(self, **kwargs) -> Dict[str, Any]:
        return {k: v.strip() if isinstance(v, str) else v for k, v in kwargs.items()}

    def validate(self, **data: Any) -> None:
        if "name" not in data or not data["name"]:
            raise ValueError("Valid name required")

    def instantiate(self, **processed) -> Product:
        # Check for a 'sabotage' flag to return the wrong type
        if processed.get("sabotage"):
            return WrongProduct()  # type: ignore
        return Product(**processed)

    def finalize(self, instance: Product) -> Product:
        instance.finalized = True
        return instance

# --- TESTS ---

def test_factory_lifecycle_success():
    """Verify full successful lifecycle execution."""
    factory = StubFactory()
    product = factory.build(name="  Oregon Trail  ")

    assert product.name == "Oregon Trail"  # prepare() worked
    assert product.finalized is True       # finalize() worked
    assert isinstance(product, Product)

def test_factory_validation_exception():
    """Verify that validate() correctly halts execution via exceptions."""
    factory = StubFactory()
    with pytest.raises(ValueError, match="Valid name required"):
        factory.build(name="")

def test_factory_type_guard_violation():
    """Verify the new runtime Type Guard catches incorrect product types."""
    factory = StubFactory()
    # Trigger the sabotage logic in our stub
    with pytest.raises(TypeError, match=r"\[FACTORY VIOLATION\].*Produced: 'WrongProduct', Expected: 'Product'"):
        factory.build(name="Saboteur", sabotage=True)

def test_abstract_instantiation_fails():
    """Ensure the base class remains abstract."""
    with pytest.raises(TypeError):
        BaseFactory() # type: ignore
