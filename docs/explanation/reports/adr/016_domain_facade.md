---
id: ADR-016
title: "Domain Package Facade SOP"
status: proposed
created_at: 2026-04-19
updated_at: 2026-04-19
component: core
type: "explanation/adr"
epic_link: https://github.com/mnaatjes/oregon-trail-clone/issues/45
---

# ADR-016: Domain Package Facade SOP

## Context
In a **Screaming MVC** architecture, the package (folder) is the "What." However, Python packages can easily leak internal implementation details if the `__init__.py` file is not strictly managed. 

To enable the **Automated Discovery System (ADR-014)** and maintain **Horizontal Isolation**, we need a Standard Operating Procedure (SOP) for the Domain Facade that ensures every package speaks with a consistent "Voice."

## Decision
We will enforce a strict structure for every `__init__.py` within `src/domain/`.

### 1. The Mandatory Manifest
Every package must declare a `__CONTEXT__` object using the **Type-Safe Manifest Strategy (TDD-002)**. This MUST be the first or primary export.

### 2. Strict Encapsulation (`__all__`)
To prevent "Guts Leakage," packages must explicitly define `__all__`. Only the following "Public" entities are permitted:
*   The `__CONTEXT__` manifest.
*   The primary **Service** class (The Actor).
*   The **Root** or **Record** model class (The Container).
*   The **Blueprint** class (The DNA).

### 3. Private Implementation
The following MUST remain private and excluded from `__all__`:
*   `logic.py` (Stateless metabolism).
*   Individual `breed` JSON loading logic.
*   Internal helper functions or transient DTOs.

## Implementation Example
```python
# src/domain/roots/wagon/__init__.py
from .context import __CONTEXT__
from .services import WagonService
from .models import WagonRoot, WagonBlueprint

__all__ = ["__CONTEXT__", "WagonService", "WagonRoot", "WagonBlueprint"]
```

## Consequences
- **Positive:** Guaranteed consistency for the Discovery Scanner.
- **Positive:** Prevents other pillars (UI/Engine) from accidentally coupling to internal `logic.py`.
- **Negative:** Requires a small amount of manual boilerplate in `__init__.py` (mitigated by its predictable nature).
- **Neutral:** Enforces a "Clean Air-Lock" between Domain packages.

## References
- [ADR-014: Automated Domain Discovery System](014_discovery_system.md)
- [TDD-002: DomainContext Contract](../../design/domain_context_contract.md)
- [ADR-005: Domain Model Taxonomy](005_domain_model_taxonomy.md)
