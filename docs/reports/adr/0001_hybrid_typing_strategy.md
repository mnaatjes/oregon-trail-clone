# ADR 0001: Hybrid Typing Strategy (Structural vs. Nominal)

## Status
Accepted

## Context
The Oregon Trail engine requires both high modularity (to support a "Screaming" and "Plug-and-Play" architecture) and strict data consistency (to ensure all game objects share a common identity and validation logic). 

Initially, the project exhibited "Architectural Dissonance" by alternating between:
1. **Structural Typing (Protocols):** Used for `DomainBinding` to allow the Engine to interact with domains without importing them.
2. **Nominal Typing (Inheritance):** Used for `DomainEntity`, `BaseServiceProvider`, and `BaseRegistry` to enforce shared behavior and identity.

This created a "split-personality" implementation where domains were conceptually "pluggable adapters" (Structural) but implementationally "rigid extensions" of the core (Nominal), leading to potential friction in static analysis (mypy) and ambiguous boundary enforcement.

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
