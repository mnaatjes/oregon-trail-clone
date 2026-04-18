---
id: ADR-003
title: "Anemic Aggregator Domains"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-18
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/3"
---

# ADR 003: Anemic Aggregator Domains: Roots and Leafs

The Oregon Trail Domain needs a Comprehensive Structural Digest which outlines the rules and composition of *Packages* within `domain/` (the Model Concern of the established [Screaming MVC Architecture](./001_screaming_mvc.md))

## Context

The Planned Architecture MUST:

1. Ensure **Total Serializability**: Every domain state must be snapshottable without side effects.
2. Enforce **Strict Hierarchy**: Define the relationship between "Atoms" (Leafs) and "Assemblies" (Roots).
3. Guarantee **Anemic Purity**: Models (DTOs) contain data; Logic (Pure Math) contains transformations.

## Decision

### 1. The "Aggregator" Rule
A Root's primary purpose is to group related DomainRecords (Leaves) and DomainBlueprints into a single unit of identity.

* **Root Identity:** Each Root is assigned a sovereign UUID via the IdentityService.
* **Leaf Anonymity:** Leaves (DomainRecords) do not have their own identity; they are "owned" by the Root.

### 2. Composition Workflow (Vertical Only)
Horizontal interaction (Leaf-to-Leaf) is strictly forbidden. Communication happens via Vertical Composition:
1. **Root Service** identifies the needed **Leaf Services**.
2. **Root DTO** is reassembled by merging transformed **Leaf DTOs**.

### 3. Serialization Protocol
To achieve 100% snapshottability, all Domain models MUST be `@dataclass(frozen=True)`. Any mutation requires returning a new instance via a `clone()` or `replace()` operation.

## Consequences

### Positive
* **Save/Load Simplicity:** The entire game state is a tree of DTOs that can be dumped to JSON with zero logic processing.
* **Testing Isolation:** Leaf logic can be tested in 100% isolation as pure mathematical functions.

### Negative
* **Cloning Overhead:** Large aggregate Roots may experience minor performance impacts during high-frequency mutations (mitigated by Python's efficient reference handling).

## Status
**Adopted** 2026-04-16
