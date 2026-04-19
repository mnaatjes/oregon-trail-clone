# tests/unit/core/contracts/test_domain_context.py

import pytest
from src.core.contracts.domain.context import DomainContext, DomainFamily
from src.core.contracts.kernel import KernelSubsystem

class MockService:
    """A dummy service for testing injection."""
    pass

def test_valid_leaf_init():
    """Verify a standard leaf can be initialized without a service."""
    context = DomainContext(
        family=DomainFamily.LEAF,
        intent="Weather Effects",
        priority=20,
        requirements=[KernelSubsystem.EVENTS]
    )
    assert context.family == DomainFamily.LEAF
    assert context.service is None

def test_valid_root_init():
    """Verify a root can be initialized with a service."""
    context = DomainContext(
        family=DomainFamily.ROOT,
        intent="Wagon Management",
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
        DomainContext(DomainFamily.LEAF, "Too Low", -1, [])
    
    # Test Over
    with pytest.raises(ValueError, match="priority' MUST be between 0 and 100"):
        DomainContext(DomainFamily.LEAF, "Too High", 101, [])

def test_intent_validation():
    """Verify that intent cannot be empty or whitespace."""
    with pytest.raises(ValueError, match="intent' CANNOT be empty"):
        DomainContext(DomainFamily.LEAF, "", 10, [])
    
    with pytest.raises(ValueError, match="intent' CANNOT be empty"):
        DomainContext(DomainFamily.LEAF, "   ", 10, [])

def test_root_requires_service():
    """Verify that a ROOT family MUST provide a service class."""
    with pytest.raises(ValueError, match="MUST provide a Service"):
        DomainContext(
            family=DomainFamily.ROOT,
            intent="Missing Service Root",
            priority=50,
            requirements=[]
            # service is None by default
        )

def test_immutability():
    """Verify that the DomainContext is frozen."""
    context = DomainContext(DomainFamily.LEAF, "Immutable", 10, [])
    with pytest.raises(Exception): # FrozenInstanceError
        context.priority = 20
