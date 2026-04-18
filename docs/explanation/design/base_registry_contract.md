---
id: TDD-008
parent_adr: ADR-003
title: "TDD: Universal BaseRegistry"
status: draft
created_at: 2026-04-18
updated_at: 2026-04-18
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/31
---

# TDD: Universal BaseRegistry

## 1. Overview
The `BaseRegistry` is a foundational utility designed to provide a standardized, type-safe mechanism for storing and retrieving objects via unique string keys. By utilizing Python's `typing.Protocol`, it allows for "Static Duck Typing," ensuring that disparate parts of the system (UI, Domain, Engine) can be managed via consistent registry patterns without being forced into a rigid inheritance hierarchy.

## 2. Goals & Non-Goals

### Goals
*   **Total Serializability**: Enforce `str` keys to ensure compatibility with JSON-based world snapshotting.
*   **Type Safety**: Leverage `Generic[T]` and `TypeVar` to provide full IDE support and static analysis.
*   **Horizontal Isolation**: Use `Protocols` to allow registration without requiring items to inherit from a "Core" base class.
*   **Flexibility**: Support both automatic key discovery (via protocol) and explicit key assignment.

### Non-Goals
*   Managing the lifecycle of registered objects (creation/destruction).
*   Implementing persistence or I/O logic (delegated to specialized registries or providers).

## 3. Proposed Design

### Type Definitions
*   **`RegistryKey`**: A `TypeAlias` for `str`.
*   **`RegistryItem`**: A `typing.Protocol` requiring a `registry_key` property.
*   **`T`**: A `TypeVar` bound to `RegistryItem` for type-safe registry operations.

### Core Class: `BaseRegistry[T]`
The registry will maintain an internal `Dict[RegistryKey, T]` to store items.

#### Methods:
| Method | Signature | Responsibility |
| :--- | :--- | :--- |
| `register` | `(item: T, key: Optional[RegistryKey] = None)` | Adds an item. Uses `item.registry_key` if `key` is not provided. |
| `get` | `(key: RegistryKey) -> Optional[T]` | Retrieves an item by key. Returns `None` if not found. |
| `all` | `() -> Dict[RegistryKey, T]` | Returns a mapping of all registered items. |
| `exists` | `(key: RegistryKey) -> bool` | Checks if a key is currently registered. |
| `remove` | `(key: RegistryKey)` | Removes an item from the registry. |

### Logic Flow (Registration)
1.  If an explicit `key` is provided, use it as the dictionary key.
2.  If no `key` is provided, attempt to access `item.registry_key`.
3.  If neither is available, raise a `ValueError` to prevent "silent failures" in the registry.

## 4. Diagnostic Goals
*   **Identity Collision**: The registry should optionally support "overwrite protection" or logging when a key is re-registered.
*   **Protocol Verification**: Use `@runtime_checkable` on the `RegistryItem` protocol to allow for `isinstance()` checks during registration for extra safety.
*   **Serialization Check**: Ensure that all keys stored are valid strings that do not break `json.dumps`.

## 5. Alternatives Considered
*   **Inheritance-based Registry**: Rejected as it violates the principle of Horizontal Isolation by forcing all registry-ready items to inherit from a common Core class.
*   **Non-string Keys**: Rejected to maintain strict adherence to ADR-003's requirement for 100% serializable state.
