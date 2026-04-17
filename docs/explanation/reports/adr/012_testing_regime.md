---
id: ADR-012
title: "Testing Regime and Fitness Functions"
status: proposed
created_at: 2026-04-17
updated_at: 2026-04-17
component: core
type: "explanation/adr"
epic_link: PENDING
---

# ADR 012: Testing Regime and Fitness Functions

## Context
The **Law of Verification** (ADR-011) requires that all code pass "Architectural Police" tests before being merged. However, we have not yet defined the infrastructure or the specific tiers of testing required to protect the **Screaming MVC** boundaries and the **Chain of Custody**.

Without a formalized regime, "Unit Testing" becomes an arbitrary exercise, and architectural drift (e.g., circular dependencies) goes undetected until the system fails.

## Decision

### 1. The Three Tiers of Verification
We adopt a three-tiered testing strategy to verify behavior, interaction, and structure.

| Tier | Tool | Target | Purpose |
| :--- | :--- | :--- | :--- |
| **Tier 1: Unit (Logic)** | `pytest` | `logic.py` | Verify the "Metabolism." Pure math, 100% coverage. |
| **Tier 2: Integration** | `pytest` | `services.py` | Verify the "Nervous System." Mock the Event Bus/Storage. |
| **Tier 3: Fitness Functions** | Custom CLI | `src/` & `docs/` | Verify the "Anatomy." Enforce isolation and provenance. |

### 2. The "Architectural Police" (Fitness Functions)
We will implement automated structural tests that treat the codebase as data. These tests will fail the build if the "Laws of the Trail" are violated:
*   **Isolation Test:** Scans `src/domain/leaves/` to ensure no Leaf package imports another Leaf.
*   **Anemic Test:** Verifies that no class in `models.py` contains business logic (methods other than `clone` or `validate`).
*   **Facade Test:** Ensures only items explicitly listed in `__all__` in `__init__.py` are accessible.
*   **Provenance Test:** (The "Police" Tool) Verifies the frontmatter IDs and links between ADRs and TDDs.

### 3. Mandatory PR Handshake
No Pull Request can be merged unless:
1.  **Coverage:** 100% of new `logic.py` functions are tested.
2.  **Regression:** All existing Tier 1 and 2 tests pass.
3.  **Compliance:** The Tier 3 Fitness Functions confirm zero architectural violations.

## Consequences

### Pros
*   **Automated Governance:** The AI or developer is physically unable to break the architecture.
*   **Deep Confidence:** Pure logic tests ensure the "Math of the Trail" is always correct.
*   **Ledger Integrity:** Documentation stays in perfect sync with code via automated frontmatter audits.

### Cons
*   **Initial Complexity:** Requires building the Tier 3 custom scanning logic.
*   **Friction:** High coverage requirements may slow down initial implementation of new domains.

## Status
**Proposed** 2026-04-17
