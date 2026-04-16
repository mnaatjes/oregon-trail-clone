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


### [ADR-00X: Title]
*   **Question/Presumption:** [Define what is being challenged or needs more detail]
*   **Analysis:** [Your thoughts and findings]
*   **Resolution/Action:** [e.g., "Accepted as is", "Drafting ADR Amendment", or "TDD will address this edge case"]
