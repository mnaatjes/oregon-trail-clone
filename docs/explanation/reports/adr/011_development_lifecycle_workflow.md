---
id: ADR-011
title: "Development Lifecycle and Workflow"
status: adopted
created_at: 2026-04-17
updated_at: 2026-04-17
component: core
type: "explanation/adr"
epic_link: "PENDING"
---

# ADR 011: Development Lifecycle and Workflow

## Context
As the Oregon Trail clone grows in complexity, the risk of "Architectural Drift" increases. We require a rigorous, traceable workflow to ensure integrity.

## Decision
We enshrine the **Four Laws of Engineering** and the **Chain of Custody**.

### 1. The Four Laws
* Law of Provenance
* Law of the Spec
* Law of Atomic PRs
* Law of Verification

### 2. Tracking and Traceability
We utilize a **GitHub Project (v2)** as the authoritative metadata ledger, bridging the Documentation and Execution layers.

## Status
**Adopted** 2026-04-17

## Addendum: Fast-Track Policy (PENDING)
To prevent process fatigue for minor maintenance, we propose a "Fast-Track" policy for non-architectural fixes.
1.  **Criteria:** A fix is eligible ONLY if it does not change the external contract:
    *   No changes to `models.py` (No new fields, no type changes).
    *   No changes to `__init__.py` (No new exports).
    *   No changes to `services.py` method signatures.
2.  **Workflow:** Create a GitHub Issue labeled `type:fast-track`, branch using `fix/ISS-ID-slug`, and state in the PR description: "Fast-Track: No architectural changes."

## Addendum: Python CLI "Police" Tool (PENDING)
To prevent manual ledger desync, we propose the creation of a Python CLI utility located in `scripts/architectural_police.py`.
1.  **Responsibility:** Scan the `docs/` directory to verify the "Law of Provenance."
2.  **Features:** 
    *   **Uniqueness Audit:** Confirms no duplicate `id` values in frontmatter.
    *   **Provenance Check:** Verifies that every TDD's `parent_adr` exists.
    *   **Sequential Warning:** Alerts if numbering gaps are detected.
3.  **Execution:** Run locally via `python scripts/architectural_police.py` or automatically as a CI/CD build step.
