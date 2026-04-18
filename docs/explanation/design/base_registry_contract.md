---
id: TDD-012
parent_adr: ADR-003
title: "TDD: Universal BaseRegistry (Lean)"
status: draft
created_at: 2026-04-18
updated_at: 2026-04-18
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/31
---

# TDD: Universal BaseRegistry (Lean)

## 1. Overview
The `BaseRegistry` is a foundational utility designed to provide a standardized, type-safe mechanism for storing and retrieving objects via unique string keys. This "Lean" version prioritizes **Explicit over Implicit** and ensures strict adherence to the **Single Responsibility Principle (SRP)** by decoupling the stored items from the registry's storage logic.

## 2. Goals & Non-Goals

### Goals
*   **Zero Coupling**: Items do not need to "know" they are being registered (no Protocols or specific properties required).
*   **Total Serializability**: Enforce `str` keys to ensure compatibility with JSON-based world snapshotting.
*   **Type Safety**: Leverage `Generic[T]` and `TypeVar` to provide full IDE support.
*   **Explicit Registration**: The caller is responsible for providing the key, ensuring clear provenance of data.

### Non-Goals
*   Automatic key discovery (Duck Typing).
*   Managing the lifecycle of registered objects.

## 3. Proposed Design

### Type Definitions
*   **`RegistryKey`**: A `TypeAlias` for `str`.
*   **`T`**: A generic `TypeVar` representing any object type.

### Core Class: `BaseRegistry[Generic[T]]`
The registry maintains an internal `Dict[RegistryKey, T]`.

#### Methods:
| Method | Signature | Responsibility |
| :--- | :--- | :--- |
| `register` | `(key: RegistryKey, item: T)` | Adds an item to the map. Key is mandatory. |
| `get` | `(key: RegistryKey) -> Optional[T]` | Retrieves an item by key. |
| `all` | `() -> Dict[RegistryKey, T]` | Returns the internal mapping. |
| `exists` | `(key: RegistryKey) -> bool` | Checks for key existence. |

## 4. Rationale for Change
Previous designs using `typing.Protocol` forced items to be "self-aware" of their registration status. This violated SRP and introduced unnecessary complexity. The Lean strategy ensures the Item focuses on **State**, the Registry focuses on **Storage**, and the Provider focuses on **Orchestration**.
