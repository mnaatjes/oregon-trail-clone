# src/engine/domain/scanner.py
from types import ModuleType
from importlib import util
from importlib.machinery import ModuleSpec
from typing import List
from pathlib import Path
from rich import inspect
from dataclasses import replace

from core.kernel.contracts.scanner import BaseScanner
from core.domain.entities.package import Package
from core.domain.entities.facade import Facade
from core.domain.contracts.context import DomainContext

class DomainScanner(BaseScanner[Package]):
    
    def __init__(self, key: str) -> None:
        self.key = key

    def scan(self, scan_path: str|Path) -> List[Package]:
        """
        Active discovery: Crawls the filesystem for __init__.py files
        and converts them into passive Package entities.
        """
        # Init container
        packages: List[Package] = []

        # Type scan_path
        if not isinstance(scan_path, Path):
            scan_path = Path(scan_path)

        # Recursive Glob
        for init_file_path in scan_path.rglob("__init__.py"):
            # Filter: make sure path contains key
            if self.key in init_file_path.parts:
                package = Package(
                    key=self.key,
                    path=init_file_path
                )
                packages.append(package)

        return packages
    
    def load_facade(self, package:Package) -> Package:
        """Use importlib to populate the Facade."""
        # Create Blueprint (Specification)
        spec = util.spec_from_file_location(
            name=package.module_name,
            location=package.path
        )
        
        # Validate Spec
        if spec is None or spec.loader is None:
            raise ImportError("")
        
        # Load
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Architectural Guard
        # Every package MUST have a DomainContext
        _context = getattr(module, "__CONTEXT__", None)
        if not isinstance(_context, DomainContext):
            raise AttributeError(
                f"[PACKAGE VIOLATION] in '{package.module_name}' "
                f"Domain package '{package.package_name}' is missing valid __CONTEXT__ attribute "
                f"See file {str(package.path)}"
            )

        # Architectural Guard
        # Capture __all__ values
        _exports = getattr(module, "__all__", [])
        object.__setattr__(package, "exports", _exports)

        # Hydrate Facade
        facade = Facade(
            name=package.module_name,
            spec=spec,
            module=module,
            file=str(package.path),
            context=_context
        )

        return replace(package, facade=facade)