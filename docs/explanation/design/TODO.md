---
title: "Project Implementation TODO"
description: "Comprehensive task list for establishing foundational infrastructure and architectural enforcement."
type: "reference"
status: "stable"
created_at: "2026-04-16 00:00:00"
updated_at: "2026-04-16 00:00:00"
owner: "Michael Naatjes"
tags: ["roadmap", "tasks", "implementation"]
version: "0.1.0"
---

# Oregon Trail Implementation TODO

This list tracks the tasks required to establish the foundational infrastructure and architectural enforcement for the **Screaming MVC** and **Anemic Aggregate** architecture, strictly following **ADR 001 through 007**.

## Phase 1: Core Architectural Contracts (ADR 001, 002, 005)
*Goal: Define the "Species" and "Laws of Physics" for the domain layer.*

- [x] Implement `ServiceContainer` in `src/core/container.py`.
- [x] Implement `BaseServiceProvider` in `src/core/contracts/provider.py`.
- [ ] Implement foundational Taxonomy Contracts in `src/core/contracts/domain/`:
    - [ ] `DomainRoot`: Sovereign entity with UUID (ADR 005).
    - [ ] `DomainRecord`: Anemic state fragment (ADR 005).
    - [ ] `DomainBlueprint`: Slug-based static template (ADR 005).
    - [ ] `DomainValueObject`: Shared semantic types in `domain/common` (ADR 005).
- [ ] Implement `EventBus` (The Nervous System) in `src/core/events.py` (ADR 007).
- [ ] Implement `StateRegistry` in `src/engine/registry.py` for world snapshots (ADR 007).

## Phase 2: Architecture Testing Regime (Fitness Functions)
*Goal: Automatically enforce ADR compliance (ADR 004, 006).*

- [ ] Scaffold Testing Infrastructure in `tests/integration/architecture/`:
    - [ ] `conftest.py`: Dynamic domain discovery (Root/Leaf separation).
    - [ ] `helpers.py`: Linter-style violation reporting.
- [ ] Implement `test_structure.py` (ADR 004):
    - [ ] Verify mandatory Anatomy: `models.py`, `logic.py`, `services.py`, `__init__.py`.
    - [ ] Enforce `__all__` exports in `__init__.py` (The Facade).
- [ ] Implement `test_taxonomy.py` (ADR 002, 005, 006):
    - [ ] Verify inheritance from `DomainRoot`/`DomainRecord`.
    - [ ] Verify Package-Level Signatures in `__init__.py`:
        - [ ] `__DOMAIN_SPECIES__` (ROOT vs LEAF).
        - [ ] `__DOMAIN_INTENT__` (Screaming Intent).
        - [ ] `__SERVICE_PROVIDER__` (Bootstrap pointer).
- [ ] Implement `test_ontology.py` (ADR 006):
    - [ ] Verify `DomainRoot` class metadata:
        - [ ] `BOOT_PRIORITY` (Sequence control).
        - [ ] `REQUIRED_PILLARS` (Dependency guarding).
        - [ ] `DOMAIN_SCOPE` (Lifecycle management).
- [ ] Implement `test_dependencies.py` (ADR 002, 004):
    - [ ] Enforce **Zero-Dependency Leaf Policy**.
    - [ ] Prevent horizontal imports between Roots (Direct imports forbidden).

## Phase 3: Infrastructure Verification (Mock Domains)
*Goal: Use minimal functional mock-ups to verify the foundation and tests.*

- [ ] Create `src/domain/leaves/mock_leaf/`:
    - [ ] Minimal `models.py`, `logic.py`, `services.py` to pass integrity tests.
- [ ] Create `src/domain/roots/mock_root/`:
    - [ ] Verify Vertical Composition (aggregating `mock_leaf` models).
    - [ ] Verify Behavioral Ontology (metadata-driven boot sequence).
- [ ] Verify Test Failures:
    - [ ] Create a "Malicious" domain (e.g., circular dependency) and ensure tests catch it.

## Phase 4: Engine Orchestration (ADR 006, 007)
*Goal: Implement the "Conductor" that manages the Ecosystem.*

- [ ] Implement `EngineOrchestrator` in `src/engine/orchestrator.py`:
    - [ ] Directory Discovery of `ROOT` and `LEAF` packages.
    - [ ] Two-phase Bootstrap (Register -> Boot) using `__SERVICE_PROVIDER__`.
    - [ ] Sequence control via `BOOT_PRIORITY`.
- [ ] Implement System Tick (Heartbeat):
    - [ ] Broadcast events for metabolic progression.

## Phase 5: Pillar Infrastructure (ADR 001)
*Goal: Define the boundaries for UI and Storage.*

- [ ] Define `UIAdapter` and `StorageAdapter` boundaries.
- [ ] Ensure `src/main.py` correctly wires the Container, Orchestrator, and Adapters.
