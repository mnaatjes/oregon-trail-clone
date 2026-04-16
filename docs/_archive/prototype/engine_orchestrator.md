---
title: "Prototype: Engine Orchestrator"
description: "Archived design document for the initial Engine Orchestrator prototype."
type: "explanation"
status: "depreciated"
created_at: "2026-04-16 04:00:00"
updated_at: "2026-04-16 04:00:00"
owner: "Michael Naatjes"
tags: [archived, design, legacy, prototype, engine]
version: "0.1.0"
---

# Prototype: Engine Orchestrator

The **Engine Orchestrator** is the central "Kernel" of the Oregon Trail engine. It is responsible for the execution flow of the game by coordinating between the `ServiceContainer` and various `Domain Modules` (Plugins).

## 1. Architectural Role: The Orchestrator

In the **Microkernel Architecture**, the Orchestrator sits in the core (src/engine/). It does not contain game-specific logic (like how health decays). Instead, it provides the **Ports** that allow game logic to be executed.

### Core Responsibilities:
- **Tick Management**: Drives the temporal progression of the game (Days, Turns).
- **Domain Coordination**: Iterates through registered domains and triggers their logic.
- **Entity Management**: Tracks which entities are active and passes them to the appropriate domain ports.

## 2. The Domain Port (`DomainBinding`)

The Orchestrator interacts with domains through a **Port** defined by the `DomainBinding` protocol. This ensures that the engine remains agnostic of the specific domains it is running.

```mermaid
graph TD
    subgraph "Engine Kernel"
        Orchestrator[Engine Orchestrator]
    end

    subgraph "Ports (Contracts)"
        Binding[DomainBinding Port]
    end

    subgraph "Domain Adapters"
        Health[Health Adapter]
        Wagon[Wagon Adapter]
        Weather[Weather Adapter]
    end

    Orchestrator -->|Calls| Binding
    Binding <|--| Health
    Binding <|--| Wagon
    Binding <|--| Weather
```

## 3. Prototype Implementation Concept

The Orchestrator uses the `ServiceContainer` to resolve domains that have registered themselves during the bootstrapping phase.

```python
from typing import List
from src.core.contracts.domain import DomainBinding, DomainEntity

class EngineOrchestrator:
    def __init__(self, container):
        self.container = container
        self.active_domains: List[DomainBinding] = []

    def bootstrap(self):
        """Resolves all registered domains from the container."""
        # The container provides a list of objects that satisfy DomainBinding
        self.active_domains = self.container.resolve_all(DomainBinding)

    def process_tick(self):
        """The main game loop iteration."""
        for domain in self.active_domains:
            # The Engine treats every domain polymorphically
            entities = self._get_entities_for_domain(domain)
            for entity in entities:
                domain.orchestrate(entity)

    def _get_entities_for_domain(self, domain: DomainBinding) -> List[DomainEntity]:
        """Filters the world state for entities relevant to this domain."""
        # Logic to match entities to the specific domain port
        pass
```

## 4. Interaction Sequence

1. **Initialization**: `main.py` creates the `ServiceContainer` and `Orchestrator`.
2. **Registration**: ServiceProviders register their domains (Health, Wagon) into the container.
3. **Bootstrapping**: The Orchestrator "opens its ports" by resolving all `DomainBinding` implementations from the container.
4. **Execution**: On every tick, the Orchestrator passes the relevant entities through the `orchestrate()` port of each domain.

## 5. Benefits of this Design

-   **Hot-Swappable Logic**: You can add a "Hunting" system by simply adding a new domain package; the Orchestrator doesn't need to be modified.
-   **Isolation**: If the "Weather" logic fails, the Orchestrator can catch the error and continue running the "Health" logic.
-   **Testability**: The Orchestrator can be tested using "Mock Adapters" that implement the `DomainBinding` protocol.
