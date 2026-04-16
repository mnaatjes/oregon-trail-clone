---
title: "Hybrid Typing Strategy"
created_at: 2026-04-14
updated_at: 2026-04-15
status: pending
---

# ADR 003: Hybrid Typing Strategy (Structural vs. Nominal)

## Context
The Oregon Trail engine needs to support a ["Screaming" Architecture](./001_screaming_mvc.md) 

1. Strict data consistency must be defined and adhered to at the `core/` (Specification) and `engine/` (Controller Concern)

   * A **Common Identity** and **Validation** logic must be determined.

   * The [`domain/`](./002_domain_hierarchy.md) (Model Concern) must be ruled by **Contract Enforcement**

   * **Bootstrapping Logic** must be consistent

2. Architectural Dissonance must be removed
   * **Structural Typing** enforement in `DomainBinding` must be resolved - made to work - with **Normal Typing** `Base*` and Abstract (ABC) Class inheritance

   * It MUST be determined if both **Structural Typing** AND **Normal Typing** are necessary

   * Currently a *split-personality* implementation where domains are conceptually **pluggable adapters** (Structural) but implementationally **rigid extensions** of the core (Nominal), leading to potential friction


## Prerequisites

1. 

## Decision
We will adopt a **Hybrid Typing Strategy** that leverages the strengths of both systems in their appropriate layers:

1. **Use Structural Typing (Protocols) for the "Scream" (Inter-Pillar Communication):**
   - The "Borders" between the Engine Kernel, UI, and Domain Pillars will be Structural.
   - **Rationale**: This allows the Engine to stay agnostic of the Domain's identity. It only cares that the "Plug Shape" (the Protocol) matches.
   - **Example**: `DomainBinding` remains a `Protocol`.

2. **Use Nominal Typing (Inheritance) for the "Skeleton" (Intra-Pillar Consistency):**
   - The "Guts" and shared infrastructure inside the pillars will be Nominal.
   - **Rationale**: This guarantees shared behavior (e.g., UUIDs, timestamps, serialization) and provides a "Hard Guardrail" against passing incompatible data types that might happen to share a similar structure.
   - **Example**: `DomainEntity` remains a base class (`ABC`).

## Consequences

### Positive
- **True Plug-and-Play Architecture:** The Engine remains blissfully ignorant of domain inner workings. New domains can be added without modifying the Engine.
- **Data Integrity:** Guarantees that every entity follows the same rules for identity and validation.
- **Testing and Mocking:** Extremely easy to "mock" a Protocol for unit tests.
- **Professional Grade Engine:** Aligns with senior-level patterns used in complex engines by distinguishing between Behavioral Interfaces and Data Infrastructure.

### Negative / Trade-offs
- **Refined Zero-Dependency Policy:** Leaf domains (e.g., `src/domain/health/models.py`) must still depend on the Core Skeleton (`src/core/contracts/`). We accept "Skeleton Dependency" as a trade-off for "DNA Consistency."
- **Mypy Friction:** Developers will encounter "Terminal Conflicts" if an entity matches the structural shape but lacks the nominal inheritance. This is intentional and acts as a safety mechanism.

## Summary Table

| Goal | Best Pattern | Why? |
| :--- | :--- | :--- |
| **Zero-Dependency** | Structural | No need to import a parent class from another pillar. |
| **Screaming Intent** | Structural | The Domain defines its own shape; it isn't "muffled" by a base class. |
| **Data Consistency** | Nominal | Guarantees every Entity has a UUID, created_at, etc. |
| **Testing/Mocking** | Structural | Extremely easy to mock a Protocol for unit tests. |

## Final Recommendation
Keep `DomainBinding` as a **Protocol (Structural)**—the ultimate "Plug." Keep `DomainEntity` as a **Base Class (Nominal)**—the "Skeleton." This ensures the Engine handles "DNA" with Nominal typing and "Interactions" with Structural typing.

## Status

Pending