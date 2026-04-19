---
id: ADR-005
title: "Domain Model Taxonomy"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-19
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/5"
---

# ADR 005: Domain Model Taxonomy

This document covers the **Static Classification** of the **Anemic Aggregate Packages** that compose a `domain/package`

**Structural Taxonomy (The "Species")**

Taxonomy is the classification of things based on shared characteristics. This is the **Type Enforcement** of the package's "DNA."

## Decision

### 1. The Five Levels of Identity
To manage the "Biologic" hierarchy, we define identity at five distinct levels:

| Identity Level | Value | Source |
| :--- | :--- | :--- |
| **Family** | `DomainFamily.ROOT` | `RootBlueprint` base class |
| **Species** | `"wagon"` | `WagonBlueprint` class name |
| **Breed (Variant)** | `"conestoga"` | `conestoga.json` (The Asset Breed) |
| **Individual** | `UUID-A1B2...` | `IdentityService` (Assigned at birth) |

### 2. The Type-Safe Manifest Strategy
We use the **Blueprint Class** (or Spore Class) as the central hook for package discovery. By passing the class to the `DomainContext`, we ensure:
- **Vertical Integrity:** The manifest knows the exact structure of its data.
- **Auto-Discovery:** The Engine derives family and species strings directly from the type.
- **Zero-Boilerplate:** Developers never manually type species strings in the manifest.

### 2. The Four Species of Data
Species defines **Individual Identity** and **Taxonomic Branch** (e.g., "wagon", "character").

| Species | Identity | Lifecycle | Role |
| :--- | :--- | :--- | :--- |
| **DomainRoot** | UUID | Stateful | The Sovereign "Actor". |
| **DomainRecord** | Anonymous | Stateful | Anemic fragments. |
| **DomainBlueprint** | Breed | Static | "Global Truth" templates. |
| **DomainSpore** | Value-based | Transient | Semantic types. |

### 2. The Domain Family (Structure)
Family defines the **Architectural Level** and **Package Role** within the Domain Layer.

| Family | Location | Interaction |
| :--- | :--- | :--- |
| **ROOT** | `src/domain/roots/` | Orchestrators; may aggregate Leafs. |
| **LEAF** | `src/domain/leaves/` | Atoms; Zero-dependency on other Leafs. |
| **SPORE** | `src/domain/common/` | Nomadic atoms; Shared Kernel elements. |

### 3. Taxonomical Rule of Composition
1. A **DomainRoot** may contain many **DomainRecords**.
2. A **DomainRecord** may contain many **DomainSpores**.
3. A **DomainRecord** (Leaf) MUST NOT contain a **DomainRoot**.
4. Horizontal interaction between **LEAF** families is forbidden.

## Status
**Adopted** 2026-04-15

## Addendum (2026-04-18): Abstraction and Species Identification
To enforce the abstract nature of the `DomainBlueprint` contract in Python and facilitate engine-level discovery, every blueprint must implement an abstract `__species__` property. This ensures that:
1.  Base contracts cannot be instantiated directly.
2.  All blueprints explicitly identify their taxonomic branch (e.g., "wagon", "malady") for structural verification and registry lookup.

## Addendum (2026-04-19): The Biologic Metaphor & Discovery Flow

To align with the "Biologic" architecture, we formally define the relationships between Domain Family members and their discovery sequence.

### Relationship Logic: Is-a vs. Has-a
- **DomainRoot (The Organism):** *Is-a* Sovereign Aggregate. It *has-a* **DomainRecord** (Vertical Aggregation).
- **DomainRecord (The Cell):** *Is-a* Leaf State Atom. It *has-a* **DomainSpore** (Composition of semantic types).
- **DomainSpore (The Nomad):** *Is-a* Nomadic Value Object. It is identity-less and owned entirely by its container.

### The Root Discovery Flow
The Engine Orchestrator uses the Root as the entry point for understanding the complete "organism" through Type Hint inspection.

```mermaid
graph TD
    Scanner[Engine Discovery Scanner] -->|1. Locate| Root[DomainRoot]
    Root -->|2. Inspect Type Hints| Record[DomainRecord]
    Record -->|3. Inspect Type Hints| Spore[DomainSpore]
    
    subgraph Registry_Hydration
        Root -->|Register| ContextRegistry
        Spore -->|Register| SporeRegistry
    end
    
    Note over Root,Spore: The Root anchors the context; <br/>Records and Spores are passive until Root discovery.
```
