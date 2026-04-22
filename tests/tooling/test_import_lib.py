# tests/tooling/test_import_lib.py

import pytest
from types import ModuleType
from rich import inspect
from rich import print as rprint
from importlib import util
from importlib.machinery import ModuleSpec
from pathlib import Path
from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Any, Type, TypeVar

from core.domain.contracts.spore import DomainSpore
from core.domain.contracts.blueprints.root import RootBlueprint
from core.domain.contracts.blueprints.display import DisplayBlueprint
from core.domain.contracts.taxonomy import DomainFamily
from core.domain.contracts.root import DomainRoot
from core.domain.entities.package import Package
from core.kernel.contracts.discovery import DiscoveryUnit
from engine.domain.scanner import DomainScanner

class MockSpore(DomainSpore):
    species = "test-species"  # type:ignore

@pytest.fixture
def display_blueprints():
    """Fixture that creates multiple, valid DisplayBlueprints."""
    return [
        DisplayBlueprint(asset_id="asset_wagon", label="Wagon", description="A sturdy wooden wagon."),
        DisplayBlueprint(asset_id="asset_shop", label="General Store", description="Supplies for the trail."),
        DisplayBlueprint(asset_id="asset_ox", label="Ox", description="A strong beast of burden."),
    ]

@pytest.fixture
def domain_roots(display_blueprints):
    """
    Fixture that creates multiple, valid DomainRoot implementations
    from a list of single-word package-names.
    """
    package_names = ["wagon", "shop", "ox", "character", "health"]
    roots = []

    # Define a mock root class that matches the contract
    @dataclass(frozen=True)
    class MockDomainRoot(DomainRoot):
        def clone(self) -> "MockDomainRoot":
            from dataclasses import replace
            return replace(self, records={k: v.clone() for k, v in self.records.items()})

    for i, name in enumerate(package_names):
        display = display_blueprints[i % len(display_blueprints)]
        
        # Create a unique Blueprint class for each species to satisfy DomainContext
        blueprint_cls = type(f"{name.capitalize()}Blueprint", (RootBlueprint,), {
            "species": name,
            "breed": f"{name}_standard",
            "display": display
        })
        # Wrap in dataclass to satisfy RootBlueprint/BaseBlueprint structure
        blueprint_cls = dataclass(frozen=True)(blueprint_cls)
        
        roots.append(MockDomainRoot(
            uid=uuid4(), 
            blueprint=blueprint_cls(breed=f"{name}_standard", display=display)
        ))
        
    return roots

@pytest.fixture
def domain_init_configs(domain_roots):
    """
    Generates a map of package names to their __init__.py content strings,
    derived from the domain_roots fixture data. Includes mock models,
    services, and the mandatory __all__ export as per ADR-016.
    """
    configs = {}
    for root in domain_roots:
        species = root.blueprint.species
        name_cap = species.capitalize()
        
        content = (
            "from dataclasses import dataclass\n"
            "from core.domain.contracts.context import DomainContext\n"
            "from core.domain.contracts.blueprints.root import RootBlueprint\n"
            "from core.domain.contracts.root import DomainRoot\n"
            "from core.domain.contracts.service import BaseDomainService\n\n"
            "# Mock Model\n"
            f"@dataclass(frozen=True)\n"
            f"class {name_cap}Root(DomainRoot):\n"
            "    def clone(self): return self\n\n"
            "# Mock Blueprint\n"
            f"@dataclass(frozen=True)\n"
            f"class {name_cap}Blueprint(RootBlueprint):\n"
            f"    species = '{species}'\n"
            f"    breed = '{root.blueprint.breed}'\n"
            f"    display = None\n\n"
            "# Mock Service\n"
            f"class {name_cap}Service(BaseDomainService):\n"
            "    pass\n\n"
            f"__CONTEXT__ = DomainContext(\n"
            f"    intent={name_cap}Blueprint,\n"
            f"    priority=10,\n"
            f"    service={name_cap}Service\n"
            f")\n\n"
            f"__all__ = [\n"
            f"    '__CONTEXT__',\n"
            f"    '{name_cap}Root',\n"
            f"    '{name_cap}Service',\n"
            f"    '{name_cap}Blueprint'\n"
            f"]\n"
        )
        configs[species] = content
    return configs

def load_module(path:Path):
    # Create unique name for module to avoid collisions
    id = uuid4()
    module_name = f"{path.parts[-2]}"
    spec = util.spec_from_file_location("", path)
    module = util.module_from_spec(spec)# type: ignore
    spec.loader.exec_module(module) # type: ignore

    return module
"""
Glossary
    - Package: the entire Domain (all its logic, assets, and data
    - Facade: the "Shipping Label" (__CONTEXT__) that tells the Engine: 
    "I am a high-priority domain that handles gold mining."
    - Contructor: __init__.py file
    - Values: data variables like __CONTEXT__
"""

def test_run(tmp_path, domain_init_configs):
    key = "domain"
    packages = ["wagon", "shop", "ox", "character", "health"]
    scanner = DomainScanner(key)
    for p in packages:
        target_path = tmp_path / key / "roots" / p  # Using 'roots' as per architecture
        content = domain_init_configs[p]
        target_path.mkdir(parents=True, exist_ok=True)
        # Write
        module_path = target_path / "__init__.py"
        module_path.write_text(content)

    results = scanner.scan(tmp_path / key)
    assert len(results) == len(packages)

    for r in results:
        package = scanner.load_facade(r)
        
        # Verify Context
        assert package.facade.context is not None #type:ignore
        assert package.facade.context.priority == 10 # type:ignore
        
        # Verify Exports (__all__)
        assert package.exports is not None
        assert len(package.exports) == 4
        assert "__CONTEXT__" in package.exports
        
        # Verify specific exports based on package name
        name_cap = package.package_name.capitalize()
        assert f"{name_cap}Service" in package.exports
        assert f"{name_cap}Root" in package.exports
        assert f"{name_cap}Blueprint" in package.exports

        rprint(f"[green]Verified {package.package_name}: {package.exports}[/green]")
        # inspect(package.facade.context) #type:ignore


