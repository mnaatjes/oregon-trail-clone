# Domain Layer Design (The Model)

The Domain layer is the "Screaming" heart of the game, organized into Sovereign Bounded Contexts.

## 1. Package Anatomy
Each domain package (e.g., `health`, `character`) follows a strict internal structure to maintain **Anemic Symbiosis**.

**Path:** `src/domain/<package_name>/`

```mermaid
graph TD
    subgraph Package_Boundary [Sovereign Bounded Context]
        Facade[__init__.py Facade]
        Models[models.py Anemic State]
        Logic[logic.py Pure Math]
        Service[services.py Orchestration]
        
        Facade --> Service
        Service --> Models
        Service --> Logic
    end
    
    External_Engine --> Facade
```

| Component | Responsibility | Rule |
| :--- | :--- | :--- |
| **Model** | Holds data only. | Anemic DTO. No logic. |
| **Logic** | Transforms data. | Pure, stateless functions. |
| **Service** | Coordinates flow. | Singleton. Feeds Model to Logic. |
| **Facade** | The "Voice". | Flattened API for external use. |

## 2. Taxonomy (Roots vs. Leaves)
The filesystem hierarchy distinguishes between atoms and assemblies.

| Type | Directory | Rule |
| :--- | :--- | :--- |
| **Leaf** | `src/domain/leaves/` | **Zero-Dependency.** Cannot import other siblings. |
| **Root** | `src/domain/roots/` | **Vertical Composition.** Aggregates Leaf Records. |

**Composition Example:**
```mermaid
classDiagram
    class CharacterRoot {
        +UUID uid
        +IdentityRecord identity
        +HealthRecord health
    }
    class HealthRecord {
        +int current_hp
    }
    CharacterRoot *-- HealthRecord : Aggregates (Vertical)
```

## 3. Lateral Interaction (Protocols)
To prevent circular imports between Roots, interaction is handled via **Static Duck Typing**.

**Path:** `src/domain/common/contracts.py`

```mermaid
graph LR
    subgraph Root_A [Shop]
        ShopService
        PayerProtocol[Protocol: Payer]
    end
    
    subgraph Root_B [Character]
        CharacterRoot
    end
    
    CharacterRoot -- "Satisfies" --> PayerProtocol
    ShopService -- "Uses" --> PayerProtocol
```

**Implementation Directive:**
- Use `typing.Protocol` to define the "Shape" required.
- The Engine Orchestrator passes the Root across the boundary if it matches the protocol.
