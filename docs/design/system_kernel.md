# System Kernel Design (The Spec)

The Kernel is the "Laws of Physics" for the Oregon Trail ecosystem. It provides the contracts and mechanisms for dependency injection and system lifecycle.

## 1. Core Contracts
All domain entities must inherit from these contracts to be recognized by the Orchestrator.

**Path:** `src/core/contracts/domain/`

```mermaid
classDiagram
    class DomainEntity {
        <<abstract>>
    }
    class DomainRoot {
        +UUID uid
        +int BOOT_PRIORITY
        +list REQUIRED_PILLARS
        +string DOMAIN_SCOPE
    }
    class DomainRecord {
        <<Anemic>>
    }
    class DomainBlueprint {
        +string slug
    }
    class DomainValueObject {
        <<Immutable>>
    }

    DomainEntity <|-- DomainRoot
    DomainEntity <|-- DomainRecord
    DomainEntity <|-- DomainBlueprint
    DomainEntity <|-- DomainValueObject
```

## 2. Dependency Injection & Lifecycle
The `ServiceContainer` manages singletons and factory-based resolution.

**Path:** `src/core/container.py` and `src/core/contracts/provider.py`

```mermaid
sequenceDiagram
    participant G as Gateway (main.py)
    participant C as ServiceContainer
    participant P as ServiceProvider

    G->>C: Initialize()
    G->>P: Call register(container)
    P->>C: Bind factories/singletons
    Note over G,P: Phase 1: Registration Complete
    
    G->>P: Call boot(container)
    P->>C: Resolve dependencies
    P->>P: Initialize cross-service logic
    Note over G,P: Phase 2: Bootstrapping Complete
```

## 3. Pillar Isolation
The Kernel enforces boundaries between functional pillars.

| Pillar | Responsibility | Path |
| :--- | :--- | :--- |
| **Domain** | Pure Logic & State | `src/domain/` |
| **Engine** | Orchestration & Rules | `src/engine/` |
| **UI** | Presentation (View) | `src/ui/` |
| **Storage** | Persistence Adapters | `src/storage/` |
