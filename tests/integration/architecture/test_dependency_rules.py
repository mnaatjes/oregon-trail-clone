# tests/integration/architecture/test_dependency_rules.py
import pytest
from rich import inspect
from .constants import (
    EXPECTED_DOMAIN_PACKAGES, 
    DOMAIN_PATH, 
    REQUIRED_DOMAIN_COMPONENTS,
    PROVIDER_PATH,
    PROVIDER_SUFFIX
)
from .conftest import domain_inventory
from .helpers import format_architecture_violation

# Test Conftest and Helpers
def test_helpers(domain_inventory):
    assert type(domain_inventory) is list

def test_domain_inventory_matches_expected(domain_inventory):
    has_all = all(item in domain_inventory for item in EXPECTED_DOMAIN_PACKAGES)
    
    if has_all is False:
        diff_expected = set(EXPECTED_DOMAIN_PACKAGES) - set(domain_inventory)
        
        pytest.fail(f"[MISSING DOMAINS] Expected Domain is missing: {", ".join([DOMAIN_PATH + "/" + d for d in diff_expected])}", pytrace=False)

def test_has_required_components(domain_name, domain_path, domain_contents):
    # Build Msg
    msg = [
        f"\n--- {domain_name.upper()} ---",
        f"Path: {domain_path}",
        f"Contents: {", ".join(domain_contents)}"
    ]

    # Check for missing required domain components
    has_required_components = all(item in domain_contents for item in REQUIRED_DOMAIN_COMPONENTS)
    if has_required_components is False:
        missing = set(REQUIRED_DOMAIN_COMPONENTS) - set(domain_contents)
        msg.append(f"Missing: {", ".join(missing)}")
        pytest.fail(f"\n".join(msg), False)
    print(f"\n".join(msg))

def test_has_service_provider(domain_name, providers):
    # Check providers empty
    if not providers:
        pytest.fail(f"No Service Providers Found!!!", False)
    
    # Check if domain_name in providers
    if domain_name not in providers:
        pytest.fail(f"[MISSING Provider] {domain_name} in {PROVIDER_PATH}", False)