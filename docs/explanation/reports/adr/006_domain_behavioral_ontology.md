---
id: ADR-006
title: "Domain Behavioral Ontology"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-15
component: core
type: "explanation/adr"
epic_link: "PENDING"
---

# ADR 006: Domain Behavioral Ontology

This document relates to the **Systemic Topology** of the Domain (Model Concern). This will be termed **Behavioral Ontology**

The Bootstrap and Engine Systems need a reliable way to Identify, Load, and Interact with Domain Aggregate Root and Leaf Packages.

## Decision

### 1. The Metadata Signatures
Every package's `__init__.py` must expose specific metadata to the Engine Orchestrator:
* `__DOMAIN_SPECIES__`: (ROOT or LEAF).
* `__DOMAIN_INTENT__`: Human-readable "Scream."
* `__SERVICE_PROVIDER__`: Path to the DI registration class.

### 2. Boot Priority
To ensure the world is built in the correct order, we adopt a sequential priority:
1. **Infrastructure (0-9):** Registry, Event Bus.
2. **Environment (10-19):** Weather, Map.
3. **Actors (20-29):** Wagon, Character.
4. **Interface (90+):** UI, Input Listeners.

## Status
**Adopted** 2026-04-15
