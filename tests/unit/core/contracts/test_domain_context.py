# tests/unit/core/contracts/test_domain_context.py

import pytest
from core.kernel.contracts.domain.context import DomainContext, DomainFamily
from core.kernel.contracts.kernel import KernelSubsystem
from core.kernel.contracts.domain.service import BaseDomainService

from core.kernel.contracts.domain.blueprints.root import RootBlueprint

class MockService(BaseDomainService):
    """A dummy service for testing injection."""
    @property
    def species(self):
        return ""
    
    @property
    def family(self):
        return DomainFamily.ROOT

def test_valid_leaf_init():
    """Verify a standard leaf can be initialized without a service."""
    context = DomainContext(
        intent=RootBlueprint,
        priority=20,
        requirements=[KernelSubsystem.EVENTS]
    )
    assert context.family == DomainFamily.LEAF
    assert context.service is None

def test_valid_root_init():
    """Verify a root can be initialized with a service."""
    context = DomainContext(
        intent=RootBlueprint,
        priority=40,
        requirements=[KernelSubsystem.EVENTS, KernelSubsystem.STATE],
        service=MockService
    )
    assert context.family == DomainFamily.ROOT
    assert context.service == MockService

def test_priority_bounds():
    """Verify that priority must be between 0 and 100."""
    # Test Under
    with pytest.raises(ValueError, match="priority' MUST be between 0 and 100"):
        DomainContext(intent=RootBlueprint, priority=1)
    
    # Test Over
    with pytest.raises(ValueError, match="priority' MUST be between 0 and 100"):
        DomainContext(intent=RootBlueprint, priority=1)

def test_intent_validation():
    """Verify that intent cannot be empty or whitespace."""
    with pytest.raises(ValueError, match="intent' CANNOT be empty"):
        DomainContext(intent=RootBlueprint, priority=1)
    
    with pytest.raises(ValueError, match="intent' CANNOT be empty"):
        DomainContext(intent=RootBlueprint, priority=1)

def test_root_requires_service():
    """Verify that a ROOT family MUST provide a service class."""
    with pytest.raises(ValueError, match="MUST provide a Service"):
        DomainContext(
            intent="Missing Service Root", #type:ignore
            priority=50,
            requirements=[]
            # service is None by default
        )

def test_immutability():
    """Verify that the DomainContext is frozen."""
    context = DomainContext(intent=RootBlueprint, priority=1)
    with pytest.raises(Exception): # FrozenInstanceError
        context.priority = 20 #type: ignore
