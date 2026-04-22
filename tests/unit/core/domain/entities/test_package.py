import pytest
from pathlib import Path
from core.domain.entities.package import Package

def test_package_derives_metadata():
    # Setup
    key = "domain"
    path = Path("/home/user/project/src/domain/roots/wagon/__init__.py")
    
    package = Package(key=key, path=path)
    
    # module_name should be 'domain.roots.wagon'
    assert package.module_name == "domain.roots.wagon"
    
    # package_name should be 'wagon'
    assert package.package_name == "wagon"

def test_package_derives_metadata_without_init():
    # Setup
    key = "domain"
    path = Path("/home/user/project/src/domain/roots/wagon")
    
    package = Package(key=key, path=path)
    
    assert package.module_name == "domain.roots.wagon"
    assert package.package_name == "wagon"

def test_package_defaults():
    key = "domain"
    path = Path("/home/user/project/src/domain/roots/wagon")
    
    package = Package(key=key, path=path)
    
    assert package.facade is None
    assert package.exports == []
