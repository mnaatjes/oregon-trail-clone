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

## 5. Plan of Execution

### Questions

1. Where to implement `ArchitecuralGuard` for Domain?

    * Should `ArchitectureGuard` be a contract with a `DomainGuard` implementation?
    * Should `ArchitectureGuard` be a Global Service?

2. What types of `ArchitectureGuard` methods are needed?

    * `LogicEntity` existance and composititon

3. What type/Object definitions are needed?

    * `LogicEntity`?
    * `DomainService` - Started
    * `PriorityGraph` - Where? What (Global Service)?

4. What is left todo for *Facade Enforcement*?

    * Is it still necessary to prevent leakage using `__all__` (See [Facade Enforcement](../reports/adr/004_domain_package_anatomy.md#3-facade-enforcement-__all__))?

5. What todos for `LogicEntity` enforcement and validation (See [Domain Logic Entities](./domain_logic_entities.md#2-goals--non-goals))?

    * Enforce purity of all logic functions
    * Enforce composition and type as *functions*
    * Where are these functions going and how will they be accessed/addressed? i.e. `module_name.<function-name>` e.g. `domain.root.wagon.apply_damage`
    * What is *Side-Effect Isolation*? How is it enforced? Why at the `LogicEntity` level and not package as whole? Part of *Zero Leaf Dependency* Architecture Guards
    * What are *Atomic Transformations*?

6. What are the `Package` and `Facade` level **Architecture Guards**?

    * `LogicEntity` composition and enforcement
    * `DomainService` composition and encapsulation
    * *Zero Dependency Leaf* isolation
    * *Horizontal* Violations
    * *Vertical* Violations
    * *Compositional* Violations: e.g. does filepath `domain/root/<package-name>` have `DomainRoot` entity, do `DomainContext` properties align? Is the *Aggregate Root* composed of all necessary components/files?
    * **Goal:** Get list of *Composition* rules together by entity and start checking them off
    * Should we identify where existing `[X VIOLATIONS]` take place to enroll them into an `ArchitectureGuard` Service?
    * Should we document *SOP*s for an `SOPGuard` sub-Service of the `ArchitectureGuard`? e.g raise `TypreError` if `ROOT` package has no `Service`.
    * How can we separate *Service Flow* from *Logic* [[ADR-004] Domain Package Anatomy](https://github.com/mnaatjes/oregon-trail-clone/issues/4)

7. What are the output types/Objects **FROM** `DomainOrchestrator`?

    * `DomainScanner` &rarr; `Package` containing: `Facade`, `DomainContext`
    * From `Package.facade.context.priority` &rarr; `PriorityGraph`
    * From `Package.facade.context.requirements` &rarr; `KernelSubsystem` Services (`EventBus`, `AssetsManager`, ...)
    * What would an `AggregateManigest` accomplish?

8. How to turn `Package` entity into:
    * `PriorityGraph`
    * Accessible Domain Entities

9. Determine when to close-out branch `feat/52-domain-scanner` and move on to `DomainOrchestrator`:

    * Do we need to add any properties to `Package` or `Facade`?
    * Do we need to perform follow-up testing on *Discovery* system? **YES**

10. Github Issue [[ADR-004] Domain Package Anatomy](https://github.com/mnaatjes/oregon-trail-clone/issues/4) refers to `domain package contains the mandatory 4-file set` - Do ALL Domain entities need a `service.py` file?

11. Where and how are we going to collect necessary properties and components from *Aggregate Root*s?

    * Are Services captured from the **Import** line, the `DomainContext.service` property, or the file `service.py`? - **Via `DomainContext.service` &rarr; `DomainManifest` linked *Service Provider* instance**
    * How is the `LogicEntity` captured from the `logic.py` file? What if there is no *Logic* needed? - **Via `Registrar`**


### Follow-up Testing

1. Scanner and Associated entities/objects/classes:
    * `BaseScanner`, `DomainScanner`
    * `DiscoveryUnit`, `Package`, `Facade`

2. Scanner Tests:

    * Scanning doesn't go deeper than `domain/{root,leaf}/<package-name>/__init__.py`
    * Scanner stays within `key` e.g. `domain`
    * Scanner fails appropriately

### Follow-up Questions

1. Priority 1: Core Orchestration and Data Flow:

    * Should we integrate a `DiscoveryManifest` base-contract as the output type of `BaseScanner` to be at parity with `DiscoveryUnit`? This seems like a logial integration and maintains SRP. Then DomainScanner will implement it's own `DomainManifest` implementation. What would/should a `DiscoveryManifest` have for properties? I assume it should be a frozen-dataclass?

    * Do the `Facade` or `Package` entities need to extract any more information from the `__init__.py` file or use any other `importlib.util` methods? Or do they have sufficient information for the `DomainOrchestrator` and/or `DomainRegistrar` to get the required attributes?

3. Architectural Guarding

    * Service will be called `ArchitecturalPolice`. Will it be a **Static** class? How will it be accessed? Would a facade make sense? I want type-hinting to no relying on just the `ServiceContainer.get(...)` method.
    
    * Can it be composed of `BaseGuard` contracts? These would define output format, have rules for Error types and perhaps even facade methods for ease-of-use.

    * Location of `ArchitecturalPolice` is `src/core/kernel`. Where would `BaseGuard` contract go? Where would implementations of `BaseGuard` go? If we created specific exceptions, where would those be declared?

4. Logical Entities: 

    * What are the **rules** for *Purity*?
    * How to check that Logical Entities have no *side-effects* like IO?
    * Do we need a `LogicEntity` type? What would it represent - each function or all functions within a Package's `logic.py` file?
    * What DX considerations must we implement to ease-of-use when addressing package-logic-functions?

5. Project Management: 

    * Review TODO Tests and the associated classes, types, and objects of Discovery Scanner system. What tests do we need to perform?
    * Do we need to add any more properties to the `Package` or `Facade` entitites?
    * We should integrate the `DiscoveryManifest` into the Scanner/Discovery system before closing the branch. How will this be accomplished - should it be a wise decision to do so?

### Follow-up TODOs

1. Spec out the `DiscoveryManifest`

    * Base Contract
    * Integrated into `BaseScanner`
    * Implemented `DomainManifest` should link `Package` to instantiated `ServiceProvider`

2. Aggregate Composition & SOPs

    * **Only `ROOT` Packages** need `service.py` file
    * Update `DomainContext` validation to reflect

3. ArchitecturalGuard Service

    * Create `ArchitecturalPolice` Service in `src/core/kernel`
    * Not a *Global* Service. *Runtime* Service
    * **Static** Analysis Tool AND **Boot-time** Validator
    * Target **Implementation Sections:** 
        - `HorizontalGuard` e.g. Roots cannit import Roots
        - `VerticalGuard` e.g. 
        - `AnatomyGuard` e.g. Records CANNOT have IDs
        - `CompositionGuard` e.g. verify all the 4-file set for Roots, 3 for others with 1 optional

4. Logical Entities

    * They are **Stateless Functions**
    * Use python `inspect` module to verify functions in `logic.py` are *Pure* e.g. argument Record and return a record
    * 