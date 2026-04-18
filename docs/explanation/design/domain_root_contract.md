---
id: TDD-007
parent_adr: ADR-003
title: "TDD: DomainRoot Contract"
status: stable
created_at: 2026-04-17
updated_at: 2026-04-18
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/18
---

# TDD: DomainRoot Contract

## 1. Overview
The `DomainRoot` is the engineering realization of the **Aggregate Root** (ADR-003). It is a passive, anemic Data Transfer Object (DTO) that anchors a Bounded Context through a globally unique UUID.

## 2. Goals & Non-Goals
### Goals
*   Enforce a mandatory, persistent UUID for every sovereign actor.
*   Act as the primary "Container" for vertical composition (aggregating Leaves).
*   Ensure 100% serializability for world snapshotting.

### Non-Goals
*   Containing business logic (delegated to `logic.py`).
*   Emitting events (delegated to `services.py`).

## 3. Proposed Design

### Data Schema (Core Fields)
All `DomainRoot` implementations must include:
*   `uid: UUID`: Unique identifier assigned by the `IdentityService`.
*   `blueprint: DomainBlueprint`: The static template used for initialization.
*   `records: Dict[str, DomainRecord]`: A mapping of aggregated Leaf Records.

### Constraints
1.  **Taxonomy:** Must inherit from `src/core/contracts/domain/root.py:DomainRoot`.
2.  **Anemic:** Must be a `@dataclass(frozen=True)`. No methods other than `clone()` are permitted.
3.  **Sovereignty:** Only one `DomainRoot` is allowed per Root Package.
4.  **Property Proxies (DX):** Implementations should use `@property` getters to provide type-safe access to the `records` dictionary.

### Implementation Example (Hybrid Strategy)
To satisfy both the engine's need for a generic `records` dictionary and the developer's need for type-safe access, the following pattern is mandated:

```python
from typing import cast
from src.core.contracts.domain.root import DomainRoot
from src.domain.wagon.records import WheelsRecord # Local Leaf Record

@dataclass(frozen=True)
class WagonRoot(DomainRoot):
    @property
    def __species__(self) -> str:
        return "wagon"

    # The 'records' dict satisfies TDD-012 and Engine Orchestration
    # records: Dict[str, DomainRecord] (Inherited)

    @property
    def wheels(self) -> WheelsRecord:
        """Type-safe proxy for engine-generic records."""
        return cast(WheelsRecord, self.records["wheels"])

    def clone(self) -> "WagonRoot":
        return replace(self, records={k: v.clone() for k, v in self.records.items()})
```

## 4. Rationale: Why the Hybrid Pattern?
*   **Engine Genericism:** The `StateRegistry` can treat every `DomainRoot` as a uniform envelope of records for bulk serialization/snapshots without knowing the internal schema.
*   **Developer Experience:** The `@property` proxies provide full IDE autocompletion and type-safety for logic and services.
*   **Decoupling:** New leaf records can be added to the `records` dict dynamically (e.g., status effects) without requiring a schema change to the Root class.

## 5. Diagnostic Goals
*   **Identity Check:** Automated validation that the `uid` is never null or malformed.
*   **Composition Audit:** Ensuring that a `DomainRoot` only contains `DomainRecord` or `DomainValueObject` types.
