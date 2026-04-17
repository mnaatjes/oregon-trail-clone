---
title: "ADR Review & Analysis"
description: "A living document for questioning, challenging, and seeking clarification on established Architectural Decision Records (ADRs)."
type: "explanation"
status: "draft"
created_at: "2026-04-16 05:25:00"
updated_at: "2026-04-16 05:25:00"
owner: "Michael Naatjes"
tags: ["architecture", "adr", "analysis"]
version: "0.1.0"
---

# ADR Review & Analysis

This document serves as a collaborative space for deep-diving into the project's Architectural Decision Records. The goal is to ensure that every "Law of Physics" established in the ADRs is robust, understood, and capable of withstanding critical scrutiny.

## Current Reviews

### [ADR-002: Domain Hierarchy]
*   **Question/Presumption:** `service.py` "are the Nervous System... and interact with the ServiceContainer"

*   **Analysis:** 

    1. Ensure that "interacts with ServiceContainer" DOES NOT imply that this is `domain/package/leaf/service.py` is a ServiceProvider

    2. As the Nervous System, does this make `service.py` responsible for `Event` propagation?

    3. Are services `Static`, `Singletons`, or does it not matter?

*   **Resolution/Action:**

    1. **Service vs Provider:** `services.py` contains the Singleton Actor; `providers.py` is the Kernel-level Factory. They are distinct.

    2. **Event Sovereignty:** Root Services are the only entities permitted to emit events to the Global Event Bus. Leaves remain silent.

    3. **Lifecycle:** Services are Stateless Singletons. They must not hold internal state to ensure 100% snapshotability of the anemic models they process.

    4. **Enforcement:** Addendum added to ADR 002, 004, and 007 to formalize these constraints.


### [ADR-002 Domain Hierarchy]

* **Question:** Given, "A Root (e.g., Shop) that requires another Root (e.g., Character) to perform a task will define a Structural Protocol." 
    1. Have we defined the properties and methods of the Structural Protocol?
    2. What form should the Structural Protocol take? - An Abstract Class (ABC) or something else?
    3. How should the Structural Protocol be implemented? - Inheritance? Adding the "(Protocol) keyword"? 

* **Resolution/Action:**
    1. **Form:** We use `typing.Protocol` (Static Duck Typing).
    2. **Implementation:** Inherit from `typing.Protocol` to define the contract. Implementing classes **do not** inherit from the Protocol; they simply implement the required methods/properties (Duck Typing).
    3. **Location:** Shared contracts live in `domain/common/contracts.py`; local contracts live at the top of the consuming Root's `services.py`.

### [ADR-002 Domain Hierarchy]

* **Question:** Given "Import Audit: Scans for illegal horizontal imports (Leaf-to-Leaf or Root-to-Root)"

    1. What is the best way to go about checking for illegal horizontal imports? Do you search the files themselves for "from...import" declarations? Do you use a directory scan with os or path modules? Other?

* **Resolution/Action:**
    1. **Mechanism:** Use Python's `ast` (Abstract Syntax Tree) module within a `pytest` suite.
    2. **Why:** AST parsing is more robust than string-based searching (regex) as it understands the structure of the code (imports, aliases, multiline).
    3. **Enforcement:** This will be implemented as a "Fitness Function" in the Architecture Testing Regime (Phase 2 TODO).

### [ADR-003 Anemic Aggregator]

* **Question:** Given, "An Aggregate Root is a DTO (Data Transfer Object) that acts as a container for a Bounded Context..."

    1. What part of the Aggregate Root in our implementation is the DTO? Is it the `DomainBlueprint` dataclass, or the Package as a whole? 

    2. We need to refine language from "Aggregate Root" (the Concept), Aggregate "Root" (a Root level Package), "Aggregate" Root (any package that is an aggregate of the files that make-it-up), etc. Are all Packages Aggregate Roots? 

    3. What properties or variables (and where) are used to define the Bounded Context of an Aggregate Root / Package?

* **Resolution/Action:**
    1. **The DTO:** The **`DomainRoot` subclass** found in `models.py` is the DTO. It is the passive data structure that anchors the UUID and aggregates other records. `DomainBlueprint` is a static template (Global Truth), not the stateful instance.
    2. **Species Distinction:**
        *   **Root Package:** The physical folder in `src/domain/roots/`.
        *   **Aggregate Root:** The DDD conceptual role.
        *   **DomainRoot:** The base class/contract for the Aggregate Root DTO.
        *   **Constraint:** ONLY Root Packages are Aggregate Roots. Leaf Packages are "Atoms" (Records) that are gathered by Roots.
    3. **Bounded Context Markers:** The Bounded Context is defined by:
        *   **Physical Boundary:** The package directory itself.
        *   **The Facade:** `__init__.py` defines the public API via `__all__`.
        *   **Behavioral Ontology:** Metadata variables like `__DOMAIN_INTENT__` and `__DOMAIN_SPECIES__` (ROOT vs LEAF) in `__init__.py` inform the Kernel of the context's nature.

