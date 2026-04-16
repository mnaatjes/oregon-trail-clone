# Architectural Status Report - 2026-04-15

## Executive Summary
An analysis of the `.context/`, `docs/explanation/engineering/`, and `src/` directories reveals a robust architectural vision (Hybrid MVC/Hexagonal with Anemic Domain Models) but identifies several critical contradictions in documentation and emerging implementation risks.

---

## 1. Mutually Exclusive Architectures & Patterns

The project intentionally favors specific patterns over their traditional counterparts:

### Anemic Domain Model vs. Rich Domain Model (DDD)
*   **Status:** Mutually Exclusive.
*   **Finding:** The project explicitly mandates an **Anemic Domain Model** (via `patterns.yml` and `domain_service_pattern.md`). Entities are "slim" dataclasses holding only structural validation. Logic is strictly separated into `logic.py` (pure functions) and `service.py` (coordination). This is the opposite of classic DDD, which advocates for "Rich" models where behavior lives with the data.

### Structural Typing vs. Nominal Typing
*   **Status:** Mutually Exclusive in Implementation.
*   **Finding:** The project employs a "split-personality" typing model. It relies on **Structural Typing** (`typing.Protocol`) for cross-system functional interactions but uses **Nominal Typing** (`abc.ABC`) for the core infrastructure.
*   **File Declarations:**
    *   **Structural Typing (Protocol):** `src/core/contracts/domain/binding.py` (Defines `DomainBinding` as a Protocol for pluggable orchestration).
    *   **Nominal Typing (Inheritance):** `src/core/contracts/domain/provider.py` (`BaseServiceProvider`), `src/core/contracts/domain/entity.py` (`DomainEntity`), and `src/core/contracts/domain/registry.py` (`BaseRegistry`).
*   **The Mutual Exclusivity:**
    *   Nominal typing (ABC/Inheritance) requires a **hard dependency**. A domain class must import and inherit from the contract class to be valid. This is "Typing by Identity."
    *   Structural typing (Protocol) requires only a **matching shape**. A domain class does not need to know the contract exists; it is valid if its methods match the signature. This is "Typing by Capability."
*   **The Conflict and Implications:**
    *   **Dependency Leakage:** While `DomainBinding` (Protocol) aims for a "Zero-Dependency" leaf policy, the fact that domain entities and registries *must* inherit from `DomainEntity` and `BaseRegistry` (Nominal) creates a mandatory dependency on `src/core/contracts/`.
    *   **Architectural Dissonance:** The system implies that domains are "pluggable adapters" (Structural), yet forces them to be "rigid extensions" of the core (Nominal). This will lead to conflicts in the terminal (e.g., mypy errors) if a developer attempts to use a "pure" structural adapter that hasn't inherited from the nominal base classes required by the Engine's orchestrator or registry loaders.
    *   **Fragile Decoupling:** The decoupling is only partial. If the nominal base classes in `core` change, every domain package is forced to update, undermining the primary benefit of the structural `Protocol` used in the binding layer.

### Hybrid Architecture (MVC + Hexagonal)
*   **Status:** Integrated but potentially confusing.
*   **Finding:** These are not exclusive here but are mapped 1:1. The **Engine** acts as both the **MVC Controller** and the **Hexagonal Core**. This requires high discipline to ensure the "Controller" logic (flow) doesn't leak into the "Core" logic (rules).

---

## 2. Identified Anti-Patterns & Contradictions

### The "Stateful Service" Contradiction (Critical)
*   **Anti-pattern:** Documentation drift/Conflicting requirements.
*   **Evidence:** `docs/.../domain_service_pattern.md` defines Services as **Stateful** ("The Hand: Stateful, Modifies models"), whereas `.context/patterns.yml` explicitly states "**Services should be stateless**; they receive Entities and return values."
*   **Risk:** If Services become stateful, the game state becomes fragmented between "Models" and "Services," making save/load functionality and temporal logic (rewinding/replaying) extremely difficult to implement.

### Service Locator vs. Dependency Injection
*   **Anti-pattern:** Service Locator.
*   **Finding:** While the `BaseServiceProvider` aims for DI, the `ServiceContainer` is accessible throughout the app. `domain_contract_specification.yml` states "Cross-Domain interaction MUST be brokered by the ... ServiceContainer." 
*   **Risk:** If services resolve dependencies from the container at runtime (rather than having them injected during the `boot` phase), the project falls into the **Service Locator anti-pattern**, hiding dependencies and making unit testing harder.

### Zero-Dependency Policy vs. Aggregate Roots
*   **Anti-pattern:** Ambiguous Boundary Enforcement.
*   **Finding:** The "Zero-Dependency Leaf Policy" prohibits domain packages from importing each other. However, `architecture.yml` defines the `Character` package as an **Aggregate Root** that "composes instances from leaf packages like health."
*   **Risk:** This creates a hierarchy where some domain packages are "more equal" than others. If `Character` imports `Health`, it is no longer uncoupled. This violates the "Universal Domain Blueprint" if the rule is applied inconsistently.

### Architectural Drift (File Structure)
*   **Finding:** Documentation (`domain_binding_strategy.md`) specifies that `provider.py` lives within the domain package (`src/domain/<package>/provider.py`). However, the actual file structure (and `architecture.yml`) places them in `src/engine/providers/`.
*   **Risk:** This suggests a drift where the **Engine** is beginning to "own" the domain wiring, potentially leading to a "God Object" or a monolithic orchestrator that knows too much about domain internals.
