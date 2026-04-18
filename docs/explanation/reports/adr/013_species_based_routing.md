---
id: ADR-013
title: "Species-Based Engine Routing"
status: proposed
created_at: 2026-04-18
updated_at: 2026-04-18
component: engine
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/34"
---

# ADR 013: Species-Based Engine Routing

## Context
The Oregon Trail engine must orchestrate multiple complex domains (Wagons, Characters, Maladies) without becoming tightly coupled to their specific implementations. We need a "Plug-and-Play" infrastructure where the Engine can identify an object and route it to the appropriate Service, View, or Logic handler without manual `import` statements or hardcoded switch-cases.

## Decision
We will use the **Species String** (defined in ADR-005 and TDD-007) as the universal "Routing Key" for all Engine-level orchestration.

### 1. The Routing Tables
The Engine will maintain internal registries (inheriting from `BaseRegistry`) that use the Species String as the primary key:
*   **ServiceRegistry**: Maps `"species_name"` -> `ServiceInstance` (e.g., `"wagon"` -> `WagonService`).
*   **ViewRegistry**: Maps `"species_name"` -> `ViewComponent` (e.g., `"wagon"` -> `WagonUI`).
*   **LogicRegistry**: Maps `"species_name"` -> `LogicModule` (e.g., `"wagon"` -> `WagonLogic`).

### 2. Registration via Manifest
During the Boot Lifecycle, the Engine will scan `DomainContext` manifests (#13). These manifests are responsible for "Self-Reporting" their species and their associated handlers to the Engine's registries.

### 3. Orchestration Flow
When the Engine encounters a `DomainRoot`:
1.  It reads the `root.__species__` property.
2.  It queries the `ServiceRegistry.get(species)` to find the handler.
3.  It passes the `DomainRoot` to that service for processing.

## Consequences

### Positive
*   **Complete Decoupling**: The Engine remains agnostic of domain-specific math and data structures.
*   **High Extensibility**: New domains can be added by simply dropping a folder into `src/domain/` with a valid `DomainContext`.
*   **Simplicity**: Routing logic is reduced to a simple dictionary lookup (`O(1)` performance).

### Negative
*   **Late Binding**: Errors in routing (e.g., a missing service for a species) will only be discovered at runtime/boot time rather than compile time. (Mitigated by a mandatory "Boot Validation" check).

## Status
**Proposed** 2026-04-18
