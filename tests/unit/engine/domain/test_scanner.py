import pytest
from pathlib import Path
from engine.domain.scanner import DomainScanner
from core.domain.contracts.context import DomainContext

def create_mock_domain(path: Path, species: str, include_context=True, include_all=True):
    path.mkdir(parents=True, exist_ok=True)
    init_content = [
        "from dataclasses import dataclass",
        "from core.domain.contracts.context import DomainContext",
        "from core.domain.contracts.blueprints.root import RootBlueprint",
        "@dataclass(frozen=True)",
        f"class {species.capitalize()}Blueprint(RootBlueprint):",
        f"    species = '{species}'",
        f"    breed = 'standard'",
        f"    display = None",
        ""
    ]
    
    if include_context:
        init_content.extend([
            f"__CONTEXT__ = DomainContext(",
            f"    intent={species.capitalize()}Blueprint,",
            f"    priority=10,",
            f"    service=object",
            f")",
            ""
        ])
    
    if include_all:
        init_content.extend([
            f"__all__ = ['__CONTEXT__']"
        ])
        
    (path / "__init__.py").write_text("\n".join(init_content))

def test_domain_scanner_scan(tmp_path):
    # Setup
    key = "domain"
    domain_path = tmp_path / key
    create_mock_domain(domain_path / "roots" / "wagon", "wagon")
    create_mock_domain(domain_path / "leaves" / "health", "health")
    
    scanner = DomainScanner(key)
    results = scanner.scan(domain_path)
    
    assert len(results) == 2
    names = [r.package_name for r in results]
    assert "wagon" in names
    assert "health" in names

def test_domain_scanner_load_facade(tmp_path):
    # Setup
    key = "domain"
    domain_path = tmp_path / key
    wagon_path = domain_path / "roots" / "wagon"
    create_mock_domain(wagon_path, "wagon")
    
    scanner = DomainScanner(key)
    package = scanner.scan(domain_path)[0]
    
    # Load
    hydrated_package = scanner.load_facade(package)
    
    assert hydrated_package.facade is not None
    assert hydrated_package.facade.context.priority == 10
    assert hydrated_package.exports == ["__CONTEXT__"]

def test_domain_scanner_load_facade_missing_context(tmp_path):
    # Setup
    key = "domain"
    domain_path = tmp_path / key
    wagon_path = domain_path / "roots" / "wagon"
    create_mock_domain(wagon_path, "wagon", include_context=False)
    
    scanner = DomainScanner(key)
    package = scanner.scan(domain_path)[0]
    
    with pytest.raises(AttributeError, match="missing valid __CONTEXT__"):
        scanner.load_facade(package)
