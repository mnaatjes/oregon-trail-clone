---
id: ADR-015
title: "Lazy-Loading Spore (Type) Registry"
status: proposed
created_at: 2026-04-19
updated_at: 2026-04-19
component: core
type: "explanation/adr"
epic_link: https://github.com/mnaatjes/oregon-trail-clone/issues/43
---

# ADR-015: Spore (Type) Registry

## Context
`DomainSpores` (Spores) are nomadic, immutable data vessels. Unlike `DomainRoots` (ROOT) which provide services and anchor contexts, Spores are identity-less atoms used for semantic typing (e.g., coordinates, money). 

To ensure clean dependency management and avoid global side-effects, we want to:
1. Avoid "magic" side-effects where importing a module alters global state.
2. Provide a central registry for the Engine to recognize these nomadic types for validation and serialization.
3. Ensure that registration is explicit, traceable, and easy to isolate during testing.

## Decision
We will implement an **Explicit Spore Type Registry**. Registration of `DomainSpore` types is a handled by the system orchestration layer, not the classes themselves.

1. **Explicit Registration:** Every `DomainSpore` must be registered with the `SporeRegistry` by an external orchestrator (e.g., the Discovery Scanner or a Service Provider).
2. **Orchestrated Discovery:** The Discovery Scanner (ADR-014) is responsible for identifying `DomainSpore` subclasses within domain packages and explicitly registering them during the bootstrap phase.
3. **Registry as a Passive Container:** The `SporeRegistry` remains a pure, passive container that holds type definitions. It does not contain any logic for finding or loading those types.

## Implementation Strategy
- **Base Class:** `DomainSpore` remains a "dumb" data structure, focusing only on identity purity guards and attribute validation.
- **Registry:** Resides in `src/core/registries/spore.py` as a specialized `BaseRegistry[Type[DomainSpore]]`.
- **Registration Flow:**
    - The **Discovery Scanner** scans a domain's `models.py`.
    - It identifies classes inheriting from `DomainSpore`.
    - It calls `spores.register(name, cls)` for each identified type.

## Consequences
- **Positive:** Explicit and predictable. No hidden "magic" happens on import.
- **Positive:** High testability. Registries can be easily cleared or mocked without worrying about module-level side-effects.
- **Positive:** Aligns with the "Zen of Python": Explicit is better than implicit.
- **Negative:** Requires an active discovery or registration step before types are available to the Engine.
- **Neutral:** Centralizes type management in the Engine's bootstrap sequence.
