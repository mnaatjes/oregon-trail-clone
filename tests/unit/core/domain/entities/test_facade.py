import pytest
from core.domain.entities.facade import Facade
from core.domain.contracts.context import DomainContext
from core.domain.contracts.blueprints.root import RootBlueprint
from dataclasses import dataclass

# Simple Mock classes since MagicMock is forbidden
class MockModuleSpec:
    def __init__(self, name):
        self.name = name

class MockModule:
    pass

@dataclass(frozen=True)
class MockBlueprint(RootBlueprint):
    species = "mock"
    breed = "mock"
    display = None

def test_facade_instantiation():
    # Setup
    mock_spec = MockModuleSpec("domain.wagon")
    mock_module = MockModule()
    
    # We can use a real DomainContext with mock values
    mock_context = DomainContext(
        intent=MockBlueprint,
        priority=10,
        service=object # Mock service
    )
    
    facade = Facade(
        name="wagon",
        spec=mock_spec, # type: ignore
        module=mock_module, # type: ignore
        file="/path/to/wagon/__init__.py",
        context=mock_context
    )
    
    assert facade.name == "wagon"
    assert facade.spec == mock_spec
    assert facade.module == mock_module
    assert facade.file == "/path/to/wagon/__init__.py"
    assert facade.context == mock_context