### [ADR-003 Anemic Aggregator]
* **Created:** 2026-04-16 07:53:00
* **Question:** Given, "Every DomainRoot must possess a globally unique UUID." -> 

    1. What is the Service which will endow this UUID? 
    
    2. Or can this be a function of the Abstract Contract which it performs every time DomainRoot is inherited/implemented?

* **Resolution/Action:**
    1. **Endowment Responsibility:** Per the "Hydration Flow" in ADR 003, the **Domain Service** is responsible for generating the UUID and passing it to the `DomainRoot` during instantiation.
    2. **Contract Role:** The `DomainRoot` contract (ADR 002, ADR 005) ensures the *existence* of the identity field, but the service acts as the "General" that assigns it when a sovereign actor is born into the world.

### [ADR-003 Anemic Aggregator]
* **Created:** 2026-04-16 07:57:00
* **Question:** Re: `DomainRecord`

    1. What properties must ALL `DomainRecords` have?


    2. Where will `DomainRecords` get their values from? Are properties defined on an individual basis?

    3. Are `DomainRecord` entities meant to be hydrated from json files or by the internal logic of the Domain System? We have an Hydration Flow for Aggregate `DomainRoot`s but how are leaves - `DomainRecords` hydrated?

* **Resolution/Action:**
    1. **Baseline Properties:** Per ADR 005, all `DomainRecord`s are **Anonymous**, **Anemic**, **Cloneable**, and **Validatable**. They represent a passive "Row" of state.
    2. **Value Sourcing:** Properties are defined by the specific Leaf Package. Values are sourced from **Leaf Services** and **Logic** transformations.
    3. **Hydration Path:** `DomainRecord`s are hydrated by **Leaf Services** (ADR 003). They may be initialized from `DomainBlueprint` templates but are ultimately the result of the Leaf's internal metabolism (Logic).


### [ADR-004 Domain Package Anatomy]
* **Created:** 2026-04-16 11:31:00
* **Question:** Given "Services are Singletons/Stateless. They should NOT hold a specific CharacterState as an internal property; they should receive the state as a parameter, transform it via Logic, and return it. This prevents "Stale State" bugs across the ecosystem..."

    1. I want to know the difference between the contents of `logic.py` (Logic) and the contents of `service.py` (Services).

    2. What are the rules for Services and Logic: Who and/or What CAN they interact with and can they NOT interact with?

    3. What is the Scope of each: Logic and Service?

    4. What is the composition of each? Are all Services Singleton Classes? Should Services be static - why or why not? Does `logic.py` just contain a list of independent functions or an organized object?

    5. What capabilities do Services and Logic of `DomainRoot`s have vs `DomainRecord`s?

* **Resolution/Action:**
    1. **The "Calculator vs. Operator" Model:**
        *   **Logic (`logic.py`) is the Calculator:** Pure, stateless mathematical transformations. Input (Model) -> Output (New Model). No side effects (no I/O, no events).
        *   **Service (`services.py`) is the Operator:** The Orchestrator. It fetches the Model, invokes the Logic, saves the result, and emits events.
    2. **Interaction Boundaries:**
        *   **Encapsulation:** `logic.py` is private to its package. Outside packages (Horizontal Siblings) must never import `logic.py` directly; they must interact via the Package Service or Facade.
        *   **I/O Policy:** Only Services may interact with external systems (ServiceContainer, Databases, Event Bus). Logic must remain a "Pure Math" zone.
    3. **Composition:**
        *   **Services:** Stateless Singletons implemented as classes. They do not hold instance state to ensure snapshotability.
        *   **Logic:** A collection of independent, pure functions.
    4. **Sovereignty:**
        *   **Roots:** Root Services are the only entities permitted to emit public events.
        *   **Leaves:** Leaf Services must remain silent to the outside world.
    5. **Addendum Required:** Draft an addendum for ADR-004 to include these practical definitions and the "Litmus Test" for developers.

### [ADR-00X: Title]
*   **Question/Presumption:** [Define what is being challenged or needs more detail]
*   **Analysis:** [Your thoughts and findings]
*   **Resolution/Action:** [e.g., "Accepted as is", "Drafting ADR Amendment", or "TDD will address this edge case"]
