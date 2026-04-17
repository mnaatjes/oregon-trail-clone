---
title: "TDD: Identity Registry Service"
description: "Technical design for the core Identity Registry responsible for UUID generation, collision detection, and global actor tracking."
type: "design"
status: "draft"
created_at: "2026-04-16 12:30:00"
updated_at: "2026-04-16 12:30:00"
owner: "Michael Naatjes"
tags: ["design", "core", "identity", "registry", "uuid"]
version: "0.1.0"
---

# TDD: Identity Registry Service

## Overview
The `IdentityRegistry` is a core infrastructure service that acts as the sovereign authority for actor identity in the Oregon Trail engine. It centralizes UUID generation and maintains a runtime map of all active `DomainRoot` identities to ensure system-wide integrity.

## Goals
- **Single Source of Truth:** Centralize UUID generation to avoid scattered calls to `uuid.uuid4()`.
- **Collision Guard:** Prevent duplicate UUIDs (even the statistically improbable ones) and "zombie" identity re-use.
- **Global Discovery:** Allow the Orchestrator and other services to verify the existence of an actor by UID without polling every domain.
- **Hydration Security:** Validate IDs during save-game loading to ensure snapshot integrity.

## Proposed Design

### 1. The Service Contract
The service will be registered in the `ServiceContainer` as `identity`.

```python
# src/core/contracts/identity.py
from abc import ABC, abstractmethod
from uuid import UUID

class IIdentityRegistry(ABC):
    @abstractmethod
    def generate_sovereign_id(self) -> UUID:
        """Generates a new, unregistered UUID."""
        pass

    @abstractmethod
    def register_id(self, uid: UUID, owner_info: str) -> None:
        """
        Manually registers an existing ID (used during hydration).
        Raises IdentityCollisionError if already registered.
        """
        pass

    @abstractmethod
    def is_registered(self, uid: UUID) -> bool:
        """Checks if a UID is currently active in the ecosystem."""
        pass

    @abstractmethod
    def release_id(self, uid: UUID) -> None:
        """Removes an ID from the registry (on actor death/deletion)."""
        pass
```

### 2. Internal Implementation
The registry maintains a mapping of `UUID -> owner_metadata`.

```python
# src/core/identity.py
import uuid
from typing import Dict

class IdentityRegistry(IIdentityRegistry):
    def __init__(self):
        self._active_ids: Dict[uuid.UUID, str] = {}

    def generate_sovereign_id(self) -> uuid.UUID:
        new_id = uuid.uuid4()
        while new_id in self._active_ids:
            new_id = uuid.uuid4() # Statistically impossible, but architecturally safe
        return new_id

    def register_id(self, uid: uuid.UUID, owner_info: str):
        if uid in self._active_ids:
            raise IdentityCollisionError(f"Collision detected for {uid} (Owned by {self._active_ids[uid]})")
        self._active_ids[uid] = owner_info
```

### 3. Integration with Domain Services
Domain services (the "Generals") use the registry to arm their Aggregate Roots with identity.

```python
# src/domain/roots/character/services.py
def create_character(self, ...):
    uid = self.identity_service.generate_sovereign_id()
    root = CharacterRoot(uid=uid, ...)
    self.identity_service.register_id(uid, "domain.roots.character")
    return root
```

## State Registry Symbiosis
The `IdentityRegistry` serves as the index for the `StateRegistry`. When the `StateRegistry` performs a world snapshot, it iterates over the identities verified by the `IdentityRegistry`.

```mermaid
graph LR
    DS[Domain Service] -->|1. Request ID| IR[Identity Registry]
    IR -->|2. Generate & Log| IR
    IR --|3. Return UUID| DS
    DS -->|4. Instantiate| DR[Domain Root]
    DR -->|5. Auto-Register| SR[State Registry]
    SR -.->|6. Verify Identity| IR
```

## Cross-Cutting Concerns
- **Performance:** Lookup is O(1) via Hash Map.
- **Persistence:** The registry is rebuilt during the hydration flow of a save game. If a collision is found in the save data, the load fails immediately.

## References
- [ADR 003: Anemic Aggregator Domains](../reports/adr/003_anemic_aggregator_domains.md)
- [ADR 007: Domain Ecosystem](../reports/adr/007_domain_ecosystem.md)
