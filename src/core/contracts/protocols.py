# src/core/contracts/protocols.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class Bootable(Protocol):
    """
    Core Kernel subsystems available for Automated Injection
    A structural contract for services that require a
    'Hydration' phase after registration but before execution.
    """
    def boot(self) -> None:
        """Performs initialization logic dependent on other services."""
        ...