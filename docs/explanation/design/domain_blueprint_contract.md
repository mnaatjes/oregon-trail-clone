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
*   **Slug-Based Identity:** Provide a unique, dot-notated string for global lookup and registry.
*   **Standardized UI Metadata:** Ensure every blueprint contains visual instructions for the UI layer via `DisplayBlueprint`.

### Non-Goals
*   **Nomadic Blueprints:** `SPORE` (ValueObjects) are blueprint-free; they are nomadic data bundles.
*   **Composition:** Blueprints do not perform composition; they define the "Recipe" that a Service uses to compose a Root.

## 3. Proposed Design

### Directory Structure Refactor
To enforce structural safety, the flat `blueprint.py` is refactored into:
`src/core/contracts/domain/blueprints/`
- `base.py`: The abstract `DomainBlueprint`.
- `root.py`: The specialized `RootBlueprint`.
- `record.py`: The specialized `RecordBlueprint`.

### Data Schema (Core Fields)
All `DomainBlueprint` implementations must include:
*   **`slug: str`**: The unique identifier (e.g., `domain.roots.wagon.conestoga`).
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
2.  **Naming Convention:** Slugs must follow: `domain.<family>.<species>.<package>.<filename>`.
3.  **Strict Typing:** A `RootBlueprint` MUST NOT be used to initialize a `DomainRecord`.

## 5. Diagnostic Goals
*   **DNA Audit:** Automated verification that a Blueprint's `family` property matches its physical class (`RootBlueprint` vs `RecordBlueprint`).
*   **Species Integrity:** Ensure that the `species` string matches the intent declared in the package's `DomainContext`.
*   **Mirror Audit:** Fitness function verifying that every Blueprint in `src/` has a corresponding JSON in `assets/`.
