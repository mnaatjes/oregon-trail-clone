# src/core/contracts/kernel.py

from enum import Enum, unique

@unique
class KernelSubsystem(Enum):
    """
    Core Kernel subsystems available for Automated Injection
    """
    REGISTRY = "registry"
    EVENTS = "events"
    STATE = "state"
    ASSETS = "assets"
    IDENTITY = "identity"