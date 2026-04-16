---
title: "Project Implementation TODO"
description: "Comprehensive task list for establishing foundational infrastructure and architectural enforcement."
type: "reference"
status: "stable"
created_at: "2026-04-16 00:00:00"
updated_at: "2026-04-16 05:15:00"
owner: "Michael Naatjes"
tags: ["roadmap", "tasks", "implementation"]
version: "0.1.0"
---

# Oregon Trail Implementation TODO

This list tracks the tasks required to establish the foundational infrastructure and architectural enforcement for the **Screaming MVC** and **Anemic Aggregate** architecture, strictly following **ADR 001 through 009**.

## Phase 1: High-Leverage Design (TDD Phase)
*Goal: Define the "Engineering Blueprints" for core systems before implementation.*

1. **Domain Taxonomy Contracts** (`src/core/contracts/domain/`)
   - **Reasoning:** ADR 005 defines the theory of Roots, Records, Blueprints, and Value Objects. A TDD is now needed to define the engineering reality: specific Python base classes, mandatory fields, and immutability enforcement.
   - **Focus:** Mapping attributes, validation rules, and serialization strategies for each "Species."
   - [ ] Draft TDD: Domain Taxonomy Contracts
   - [ ] Implement foundational Taxonomy Contracts.

2. **Engine Orchestrator & Boot Lifecycle** (`src/engine/orchestrator.py`)
   - **Reasoning:** ADR 006 and 007 describe a complex two-phase bootstrap process (Register → Boot) and dynamic discovery.
   - **Focus:** Sequence Diagrams for package discovery, metadata reading (`__SERVICE_PROVIDER__`), and `BOOT_PRIORITY` enforcement.
   - [ ] Draft TDD: Engine Orchestrator
   - [ ] Implement `EngineOrchestrator` and Two-phase Bootstrap.

3. **Architecture Testing Regime (Fitness Functions)**
   - **Reasoning:** Screaming discipline (ADR 001, 004) requires automated enforcement to prevent "leaky" abstractions.
   - **Focus:** Linter-style scanning of `src/domain/` to enforce Leaf/Root isolation and mandatory metadata signatures.
   - [ ] Draft TDD: Architecture Testing Regime
   - [ ] Scaffold Testing Infrastructure in `tests/integration/architecture/`.
   - [ ] Implement `test_structure.py`, `test_taxonomy.py`, `test_ontology.py`, `test_dependencies.py`.

4. **Event Bus (The Nervous System)** (`src/core/events.py`)
   - **Reasoning:** ADR 007 identifies this as the mechanism for cross-domain reaction.
   - **Focus:** Payload structures and "silent leaf" policy—ensuring only Roots emit public events.
   - [ ] Draft TDD: Event Bus
   - [ ] Implement `EventBus`.

## Phase 2: Core Infrastructure Implementation
*Goal: Finalize the remaining kernel components.*

- [x] Implement `ServiceContainer` in `src/core/container.py`.
- [x] Implement `BaseServiceProvider` in `src/core/contracts/provider.py`.
- [ ] Implement `StateRegistry` in `src/engine/registry.py` for world snapshots (ADR 007).
- [ ] Implement System Tick (Heartbeat): Broadcast events for metabolic progression.

## Phase 3: Infrastructure Verification (Mock Domains)
*Goal: Use minimal functional mock-ups to verify the foundation and tests.*

- [ ] Create `src/domain/leaves/mock_leaf/`: Minimal anatomy to pass integrity tests.
- [ ] Create `src/domain/roots/mock_root/`: Verify Vertical Composition and Behavioral Ontology.
- [ ] Verify Test Failures: Ensure "Malicious" domains (e.g., circular dependencies) are caught.

## Phase 4: Pillar Infrastructure & Integration
*Goal: Define the boundaries for UI and Storage and wire the system.*

- [ ] Define `UIAdapter` and `StorageAdapter` boundaries.
- [ ] Ensure `src/main.py` correctly wires the Container, Orchestrator, and Adapters.
