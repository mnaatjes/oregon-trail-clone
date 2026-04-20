# tests/tooling/test_import_lib.py

import pytest
from rich import inspect
from rich import print as rprint
from importlib import util
from pathlib import Path
from uuid import UUID, uuid4

from core.domain.contracts.spore import DomainSpore
from core.domain.contracts.taxonomy import DomainFamily

class MockSpore(DomainSpore):
    @property
    def family(self):
        return DomainFamily.SPORE
    @property
    def species(self) -> str:
        return "test-species"

def load_module(path:Path):
    # Create unique name for module to avoid collisions
    id = uuid4()
    module_name = f"{path.parts[-2]}"
    print(module_name)
    spec = util.spec_from_file_location(module_name, path)
    module = util.module_from_spec(spec)# type: ignore
    spec.loader.exec_module(module) # type: ignore
    #inspect(module_name)
    inspect(spec)

def test_run_load_module(tmp_path):
    """"""
    # Find Domain
    dir_domain = tmp_path / "domain"
    dir_root = dir_domain / "root"
    dir_package = dir_root / "test_package"
    dir_package.mkdir(parents=True, exist_ok=True)
    target_path = dir_package / "__init__.py"

    target_path.write_text(
        "from core.domain.contracts.context import DomainContext\n"
        "from tests.tooling.test_import_lib import MockSpore\n"
        "__CONTEXT__ = DomainContext(intent=MockSpore,priority=1)"
    )

    load_module(target_path)