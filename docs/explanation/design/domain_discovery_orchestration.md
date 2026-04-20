---
id: TDD-014
parent_adr: ADR-014
title: "TDD: Domain Discovery & Orchestration System"
status: draft
created_at: 2026-04-20
updated_at: 2026-04-20
component: engine
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/42
---

# TDD: Domain Discovery & Orchestration System

## 1. Overview
This specification defines the "Conductor-Based" initialization of the Domain Layer. It uses the `DomainContext` as the single source of truth to automate the discovery, registration, and hydration of all domain packages. This system bridges the gap between the static Domain Spec and the active Game Engine.

## 2. Goals & Non-Goals
### Goals
*   **Zero-Boilerplate Wiring:** Automate the registration of Services, Spores, and Blueprints.
*   **Priority-Aware Booting:** Ensure domains with dependencies (e.g., Wagons) boot after their requirements (e.g., Maps).
*   **Strict Encapsulation:** Enforce the "Package Threshold" SOP (ADR-016).
*   **Separation of Concerns:** Decouple "Registration" (Infrastructure) from "Business Logic" (Service).

### Non-Goals
*   This system does not handle the **Game Loop** (Ticks/Turns).
*   This system does not handle **Persistence** (Saving/Loading state).

## 3. Component Specification

### 3.1 BaseDomainService (The Actor)
*   **Path:** `src/core/domain/contracts/service.py`
*   **Role:** The stateless "Operator" of an aggregate root. 
*   **Contract:** 
    *   Must implement the `Bootable` protocol (optional `boot()` method).
    *   Zero awareness of the `ServiceContainer` or `Provider`.
    *   Focuses purely on coordinating `logic.py` and `models.py`.

### 3.2 BaseServiceProvider (The Infrastructure)
*   **Path:** `src/core/kernel/contracts/provider.py`
*   **Role:** The "Electrician" that wires a package into the Engine.
*   **Key Feature: Domain Facades.**
    *   Provides type-hinted `@property` access to: `self.events` (`EventBus`) and `self.assets` (`AssetService`).
    *   Decouples the domain developer from `self.container.get("string_key")`.

### 3.3 DomainRegistrar (The Archivist)
*   **Path:** `src/engine/domain/registrar.py`
*   **Role:** Handles the **Static DNA** of a package.
*   **Logic:** 
    *   If `family == SPORE`: Registers the `intent` class in the `SporeRegistry`.
    *   If `family == LEAF`: Registers the `intent` class in the `BlueprintRegistry`.
    *   Also handles the registration of `logic.py` modules into the `LogicRegistry`.

### 3.4 DomainProviderFactory (The Wire-Man)
*   **Path:** `src/engine/domain/provider_factory.py`
*   **Role:** Produces the correct `ServiceProvider` for a discovered package.
*   **Logic:** 
    *   **The Check:** If `DomainContext.provider_class` is defined, instantiate the user's custom provider.
    *   **The Fallback:** If no custom provider exists, instantiate a `StandardDomainProvider` that automatically binds the `DomainContext.service` to the `ServiceContainer`.

### 3.5 DomainOrchestrator (The Conductor)
*   **Path:** `src/engine/domain/orchestrator.py`
*   **Role:** The active agent that manages the total lifecycle.
*   **Logic:**
    1.  **Discovery:** Scans `src/domain/` for `__CONTEXT__` objects.
    2.  **Graphing:** Sorts discovered packages into a **Priority Queue** (0-100).
    3.  **Registration:** Iterates through the queue and tells the `Registrar` and `ProviderFactory` to perform their wiring (`Phase 1`).
    4.  **Booting:** Iterates through the queue again and triggers `.boot()` on all registered services (`Phase 2`).

## 4. Diagnostic Goals & Checklist
- [ ] **Discovery Audit:** Verify filesystem scanning identifies packages with `__init__.py` manifests.
- [ ] **SOP Guard:** Raise `TypeError` if a `ROOT` package fails to provide a `service`.
- [ ] **Sequence Integrity:** Ensure `Phase 2 (Boot)` only starts after `Phase 1 (Register)` is complete for the entire priority graph.
- [ ] **Facade Verification:** Ensure `BaseServiceProvider` facades correctly resolve from the `ServiceContainer`.
