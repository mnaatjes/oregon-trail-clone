---
title: "TDD: Domain Service Entities"
description: "Engineering blueprint for orchestration and side-effect management within the domain layer."
type: "explanation"
status: "pending"
created_at: "2026-04-17 00:00:00"
updated_at: "2026-04-17 00:00:00"
owner: "Michael Naatjes"
tags: ["design", "service", "orchestration", "tdd"]
version: "0.1.0"
---

# TDD: Domain Service Entities

## 1. Overview
This document defines the implementation standards for `services.py` entities. Service entities represent the **"Nervous System"** or the **"General"** of a domain—the active orchestrators that coordinate state, logic, and side effects.

## 2. Goals & Non-Goals
### Goals
*   Provide a single, clear entry point for domain "Intent."
*   Encapsulate all side effects (I/O, Events).
*   Maintain "Snapshotability" by enforcing statelessness.

### Non-Goals
*   Containing complex mathematical rules (delegated to Logic).
*   Defining data structures (delegated to Models).
*   Directly rendering UI elements.

## 3. Proposed Design

### The "Operator" Pattern
Services act as the hands that hold the Logic Calculator. They understand the application context and manage the "Transaction" of changing state.

### Interaction Rules (Codified)
1.  **Orchestration:** Responsible for the lifecycle of a domain action: Fetch → Logic → Save → Notify.
2.  **Singleton Class:** Managed by the `ServiceContainer`.
3.  **No State Storage:** Forbidden from storing domain data in `self` (e.g., `self.wagon_health`).
4.  **Adapter Access:** Allowed to use dependency-injected adapters (Storage, Event Bus).
5.  **Public Interface:** The "Voice" of the domain; the only way for the Engine to enact change.
6.  **Sovereignty Rules:**
    *   **Roots:** Can emit public events.
    *   **Leaves:** Silent; restricted to internal coordination.

### Detailed Design

#### Orchestration Sequence
```mermaid
sequenceDiagram
    participant E as Engine
    participant S as Domain Service
    participant A as Storage Adapter
    participant L as Domain Logic
    participant B as Event Bus

    E->>S: enact_intent(id, context)
    S->>A: fetch_model(id)
    A-->>S: model_dto
    S->>L: calculate_transition(model_dto, context)
    L-->>S: new_model_dto
    S->>A: persist(new_model_dto)
    S->>B: emit_event(DomainChanged, new_model_dto)
    S-->>E: success_acknowledgment
```

#### Dependency Graph
*   **Allowed Imports:** `models.py`, `logic.py`, `src/core/contracts/`, `src/domain/common/`.
*   **Forbidden Imports:** Any sibling `services.py` (Horizontal Isolation).

## 4. Diagnostic Goals
*   **Circular Dependency Prevention:** Services must use **Protocols** or **Events** to communicate laterally. No direct imports of sibling services.
*   **Persistence Integrity:** Services must ensure that state is only persisted if the Logic transition was successful.

## 5. Cross-Cutting Concerns
*   **Observability:** Services should log major "Intent" shifts (e.g., `CharacterDied`, `TradeCompleted`).
*   **Error Handling:** Services must translate technical errors (e.g., `DiskFull`) into domain-appropriate responses or events.
