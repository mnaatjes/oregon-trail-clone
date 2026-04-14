# tests/integration/architecture/conftest.py

import pytest
import os
from .constants import (
    EXPECTED_DOMAIN_PACKAGES, 
    DOMAIN_PATH, 
    REQUIRED_DOMAIN_COMPONENTS,
    PROVIDER_PATH,
    PROVIDER_SUFFIX
)
from .helpers import get_all_domains

@pytest.fixture(scope='session')
def domain_inventory():
    return get_all_domains()

@pytest.fixture(params=get_all_domains())
def domain_name(request):
    return request.param

@pytest.fixture
def domain_path(domain_name):
    return f"{DOMAIN_PATH}/{domain_name}"

@pytest.fixture
def domain_contents(domain_path):
    items = os.listdir(domain_path)
    return [os.path.splitext(i)[0] for i in items]

@pytest.fixture()
def providers(domain_name):
    if not os.path.exists(PROVIDER_PATH):
        return []
    
    return [i.replace(f"_{PROVIDER_SUFFIX.lower()}.py", "") for i in os.listdir(PROVIDER_PATH)]
