---
id: ADR-010
title: "Asset Management & Directory Mirroring"
status: proposed
created_at: 2026-04-17
updated_at: 2026-04-17
component: engine
type: "explanation/adr"
epic_link: "PENDING"
---

# ADR 010: Asset Management & Directory Mirroring

## Context
The Oregon Trail clone relies on **DomainBlueprints** (static "Global Truths") to hydrate its anemic state. We need a system that decouples data from code while ensuring their relationship is discoverable and strictly enforced.

## Decision
We adopt a **Strict Physical Mirroring** strategy between `src/domain/` and `assets/domain/`.

### 1. The Mirroring Mandate
Assets must reside in a path that mirrors their code counterparts.
* `src/domain/roots/wagon/` -> `assets/domain/roots/wagon/`

### 2. The Asset Pipeline
The **AssetManager** service handles the mapping of JSON files to `DomainBlueprint` objects during bootstrap.

## Status
**Proposed** 2026-04-17
