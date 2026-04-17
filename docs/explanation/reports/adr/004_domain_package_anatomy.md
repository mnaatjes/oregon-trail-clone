---
id: ADR-004
title: "Domain Package Anatomy"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-17
component: core
type: "explanation/adr"
epic_link: "PENDING"
---

# ADR 004: Domain Package Anatomy

This ADR is the *Structural Blueprint* that ties the **Taxonomy** (WHAT things are) and the **Ontology** (HOW they sit in the world) into a physical folder structure. It is the most *Screaming* part of the architecture.

## Context

An Anatomy with strict definitions is necessary to explicitly maintain architecture patterns.

## Decision

### 1. The Standardized File Set
Every Domain Package (Leaf or Root) MUST contain the following four files. No more, no less.

| File | Analogy | Responsibility |
| :--- | :--- | :--- |
| `models.py` | The Resource | Anemic DTOs (Records/Blueprints). Zero logic. |
| `logic.py` | The Metabolism | Pure, stateless math. Transformation functions. |
| `services.py` | The Nervous System | Orchestration. Coordinates Models and Logic. |
| `__init__.py` | The Voice | The Facade. Lifts the intent to the Engine. |

### 2. The Logic vs. Service Addendum (Calculator vs. Operator)
* **`logic.py` (The Calculator):** Pure math. It takes a Model, does math, and returns a new Model. It has no "hands"; it cannot talk to the database or the event bus.
* **`services.py` (The Operator):** The orchestrator. It has "hands." It fetches the Model, gives it to Logic, and then "saves" or "emits" the result.

### 3. Facade Enforcement (`__all__`)
To prevent internal leakage, the `__init__.py` MUST use `__all__` to explicitly define which Nouns (Models) and Verbs (Services) are visible to the outside world.

## Consequences

### Positive
* **Predictability:** A developer knows exactly where to find the "math" vs the "data" in any package.
* **Linter Enforcement:** We can write automated tests to ensure no package is missing these four files.

## Status
**Adopted** 2026-04-16
