---
id: ADR-011
title: "Development Lifecycle and Workflow"
status: adopted
created_at: 2026-04-17
updated_at: 2026-04-18
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

## Addendum (2026-04-18): Python CLI "Police" Tool (PENDING)
To prevent manual ledger desync, we propose the creation of a Python CLI utility located in `scripts/architectural_police.py`.

### 1. Role and Intended Use
Its primary role is Provenance Auditing and Structural Enforcement. It ensures that no "Dark Matter" (undocumented or untraced code/decisions) enters the repository.
*   **Documentation Audit:** Scans `docs/` to ensure every TDD has a valid parent ADR, and every ADR has a unique ID.
*   **Link Verification:** Checks for numbering gaps or broken references between design documents.
*   **Boundary Enforcement:** (Future) It could verify that files in `src/domain/leaves/` don't import from `src/domain/roots/`, enforcing the "Laws of Physics" defined in `architecture.yml`.

### 2. Where to Write the Code?
According to ADR-011, the tool should be located at:
*   `.scripts/architectural_police.py`

You would likely use the `argparse` or `click` library to create a CLI interface with subcommands like `audit-docs` or `check-boundaries`.

### 3. How to Test It?
Testing a policing tool requires a "Police for the Police":
*   **Unit Tests:** Create a test suite in `tests/unit/scripts/test_architectural_police.py`.
*   **Mock Filesystem:** Use `pytest` with a temporary directory (`tmp_path`) to generate "invalid" documentation structures (e.g., a TDD with a non-existent `parent_adr`) and assert that the tool correctly identifies and reports the failure.
*   **Snapshot Testing:** Ensure the output formatting remains clear and helpful for developers.

### 4. What will Trigger it?
It is triggered in three specific environments:
1.  **Local Manual:** Developers run `python scripts/architectural_police.py` before committing.
2.  **Git Hooks:** A pre-push or pre-commit hook (as suggested in `EXP-WORKFLOW`) can run a lightweight version of the scan.
3.  **CI/CD (GitHub Actions):** The most critical trigger. Every Pull Request must pass the "Police" check before the "Merge" button is enabled.

### 5. Why is it Recommended?
*   **Prevents Architectural Drift:** In a "Screaming MVC" system, the folder structure is the documentation. If someone adds a file that doesn't fit the taxonomy, the tool catches it instantly.
*   **Ensures the "Chain of Custody":** It automates the "Law of Provenance." Manually checking that every PR has a TDD and ADR link is tedious and error-prone; the tool makes it a hard requirement.
*   **Scalability:** As the project grows to dozens of domains, the "Police" tool acts as a tireless architect, ensuring the original vision (Screaming MVC) is maintained without the lead architect having to review every single line for structural compliance.
