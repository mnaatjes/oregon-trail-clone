# src/core/kernel/contracts/discovery.py

from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DiscoveryUnit(ABC):
    """
    The Abstract Contract for any item discovered on the filesystem.
    Forces all discovered items to have a Key, a Path, and an Identity
    """
    key: str
    path: Path
    id: UUID = field(default_factory=uuid4)

    # Derived Properties
    anchor: Path = field(init=False)
    rel_path: Path = field(init=False)

    def __post_init__(self):
        """
        The 'Universal Physics' of discovery.
        This logic runs for Domains, Assets, and Configs alike.
        """
        # Validate key in path
        if not self.key in str(self.path):
            raise ValueError(
                f"[SCANNING VIOLATION] in '{self.__class__.__name__}' "
                f"Key {self.key} NOT FOUND in {str(self.path)}"
            )
        # Derive Anchor
        _anchor = Path(next(p for p in self.path.parents if p.name == self.key).parent)

        # Derive Relative Path
        _rel = self.path.relative_to(_anchor)

        # Set Properties
        object.__setattr__(self, "anchor", _anchor)
        object.__setattr__(self, "rel_path", _rel)