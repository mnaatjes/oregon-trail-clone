# src/core/kernel/contracts/discovery/manifest.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Generic, TypeVar

from src.core.kernel.contracts.discovery.unit import DiscoveryUnit
from src.core.kernel.contracts.discovery.status import DiscoveryStatus
from src.core.kernel.contracts.discovery.payload import DiscoveryPayload

# Declare TypeVars
T_Unit = TypeVar("T_Unit", bound=DiscoveryUnit)
T_Payload = TypeVar("T_Payload", bound=DiscoveryPayload)

@dataclass(frozen=True)
class DiscoveryManifest(Generic[T_Unit, T_Payload]):
    """
    The DiscoveryManifest is intended to contain one record representing a single unit
    - The Orchestrator will produce a List[DiscoveryManifest]
    - Granular Error Handling
    - 
    """
    unit: T_Unit                # Passive Filesystem Reference and Chain of Custody
    payload: T_Payload          # Hydrated Object; represents component as it exists in memory
    status: DiscoveryStatus     # Enum outcome of loading phase
    errors: List[Exception]     # Collection of any issues during the interrogation process
    metadata: Dict[str, Any]    # Container for transient data and metadata