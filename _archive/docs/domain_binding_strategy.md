# Domain Binding Strategy: Technical vs. Functional Wiring

In the Oregon Trail engine, we distinguish between two distinct "wiring" systems: **Technical Infrastructure** and **Functional Execution**. Understanding this parallel is key to maintaining a decoupled, modular architecture.

## 1. The "Wiring" Parallel

The `DomainBinding` is to the **Engine** what the `ServiceProvider` is to the **ServiceContainer**. One handles the construction of the system, while the other handles its runtime execution.

| Feature | ServiceProvider | DomainBinding |
| :--- | :--- | :--- |
| **System** | **Technical Infrastructure** | **Game Logic Execution** |
| **Target** | `ServiceContainer` | `Engine Orchestrator` |
| **Goal** | **Discovery**: "What tools exist?" | **Execution**: "What rules do I run?" |
| **Phase** | **Boot Phase**: (Once at startup) | **Tick Phase**: (Every frame/day) |

---

## 2. Relationship: 1:1 with the Domain Package

The `DomainBinding` has a **1:1 relationship with the Domain Package (Bounded Context)**, rather than individual `DomainEntities`. 

### The Reasoning:
-   **Encapsulation**: A Domain Package (e.g., `health`) represents a single "Area of Expertise." It owns all the math, state changes, and rules for its domain. The Engine coordinates with a single "representative" (the Binding) rather than multiple granular objects.
-   **Capability-Based Orchestration**: In a truly modular engine, a domain doesn't care about the specific identity of an entity (e.g., a `Person` or an `Ox`). it only cares that the entity possesses the required **"Capability"** (e.g., "Healthiness").
-   **Screaming Architecture**: Keeping one binding per package maintains the clarity of the `src/domain/` directory, preventing it from being cluttered by redundant binding files for every entity type.

---

## 3. Handling Multiple Entities via Protocols

If a domain needs to manage multiple entity types (e.g., Health for both `Person` and `Ox`), it uses a **Capability Protocol** rather than separate bindings.

```python
# src/domain/health/binding.py

from typing import Protocol, runtime_checkable
from src.core.contracts.domain import DomainBinding
from .models import HealthState, MaladyBlueprint

# Define a 'Capability' rather than a 'Type'
@runtime_checkable
class Healthable(Protocol):
    state: HealthState
    blueprint: any

class HealthBinding(DomainBinding[Healthable, HealthState, MaladyBlueprint]):
    """
    One binding for the WHOLE health package.
    It can orchestrate ANYTHING that is 'Healthable'.
    """
    def orchestrate(self, entity: Healthable):
        # The logic is applied to the 'Capability' of being healthy,
        # regardless of whether the entity is a Person or an Ox.
        self.service.process_health(entity)
```

---

## 4. Summary of the Hierarchy

Every domain package follows a consistent internal structure:

1.  **`src/domain/<package>/`** (The Bounded Context)
    -   **`provider.py`**: The **Technical Wiring**. Tells the Container how to build the tools.
    -   **`binding.py`**: The **Functional Wiring**. Tells the Engine how to run the rules.
    -   **`models.py`**: The "Patients" (State Containers).
    -   **`logic.py`**: The "Math" (Pure Rules).
    -   **`service.py`**: The "Orchestrator" (Coordinates local logic).

**Verdict**: Keeping the binding 1:1 with the package maintains the **Universal Domain Blueprint (UDB)** and ensures that the Engine interacts with a unified, expert representative of that domain.
