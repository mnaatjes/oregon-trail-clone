# tests/unit/core/test_container.py
import pytest
from rich import inspect
from core.kernel.container import ServiceContainer
from core.kernel.contracts.provider import BaseServiceProvider

class MockProvider(BaseServiceProvider):
    def __init__(self, container: ServiceContainer):
        super().__init__(container)
        self.boot_called = False

    def bind(self):
        self.container.bind('mock_service', lambda c: 'This is a mock service')
    
    def boot(self):
        self.boot_called = True

    def provides(self):
        return ['mock_service']

class DependentMockProvider(BaseServiceProvider):
    def __init__(self, container: ServiceContainer):
        super().__init__(container)
        self.boot_called = False
        self.resolved_service = None

    def bind(self):
        # This service depends on 'mock_service' from the first provider
        self.container.bind('dependent_service', lambda c: f"Dependent on: {c.get('mock_service')}")
    
    def boot(self):
        self.boot_called = True
        # Resolution is safe in the boot phase
        self.resolved_service = self.container.get('mock_service')

    def provides(self):
        return ['dependent_service']

@pytest.fixture
def container():
    return ServiceContainer()

def test_service_registration(container):
    provider = MockProvider(container)

    for p in provider.provides():
        assert not container.has(p)
        container.bind(p, lambda c: f"Service for {p}")
        assert container.has(p)
    
    inspect(container._services)

def test_service_retrieval(container):
    provider = MockProvider(container)
    provider.bind()

    service = container.get('mock_service')
    assert service == 'This is a mock service'
    
    with pytest.raises(KeyError):
        container.get('non_existent_service')

def test_container_bootstrapping(container):
    """Verify the two-phase (bind -> Boot) lifecycle orchestration."""
    providers = [
        MockProvider(container),
        DependentMockProvider(container)
    ]

    # PHASE 1: Registration
    for p in providers:
        p.bind()
    
    assert container.has('mock_service')
    assert container.has('dependent_service')
    # Services should NOT be booted yet
    for p in providers:
        assert not p.boot_called

    # PHASE 2: Bootstrapping
    for p in providers:
        p.boot()
    
    # Verify boot sequence
    assert providers[0].boot_called
    assert providers[1].boot_called
    assert providers[1].resolved_service == 'This is a mock service'

    # Verify resolution of the dependent service
    assert container.get('dependent_service') == 'Dependent on: This is a mock service'
    
def __test_service_overwrite(container):
    container.bind('test_service', lambda c: 'First version')
    assert container.get('test_service') == 'First version'

    container.bind('test_service', lambda c: 'Second version')
    assert container.get('test_service') == 'Second version'
