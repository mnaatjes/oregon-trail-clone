# src/core/domain/entities/package.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from core.kernel.contracts.discovery.unit import DiscoveryUnit
from core.domain.entities.facade import Facade

@dataclass(frozen=True)
class Package(DiscoveryUnit):
    """A discovery unit specifically for Python Packages."""
    # properties for post-init
    module_name: str = field(init=False)    # import notation
    package_name: str = field(init=False)   # single_word for DX
    facade: Optional[Facade] = None         # importlib.util content
    exports: List[str] = field(default_factory=list) # captures __all__

    def __post_init__(self):
        """Calculates all derived metadata once during instantiation."""

        # Derive Module Name
        fp = self.path.with_suffix("")
        index = list(fp.parts).index(self.key)
        parts = list(fp.parts)[index:]
        
        # Pop unwanted values
        if parts[-1] == "__init__":
            parts.pop()
        _module_name = ".".join(parts)

        # Derive Package Name
        _package_name = _module_name.split(".")[-1]

        # Set Properties
        object.__setattr__(self, "module_name", _module_name)
        object.__setattr__(self, "package_name", _package_name)