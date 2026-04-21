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

### Refinement Questions

1. `DiscoveryManifest`

Given 
```py
# Declare Typevar
T = TypeVar("T", bound=DiscoveryUnit)

class BaseScanner(ABC, Generic[T]):
    @abstractmethod
    def scan(self, path:str) -> List[T]:
        """Find all units of type T in the given path."""
        pass
```

How do we properly introduce the `DiscoveryManifest` and enforce its usage?

2. `ArchitecturalPolice`

    * Name recomendations: change `PoliceUnit` to `GuardUnit`? Recommend other intuitive names

    * Recommended `The Facade: Access it via self.police on the BaseServiceProvider. This gives you full IDE type-hinting.` Does this mean a ServiceProvider registers the PoliceService for use elsewhere? I assumed this as a given. Or do you mean something else?

    * Should we identify where existing `[X VIOLATIONS]` take place to enroll them into an `ArchitectureGuard` Service?

    * Should we document *SOP*s for an `SOPGuard` sub-Service of the `ArchitectureGuard`? e.g raise `TypreError` if `ROOT` package has no `Service`.
    
    * How can we separate *Service Flow* from *Logic* [[ADR-004] Domain Package Anatomy](https://github.com/mnaatjes/oregon-trail-clone/issues/4)

3. Logical Entities:

    * Explain how `LogicEntity` is represented by the `Facade.module`. Does importlib.util allow you to access the `from...import` lines? If so, what is the return type? How can this be utilize?
    
    * Should we still create a dataclass called `LogicEntity` for ease of use?
    
    * Explain how the functions from `domain/{root,leaf}/<package-name>/logic.py` can result in a DX call of `wagon.Logic.calculate_speed(wagon)`?

4. Project Managment:

    * Should all `domain/{root,leaf}/<package-name>/__init__.py` files have `__all__` declared explicitly or is this value accessible via the module property of Facade?

5. Unanswered from Previous:

    * Where and how are we going to collect necessary properties and components from *Aggregate Root*s?

        * Are Services captured from the **Import** line, the `DomainContext.service` property, or the file `service.py`? - **Via `DomainContext.service` &rarr; `DomainManifest` linked *Service Provider* instance**
        * How is the `LogicEntity` captured from the `logic.py` file? What if there is no *Logic* needed? - **Via `Registrar`**

    * What would an `AggregateManigest` accomplish? Or is this the `DomainManifest` - `DiscoveryManifest`?

    * Where will the `PriorityGraph` be declared? Should this be a dataclass or a service? Will we have different types of Graph structures i.e. should we create a `BaseGraph` contract?

### Follow-up TODOs

1. Spec out the `DiscoveryManifest`

    * Base Contract
    * Integrated into `BaseScanner`
    * Implemented `DomainManifest` should link `Package` to instantiated `ServiceProvider`
    * Properties for `DiscoveryManifest` (Frozen Dataclass):
        * `unit`: The original DiscoveryUnit (e.g., the Package).
        * `facade`: The hydrated Facade (containing the module and __CONTEXT__).
        * `status`: An Enum (VALID, MALFORMED, IGNORED).

2. Aggregate Composition & SOPs

    * **Only `ROOT` Packages** need `service.py` file
    * Update `DomainContext` validation to reflect

3. `ArchitecturalPolice` Service

    * Create `ArchitecturalPolice` Service in `src/core/kernel`
    * Not a *Global* Service. *Runtime* Service
    * Analysis Tool AND **Boot-time** Validator; A **Service** and NOT a *Static* class
    * `ArchitectureGuard` contract `src/core/kernel/contracts/guard.py`
    * Associated Exceptions in `src/core/kernel/exceptions.py`
    * Target **Implementation Sections:** in `src/core/engine/kernel/police/guards/`
        - `HorizontalGuard` e.g. Roots cannit import Roots
        - `VerticalGuard` e.g. 
        - `AnatomyGuard` e.g. Records CANNOT have IDs
        - `CompositionGuard` e.g. verify all the 4-file set for Roots, 3 for others with 1 optional

4. Logical Entities

    * They are **Stateless Functions**
    * Use python `inspect` module to verify functions in `logic.py` are *Pure* e.g. argument Record and return a record
    * *Purity* means **Same output as input**
    * *Side-Effects* are checked via **Abstract Syntax Tree** looking for prohibited keywords, e.g. `open`, `with`, `print`, `requests`, `import os`
    * `LogicEntity` will be represented by `Facade.module` via use of `from . import logic as logic` 

5. Finalizing branch `feat/52-domain-scanner`:

**TODOs:**
* To `Facade` add `exports: List[str]` = captured from `module.__all__`
* To `Package` add `is_root:bool`, `is_leaf:bool`
* Refactor: `DomainScanner.scan()` to return `DomainManifest`

**Testing:**
* *Scanner and Associated entities/objects/classes:
    * `BaseScanner`, `DomainScanner`
    * `DiscoveryUnit`, `Package`, `Facade`
* Scanning doesn't go deeper than `domain/{root,leaf}/<package-name>/__init__.py`
* Scanner stays within `key` e.g. `domain`
* Scanner fails appropriately
* Failure modes (`__init__.py` is empty)
* Verify `DomainManifest`