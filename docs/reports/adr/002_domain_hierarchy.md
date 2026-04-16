---
title: "Domain Heirarchy"
created_at: 2026-04-15
updated_at: 2026-04-15
status: presented
---

# ADR 002: Domain Hierarchy

The Oregon Trail Domain Level Architecture must be rationalized with Anti-Patterns and zones of Mutual-Exclusivity resolved.

## Context

1. The [*split personality*](./003_hybrid_typing_strategy.md) of domain (Model Concern) genesis and behavior must be resolved. The following is still undecided:

    * Are domains **pluggable adapters** requiring **Structured Typing** and therefore require a **Service Contract** `DomainBinding`?

    * Are domains **rigid extentions** of [**Normally Typed**](./004_normal_typing_strategy.md) `core/domain/contracts/`?

    * Which **Typing** will be adopted: [Normal](./004_normal_typing_strategy.md) or [Structural-Normal Hybrid](./003_hybrid_typing_strategy.md)?

2. The Domain (Model Concern) **Lexicon** is inconsistent and unclear. We must determine how to organize and name both Domain Contract Abstracts and their implementations and what their **Responsibilities** will be

    * Responsibilities of Domain Contracts `core/contracts/domain` and Domain Implementations is unclear:
    
    * What relationship - if any - will each `core/contracts/domain` have with the `Bootstrap` and `ServiceProviders`?

3. Address the following **Domain-Related Issues**:

    * Will be adopt an **Aggregate Root** domain architecture in which a cluster of associated objects is treated as a single unit for data changes. Is a `DomainEntity` the highest position in the heirerchy representing that `Package`

    * **Zero-Dependency Leaf Policy** Is it mutually exclusive with other decisions and can it be adopted?

    * **Anemic Domain Model**: (Logic IN Service/Package) Will we treat the Screaming-Model as a *Package* (the folder, e.g. `domain/character/`) as the Aggregate Root - instead of the Class (`CharacterClass`) itself. 

        - Allows for *Stateless* logic; therefore logic is decoupled from Stateful-Class/Object

        - Discoverability: Verbs are found IN the Folder `__init__.py`

        - Pure functions are easier to Unit Test

        - Shifts the definition of the **Aggrigate Root** FROM the Class/Object TO the *Package* `domain/<ar-package-name>/__init__.py`

        - Protect internal details and only expose the Package *facade* in `__init__.py`

    * **Domain Driven Model**: (Logic IN Entity) Will we use a *Rich Model*

        - Discoverability: Methods visable ON Object

        - Complexity: Objects become Fat

    * Determine if **Anemic Domain** and **Aggregate Root** are mutually-exclusive or cannot be adopted together? I.e. wanting a Domain Hierarchy of Aggregate Root entry-point but the lower sibling-domains to be *Anemic* with their logic/services contained within their own logic/services files: e.g. `domain/<root-name>/{sibling...}/logic.py`

4. **Testing Regime** must be refactored to conform to new decisions and be rationalized more thoroughly.

## Prerequisites

1. MVC and Screaming-MVC MUST be adopted, rules generated, and `context/` yml file synthesized for Agentic-Workflow

2. Determine if the architecture will enforce **Normal Typing** or **Structural-Normal Hybrid Typing**

## References

1. **Zero-Dependency Leaf** policy is *Mutually Exclusive to **Aggregate Root** policy

## Decision

1. Resolved *Split Personality* Typing as ___

2. Domain Concern **Responsibilities** and **Lexicon**:

    * Representing the **Model** Entity, Model, Value-Object, Blueprint, State(Object)

    * Representing the **Logic**: Logic, Services

    * Representing the **Infrastructure**: Registry, ServiceProvider, Binding

3. Agreement on **Domain Related Issues**: Structural and Relational:

    3.1. **Aggregate Root**: Adopted

    * Adopt Aggregate Root in favor of Zero-Dependency Leaf. `DomainEntity` (the Aggregate Root) renamed to `___` 
    
    * An Aggregate Root CANNOT be declared/defined WITHOUT a **Bounded Context**

    * AR becomes the *Facade* for the Bounded Context via **Encapsulation**

    3.2 **The Anatomy of the Anemic Aggregate Package**: Adopted

    * **The Model `domain/<package_name>/model.py`**: Represents the *state*; it just has no behavior - DTO/Entity. It is an immutable (or nearly immutable) @dataclass. It defines the structure of the data.It is *Anemic* because doesn't know how to change itself. It just sits there like a spreadsheet row.

    * **The Logic `domain/<package_name>/logic.py`**: A collection of Pure Functions - Domain Rules. These functions take a Model as input, perform math, and return a new version of the Model (or a modified one). They never touch the database, the network, or the file system. They are "stateless" math.

    * **The Service `domain/<package_name>/service.py`**: Serves as the Orchestrator - Application Service. In Python, a Module (the file itself) acts as a static namespace. However, to stay compatible with your ServiceContainer and Dependency Injection, you’ll likely use a standard class.It pulls data from the source, sends it to the Logic to be processed, and then saves the result. It coordinates the "Transaction" of a game event.

    * **The Facade `domain/<package_name>/__init__.py`**: This is the *Discovery* layer - Package / API. It selectively imports functions from the Service and Logic and makes them available at the package level. The *Scream* ensures that when the Engine types health.apply_damage(), it doesn’t care that the math is actually in logic.py and the coordination is in services.py.

    3.3 **Packages as Structural Siblings**: Adopted

    * The *Reality* is that all Packages / Anemic Aggregates are **Structural Siblings**; each is a *Facade*

    ```text
    src/domain/
    ├── health/                  <-- STANDALONE SIBLING
    │   ├── models.py            <-- HealthState (HP: 10)
    │   ├── logic.py             <-- apply_damage()
    │   └── service.py
    │
    └── character/               <-- AGGREGATE ROOT
        ├── models.py            <-- CharacterState (holds a HealthState)
        ├── logic.py             <-- apply_aging() (NEVER imports health.logic)
        └── service.py           <-- Coordinates Character-specific events
    ```

    * However, some Packages have a **Conceptual Hierarchy** over other packages. E.g. `Character` over `Health` or `Shop` over `Character(Storekeeper)`

    * Orchestration:

    ```mermaid
    graph TD
        %% The Physical Layer (Siblings)
        subgraph Sibling_Layer [src/domain/Siblings]
            Character[Character Package]
            Health[Health Package]
        end

        %% The Logical Layer (Engine as Bridge)
        Engine[Engine / Controller]
        
        %% The Execution Flow
        Engine -->| Pulls HealthState from| Character
        Engine -->| Passes HealthState to| Health
        Health -->| Returns New HealthState| Engine
        Engine -->| Updates| Character
    ```

4. Implement robust **Testing Regime** which checks-for architectural alignment and provides developer feedback

## Consequences

3. **Domain Related Issues**:

    * Use **Zero-Dependency Leaf** policy at the **Structural Sibling** level ONLY. Standalone packages CANNOT traverse siblings. Aggregate Roots CAN possess Standalone packages in their **Conceptual Hierarchy**

    * A **Bounded Context** MUST be defined with each **Aggregate Root**

    * Requires a formal **Package** structure for `__init__.py` which is capable of differentiating between a **Standalone Package** and an **Aggregate Root**. 

    * Requires a systemetized way of encoding / enforcing **Conceptual Hierarchy** and configuring for **Dependency Management** via **ServiceProviders**

**Hierarchy Enforcement**

### Positive

* Defined Scope of `domain` and its components

## Status: Presented