---
id: TDD-001
parent_adr: ADR-005
title: "TDD: DomainBlueprint Contract"
status: approved
created_at: 2026-04-17
updated_at: 2026-04-19
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/44
---

# TDD: DomainBlueprint Contract

## 1. Overview
The `DomainBlueprint` is the engineering realization of the **Global Truth** (ADR-005). It is a static, read-only template that defines the immutable "DNA" of a domain entity. It serves as the specification used by Services to initialize stateful `DomainRoot` or `DomainRecord` instances.

## 2. Goals & Non-Goals
### Goals
*   **Taxonomical Enforcement:** Ensure blueprints explicitly identify their `DomainFamily` (ROOT/LEAF) and `Species` (e.g., "wagon").
*   **Enforce Immutability:** Ensure templates cannot be modified at runtime.
*   **Breed-Based Identity:** Provide a unique, dot-notated string for global lookup and registry (e.g., `domain.roots.wagon.conestoga`). This is the **Variant**.
*   **Standardized UI Metadata:** Ensure every blueprint contains visual instructions for the UI layer via `DisplayBlueprint`.

### Non-Goals
*   **Nomadic Blueprints:** `SPORE` (ValueObjects) are blueprint-free; they are nomadic data bundles.
*   **Composition:** Blueprints do not perform composition; they define the "Recipe" that a Service uses to compose a Root.

## 3. Proposed Design

### The Five Levels of Identity
To manage the "Biologic" hierarchy, we define identity at five distinct levels:

| Identity Level | Value | Source |
| :--- | :--- | :--- |
| **Family** | `DomainFamily.ROOT` | `WagonRoot` class inheritance |
| **Species** | `"wagon"` | `WagonBlueprint.species` property |
| **Breed (Variant)** | `"conestoga"` | `conestoga.json` (The Asset Breed) |
| **UID (Individual)** | `UUID-A1B2...` | `IdentityService` (Assigned at birth) |

### Directory Structure Refactor
To enforce structural safety, the flat `blueprint.py` is refactored into:
`src/core/contracts/domain/blueprints/`
- `base.py`: The abstract `DomainBlueprint`.
- `root.py`: The specialized `RootBlueprint`.
- `record.py`: The specialized `RecordBlueprint`.

### Data Schema (Core Fields)
All `DomainBlueprint` implementations must include:
*   **`breed: str`**: The unique variant identifier (e.g., `conestoga`).
*   **`display: DisplayBlueprint`**: A nested DTO containing UI hints (label, icon, color).
*   **`family: DomainFamily`**: The architectural role (`ROOT` or `LEAF`).
*   **`species: str`**: The taxonomic branch (e.g., "wagon", "character").

### The Spore Prohibition
The `DomainBlueprint` base class implements a guard that prevents any blueprint from claiming the `SPORE` family, as Spores are nomadic and blueprint-free.

## 4. Detailed Design

### Specialized Blueprint Contracts

```python
# src/core/contracts/domain/blueprints/root.py
@dataclass(frozen=True)
class RootBlueprint(DomainBlueprint):
    family: DomainFamily = DomainFamily.ROOT
    # required_records: List[str] - Hook for assembly validation
```

```python
# src/core/contracts/domain/blueprints/record.py
@dataclass(frozen=True)
class RecordBlueprint(DomainBlueprint):
    family: DomainFamily = DomainFamily.LEAF
```

### Constraints
1.  **Immutability:** Must be decorated with `@dataclass(frozen=True)`.
2.  **Naming Convention:** Breed identifiers must follow: `domain.<family>.<species>.<breed>`.
3.  **Strict Typing:** A `RootBlueprint` MUST NOT be used to initialize a `DomainRecord`.

## 5. Implementation Philosophy: Family Automation (Zero-Boilerplate)
To minimize developer friction while maintaining strict type-safety, we utilize inheritance-based automation:
*   **Specialized Parents:** By extending `RootBlueprint` or `RecordBlueprint`, the developer implicitly defines the architectural role of the blueprint.
*   **Automatic Family Assignment:** The base classes automatically assign the correct `DomainFamily` (ROOT or LEAF).
*   **Proactive Guards:** The `DomainBlueprint` base class utilizes `__init_subclass__` to proactively forbid the use of the `SPORE` family in any blueprint implementation.
*   **Result:** The developer focus remains entirely on defining the data attributes of the species, while the architecture handles the taxonomical wiring.

## 6. Diagnostic Goals
*   **DNA Audit:** Automated verification that a Blueprint's `family` property matches its physical class (`RootBlueprint` vs `RecordBlueprint`).
*   **Species Integrity:** Ensure that the `species` string matches the intent declared in the package's `DomainContext`.
*   **Mirror Audit:** Fitness function verifying that every Blueprint in `src/` has a corresponding JSON in `assets/`.
