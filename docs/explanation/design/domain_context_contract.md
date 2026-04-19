---
id: TDD-002
parent_adr: ADR-003
title: "TDD: DomainContext Contract"
status: pending
created_at: 2026-04-17
updated_at: 2026-04-19
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/13
---

# TDD: DomainContext Contract

## 1. Overview
The `DomainContext` is the **Unified Context Manifest**. Every package in `src/domain/` must instantiate this object in its `__init__.py` as `__CONTEXT__`. 

By passing the actual **Blueprint** or **Spore** class as the `intent`, the manifest becomes a type-safe "DNA Sample" that the Engine uses for Discovery and Bootstrapping.

## 2. Goals & Non-Goals
### Goals
*   **Type-Safe Discovery:** Use class references instead of loose strings to identify domain intent.
*   **Auto-Bubbling:** Automatically derive `DomainFamily` and `Species` from the intent class.
*   **Zero-Boilerplate:** Eliminate redundant string declarations across the package.
*   **Validation:** Enforce architectural rules (e.g., ROOT packages must provide a Service) at the code level.

## 3. Proposed Design

### Data Schema (Core Fields)
The manifest no longer requires a `family` property, as it is derived from the `intent` class.

| Property | Type | Role |
| :--- | :--- | :--- |
| **`intent`** | `Type[DomainBlueprint] | Type[DomainSpore]` | The structural definition (The Class). |
| **`priority`** | `int` (0-100) | Sequential boot order (lower = earlier). |
| **`requirements`**| `List[KernelSubsystem]` | Kernel services needed for injection. |
| **`service`** | `Type[Any] | None` | The operator (Required if `intent` is a `RootBlueprint`). |

### Derived Properties (Logic)
The `DomainContext` provides helper properties for the Engine:
*   **`family`**: Returns `self.intent.family` (ROOT, LEAF, or SPORE).
*   **`species`**: Derived from `self.intent.__name__` or an explicit species property.

### Package Integration Example
```python
# src/domain/roots/wagon/__init__.py
from .models import WagonBlueprint, WagonRoot
from .services import WagonService

__CONTEXT__ = DomainContext(
    intent=WagonBlueprint,  # The Class IS the intent
    priority=10,
    service=WagonService
)
```

## 4. Diagnostic Goals
*   **Type Match Audit:** Verify that `intent` inherits from `DomainBlueprint` or `DomainSpore`.
*   **Service Guard:** Raise a `TypeError` if a ROOT family intent is provided without a `service`.
*   **Requirement Integrity:** Ensure all listed `requirements` are available in the `KernelSubsystem` registry.
