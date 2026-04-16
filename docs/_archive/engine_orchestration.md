---
title: "Engine Orchestration Design (The Controller)"
description: "Archived design document detailing the Engine Orchestrator, Event Bus, and System Tick."
type: "explanation"
status: "depreciated"
created_at: "2026-04-16 04:00:00"
updated_at: "2026-04-16 04:00:00"
owner: "Michael Naatjes"
tags: [archived, design, legacy, engine]
version: "0.1.0"
---

# Engine Orchestration Design (The Controller)

The Engine is the "Conductor" of the Oregon Trail ecosystem. It manages the lifecycle, movement, and interaction of domain packages while enforcing architectural boundaries (ADR 001, 006, 007).

## 1. The Domain Orchestrator (The Conductor)
The Orchestrator is the active component within the System Kernel that oversees the "Movement and Sequence" of the game world.

**Path:** `src/engine/orchestrator.py`

```mermaid
flowchart TD
    Scan[1. Directory Scan] --> Taxonomy[2. Vet Taxonomy Signatures]
    Taxonomy --> Ontology[3. Resolve Ontological Metadata]
    Ontology --> Sort[4. Sort by BOOT_PRIORITY]
    Sort --> Bootstrap[5. Two-Phase Bootstrap]
    Bootstrap --> Heartbeat[6. Start System Tick]
```

### Responsibilities
1. **Awareness:** Scans the `domain/` directory for `__DOMAIN_SPECIES__`.
2. **Registration:** Invokes `register()` on all `__SERVICE_PROVIDER__` classes.
3. **Sequencing:** Boots providers in order of their `BOOT_PRIORITY`.
4. **Mediation:** Facilitates Root-to-Root interaction via Structural Protocols.

---

## 2. The Nervous System (Event Bus)
The Event Bus allows decoupled interaction between sovereign domains. Siblings react to the "Environment" rather than calling each other directly (ADR 007).

**Path:** `src/core/events.py`

```mermaid
sequenceDiagram
    participant Weather as Leaf: Weather
    participant Character as Root: Character
    participant Bus as Event Bus
    participant Orchestrator as Engine Orchestrator

    Orchestrator->>Bus: Emit: TickDay
    Bus->>Weather: Notify: TickDay
    Weather->>Weather: Calculate Blizzard
    Weather->>Bus: Emit: BlizzardStarted (Public)
    Note over Weather: Rule: Only Roots emit Public Events.
    Bus->>Character: Notify: BlizzardStarted
    Character->>Character: Apply Health Penalty
```

### Event Ownership Rules
- **Sovereignty:** Only a **Root Service** is allowed to broadcast a Public Event.
- **Silence:** Leaves must report changes to their parent Root; they remain silent to the outside world.

---

## 3. World State (State Registry)
The State Registry collects snapshots of every active `DomainRoot` for total serializability and "Save Game" functionality (ADR 003, 007).

**Path:** `src/engine/registry.py`

```mermaid
graph TD
    subgraph Ecosystem [Live Domain Ecosystem]
        C1[Character: Jedediah]
        C2[Character: Ezekiel]
        W1[Wagon: The Bessie]
    end

    subgraph Kernel [System Kernel]
        Registry[State Registry]
        Registry -->|Collects Anemic DTOs| C1
        Registry -->|Collects Anemic DTOs| C2
        Registry -->|Collects Anemic DTOs| W1
    end

    Registry -- "Single JSON Snapshot" --> JSON[(SaveGame.json)]
```

---

## 4. The Heartbeat (System Tick)
The Ecosystem relies on the progression of time. The Orchestrator emits a **Broadcast Event** to trigger "Metabolic" needs across all Roots.

```mermaid
flowchart LR
    Tick[Orchestrator Tick] -->|Broadcast| Bus[Event Bus]
    Bus -->|Notify| Root1[Root: Health]
    Bus -->|Notify| Root2[Root: Wagon]
    Bus -->|Notify| Root3[Root: Environment]
```
- **Tick Priority:** Ties back to `BOOT_PRIORITY`. Ensures "Weather" is calculated before "Health" is penalized.
