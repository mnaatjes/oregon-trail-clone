---
id: ADR-005
title: "Domain Model Taxonomy"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-18
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/5"
---

# ADR 005: Domain Model Taxonomy

This document covers the **Static Classification** of the **Anemic Aggregate Packages** that compose a `domain/package`

**Structural Taxonomy (The "Species")**

Taxonomy is the classification of things based on shared characteristics. This is the **Type Enforcement** of the package's "DNA."

## Decision

### 1. The Four Species of Data

| Species | Identity | Lifecycle | Role |
| :--- | :--- | :--- | :--- |
| **DomainRoot** | UUID | Stateful | The Sovereign "Actor" (e.g., Character). |
| **DomainRecord** | Anonymous | Stateful | Anemic fragments (e.g., Health status). |
| **DomainBlueprint** | Slug | Static | "Global Truth" templates (e.g., Farmer profession). |
| **DomainValueObject** | Value-based | Transient | Semantic types (e.g., Money, Coord). |

### 2. Taxonomical Rule of Composition
1. A **DomainRoot** may contain many **DomainRecords**.
2. A **DomainRecord** may contain many **DomainValueObjects**.
3. A **DomainRecord** (Leaf) MUST NOT contain a **DomainRoot**.

## Status
**Adopted** 2026-04-15

## Addendum (2026-04-18): Abstraction and Species Identification
To enforce the abstract nature of the `DomainBlueprint` contract in Python and facilitate engine-level discovery, every blueprint must implement an abstract `__species__` property. This ensures that:
1.  Base contracts cannot be instantiated directly.
2.  All blueprints explicitly identify their taxonomic branch (e.g., "wagon", "malady") for structural verification and registry lookup.
