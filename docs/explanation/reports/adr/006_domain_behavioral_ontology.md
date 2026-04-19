---
id: ADR-006
title: "Domain Behavioral Ontology"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-18
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/6"
---

# ADR 006: Domain Behavioral Ontology

This document relates to the **Systemic Topology** of the Domain (Model Concern). This will be termed **Behavioral Ontology**

The Bootstrap and Engine Systems need a reliable way to Identify, Load, and Interact with Domain Aggregate Root and Leaf Packages.

## Decision

### 1. The Metadata Manifest
Every package's `__init__.py` must expose a `DomainContext` manifest assigned to the variable `__CONTEXT__`. This replaces the previous individual metadata properties.

| Field | Type | Description |
| :--- | :--- | :--- |
| `family` | `DomainFamily` | ROOT or LEAF classification. |
| `intent` | `str` | Human-readable "Scream" of the package. |
| `priority` | `int` | Sequential boot order (0-100). |
| `requirements` | `List[str]` | Required kernel subsystems (Events, Assets, etc). |
| `service` | `Type[Any]|None` | The Domain Service class (Enables Zero-Provider auto-wiring). |

### 2. Boot Priority
To ensure the world is built in the correct order, we adopt a sequential priority:
1. **Infrastructure (0-19):** Registry, Event Bus, Identity.
2. **Environment (20-39):** Weather, Map, Locations.
3. **Actors (40-59):** Wagon, Character, Inventory.
4. **Logic (60-79):** Encounter Engines, Progression.
5. **Interface (80-100):** UI, Input Listeners, Storage Adapters.

## Status
**Adopted** 2026-04-15
**Updated** 2026-04-19 (Terminology alignment with ADR-005 and TDD-002)
**Addendum** 2026-04-19: **Zero-Provider Strategy.** To minimize boilerplate and enforce "Anemic Purity," domain packages are transitioned to a "Zero-Provider" model. The Engine Orchestrator will perform Automated Constructor Injection for the `service` class based on the `requirements` list, eliminating the need for `provider.py` files in 90% of domain packages. Explicit type-hinting in domain constructors is now the primary mechanism for dependency wiring.

