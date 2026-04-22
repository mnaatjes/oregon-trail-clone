import pytest
from pathlib import Path
from dataclasses import dataclass
from core.kernel.contracts.discovery.unit import DiscoveryUnit

@dataclass(frozen=True)
class MockDiscoveryUnit(DiscoveryUnit):
    pass

def test_discovery_unit_derives_properties():
    # Setup: a path that contains the key 'src'
    # /root/project/src/domain/wagon/__init__.py
    key = "src"
    path = Path("/root/project/src/domain/wagon/__init__.py")
    
    unit = MockDiscoveryUnit(key=key, path=path)
    
    # Anchor should be the parent of the folder named 'src'
    # path.parents: [wagon, domain, src, project, root, /]
    # next p where p.name == 'src' is 'src'
    # parent of 'src' is '/root/project'
    assert unit.anchor == Path("/root/project")
    
    # Relative path should be from anchor
    assert unit.rel_path == Path("src/domain/wagon/__init__.py")

def test_discovery_unit_raises_error_if_key_not_in_path():
    key = "missing"
    path = Path("/root/project/src/domain/wagon/__init__.py")
    
    with pytest.raises(ValueError, match="Key missing NOT FOUND"):
        MockDiscoveryUnit(key=key, path=path)

def test_discovery_unit_identity_is_unique():
    key = "src"
    path = Path("/root/project/src/domain/wagon/__init__.py")
    
    unit1 = MockDiscoveryUnit(key=key, path=path)
    unit2 = MockDiscoveryUnit(key=key, path=path)
    
    assert unit1.id != unit2.id
