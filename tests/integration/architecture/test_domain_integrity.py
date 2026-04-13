# tests/integration/architecture/test_domain_integrity.py
import pytest
import os
from rich import inspect, print

DOMAIN_PATH = "src/domain"
PROVIDER_PATH = "src/engine/providers"
DOMAIN_NAMES = ["character", "health"]
DOMAIN_COMPONENTS = ["registry", "services", "models"]
DOMAINS = [d for d in os.listdir(DOMAIN_PATH) if os.path.isdir(os.path.join(DOMAIN_PATH, d))]

@pytest.mark.parametrize("domain_name", DOMAIN_NAMES)
def test_domain_dir_exists(domain_name):
    # Check if the domain exists in the DOMAINS list
    if domain_name not in DOMAINS:
        pytest.fail(f"Domain '{domain_name}' does not exist in {DOMAIN_PATH}")
    domain_dir = os.path.join(DOMAIN_PATH, domain_name)
    # Capture with pytest.raises
    try:
        assert os.path.isdir(domain_dir), f"Domain directory '{domain_dir}' does not exist."
    except AssertionError as e:
        pytest.fail(str(e))

@pytest.mark.parametrize("domain_name", DOMAIN_NAMES)
def test_provider_class_exists(domain_name):
    provider_file = os.path.join(PROVIDER_PATH, f"{domain_name}_provider.py")
    # Capture with pytest.raises
    try:
        assert os.path.isfile(provider_file), f"Provider file '{provider_file}' does not exist for domain '{domain_name}'."
        module_name = f"engine.providers.{domain_name}_provider"
        provider_module = __import__(module_name, fromlist=[''])
        provider_class_name = f"{domain_name.capitalize()}Provider"
        assert hasattr(provider_module, provider_class_name), f"Provider class '{provider_class_name}' does not exist in '{provider_file}'."
    except AssertionError as e:
        pytest.fail(str(e))

@pytest.mark.parametrize("domain_name", DOMAIN_NAMES)
def test_domain_components_exist(domain_name):
    domain_dir = os.path.join(DOMAIN_PATH, domain_name)
    for component in DOMAIN_COMPONENTS:
        component_file = os.path.join(domain_dir, f"{component}.py")
        # Capture with pytest.raises
        try:
            assert os.path.isfile(component_file), f"Component file '{component_file}' does not exist in domain '{domain_name}'."
        except AssertionError as e:
            pytest.fail(str(e))