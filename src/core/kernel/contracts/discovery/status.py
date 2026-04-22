# src/core/kernel/contracts/discovery/status.py

from enum import Enum

class DiscoveryStatus(Enum):
    VALID = "valid"
    MALFORMED = "malformed"
    IGNORED = "ignored"
