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

# ADR-015: Lazy-Loading Spore (Type) Registry

## Context
`DomainValueObjects` (Spores) are nomadic, immutable data vessels that reside in `src/domain/common/`. Unlike `DomainRoots` (ROOT) which provide services and anchor contexts, Spores are identity-less atoms used for semantic typing (e.g., coordinates, money). 

To ensure high performance and clean dependency management, we want to:
1. Avoid "pre-booting" or registering Spores that are not in use.
2. Implement "Just-in-Time" (JIT) recognition of Spore types when a Root or Record imports them.
3. Allow the Engine to recognize these nomadic types for validation and serialization without manual registration.

## Decision
We will implement a **Spore Type Registry** using Python's `__init_subclass__` hook. 

1. **Implicit Registration:** Every class inheriting from `DomainValueObject` will automatically register its type definition with a global `SporeRegistry` the moment the class is defined (i.e., when the module is first imported).
2. **Lazy-Loading:** The Engine Orchestrator will not proactively scan `src/domain/common` for Spores. Instead, Spores are "discovered" when they are first referenced by a Root or Record's type hints.
3. **Type-Hint Discovery:** The Discovery Scanner (ADR-014) will inspect the properties of `DomainRoots` and `DomainRecords`. If it encounters a type belonging to the `SPORE` family, it will verify its registration in the `SporeRegistry`.

## Implementation Strategy
- **Base Class Hook:** Add `__init_subclass__` to `DomainValueObject` in `src/core/contracts/domain/value_object.py`.
- **Registry:** Resides in `src/core/contracts/registry.py` as a specialized `BaseRegistry[Type[DomainValueObject]]`.
- **Validation:** The Discovery Scanner ensures that all `SPORE` types used in a package are validly registered.

## Consequences
- **Positive:** Zero boot-time overhead for unused Spores.
- **Positive:** Automates the "Manual Registration" tax for developers.
- **Negative:** Registration happens as a side-effect of import, which can be less explicit than manual wiring.
- **Neutral:** Requires consistent use of type hints in Domain models.
