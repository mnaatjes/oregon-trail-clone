---
title: "Domain Contracts Design (The Spec)"
description: "Archived design document detailing Domain Contracts, Taxonomy, and Anatomy."
type: "explanation"
status: "depreciated"
created_at: "2026-04-16 04:00:00"
updated_at: "2026-04-16 04:00:00"
owner: "Michael Naatjes"
tags: [archived, design, legacy, contracts]
version: "0.1.0"
---

# Domain Contracts Design (The Spec)

This document defines the core contracts and interfaces that govern the **Taxonomy** and **Anatomy** of the Oregon Trail domain layer, as established in **ADR 001 through 007**.

## 1. The Fundamental Unit: The Package (ADR 004)
The fundamental unit of the domain is the **Package**, not a base entity class. Each package (e.g., `health`, `character`) is a Sovereign Bounded Context defined by its **Anatomy** and **Taxonomic Signatures**.

### Taxonomic Signatures (ADR 006)
Every domain package must declare its "Species" and "Intent" within its `__init__.py` facade to be discoverable by the System Kernel.

| Signature | Role | Example |
| :--- | :--- | :--- |
| `__DOMAIN_SPECIES__` | Structural Validation | `"ROOT"` or `"LEAF"` |
| `__DOMAIN_INTENT__` | Screaming Intent | `"Manage Character Vitality"` |
| `__SERVICE_PROVIDER__` | Bootstrap Pointer | `"health.providers.HealthProvider"` |
| `__all__` | Encapsulation | List of exported Nouns and Verbs. |

---

## 2. Domain Taxonomy (The Species)
Taxonomy is enforced through inheritance from core contracts in `src/core/contracts/domain/`. There is no common "DomainEntity" base; classes inherit the specific behavior required by their role (ADR 002, 005).

```mermaid
classDiagram
    class DomainRoot {
        <<abstract>>
        +UUID uid (Sovereign)
        +BOOT_PRIORITY int
        +REQUIRED_PILLARS list
        +DOMAIN_SCOPE str
    }
    class DomainRecord {
        <<abstract>>
        +Identity None (Anonymous)
    }
    class DomainBlueprint {
        <<abstract>>
        +slug str (Static)
    }
    class DomainValueObject {
        <<abstract>>
        +Identity Value-based (Immutable)
    }

    note for DomainRoot "Species: ROOT (Aggregate Root)"
    note for DomainRecord "Species: LEAF (Passive State)"
    note for DomainBlueprint "Species: TEMPLATE (Global Truth)"
    note for DomainValueObject "Species: TYPE (Shared Kernel)"
```

### Contract Specifications (ADR 005)

| Contract | Identity | Scope | Responsibility |
| :--- | :--- | :--- | :--- |
| **DomainRoot** | UUID | Aggregate Root | The Sovereign "Actor". Anchors a Bounded Context. |
| **DomainRecord** | None | Leaf State | Anemic, anonymous state fragments (Atoms). |
| **DomainBlueprint** | Slug | Template | Static "Global Truth" loaded from JSON. |
| **DomainValueObject** | Value | Shared Kernel | Semantic types (Money, Coord) in `domain/common`. |

---

## 3. Infrastructure Contracts
These contracts define the lifecycle and discovery mechanisms used by the **System Kernel** (ADR 006, 007).

### A. BaseServiceProvider
Manages the two-phase (Register -> Boot) lifecycle of a domain package.

**Path:** `src/core/contracts/provider.py`

```mermaid
sequenceDiagram
    participant Kernel as System Kernel
    participant Provider as BaseServiceProvider
    participant Container as ServiceContainer

    Kernel->>Provider: 1. register(container)
    Provider->>Container: Bind factories (Lazy)
    
    Kernel->>Provider: 2. boot(container)
    Provider->>Container: Resolve & Initialize (Active)
```

### B. BaseRegistry
The exclusive provider of **DomainBlueprints**.

**Path:** `src/core/contracts/domain/registry.py`

```mermaid
flowchart LR
    Assets[(Assets: JSON)] -->|Hydrate| Registry[BaseRegistry]
    Registry -->|Provides| Blueprint[DomainBlueprint]
    Service[Domain Service] -->|Requests| Registry
```

---

## 4. Interaction via Duck Typing (ADR 002, 003)
Lateral interaction between Roots is strictly decoupled. Roots define their requirements via **Structural Protocols** rather than importing siblings.

```python
# Defined at the top of services.py in the consuming Root
class Payer(Protocol):
    balance: int
    def deduct(self, amount: int) -> bool: ...
```

```mermaid
graph LR
    subgraph Root_Shop [Domain: Shop]
        ShopService --> PayerProtocol[Protocol: Payer]
    end
    
    subgraph Root_Character [Domain: Character]
        CharacterRoot
    end
    
    CharacterRoot -- "Satisfies Shape" --> PayerProtocol
    Engine[Engine Orchestrator] -->|Mediates| CharacterRoot
    Engine -->|To| ShopService
```
