---
id: TDD-011
parent_adr: ADR-011
title: "TDD: Architectural Police Infrastructure"
status: pending
created_at: 2026-04-18
updated_at: 2026-04-18
component: core
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/22
---

# TDD: Architectural Police Infrastructure

## 1. Overview
The "Architectural Police" is the automated realization of the **Four Laws of Engineering**. This infrastructure provides three layers of enforcement:
1.  **Passive:** GitHub Templates (Issue/PR) to guide the developer.
2.  **Local:** Git Hooks (Bash) to prevent illegal branch names and ghost commits.
3.  **Core:** Python CLI Tool (`scripts/architectural_police.py`) to audit documentation and boundary isolation.

## 2. Goals & Non-Goals
### Goals
*   Automate the **Law of Provenance** verification.
*   Enforce **Boundary Isolation** (Leaf-to-Leaf isolation).
*   Prevent "Ghost Commits" (commits without Issue IDs).
*   Ensure every ADR has an Epic and every TDD has a Feature Issue.

### Non-Goals
*   Enforcing code style/linting (delegated to Ruff/Black).
*   Automating code fixes (the Police only report; the Developer resolves).

## 3. Proposed Design

### Layer 1: Passive Provenance (GitHub Templates)
Create `.github/ISSUE_TEMPLATE/` (Epic, Feature, Task) and `.github/PULL_REQUEST_TEMPLATE.md`.
*   **Reason:** Forces the developer to see and fill out the "Chain of Custody" header before work begins.

### Layer 2: Local Enforcement (Git Hooks)
Implement a `pre-push` hook to enforce naming conventions.
```bash
#!/bin/bash
branch_name=$(git symbolic-ref --short HEAD)
if [[ ! $branch_name =~ ^(feat|fix|docs|refactor|police)/[0-9]+-.* ]]; then
    echo "❌ ERROR: Branch name must follow 'type/ISS-ID-slug' convention."
    exit 1
fi
```

### Layer 3: The Audit Tool (`scripts/architectural_police.py`)
A Python CLI built with `argparse`.
*   **Command:** `audit-docs`: Scans `docs/` to ensure no `epic_link: PENDING` or `feature_link: PENDING` exists.
*   **Command:** `audit-boundaries`: Scans `src/domain/` to ensure Leaf packages do not import from other Leaves or Roots.
*   **Command:** `audit-ledger`: Uses the GitHub API (via `gh`) to ensure every row in the Project Ledger has a corresponding TDD/ADR link.

## 4. Diagnostic Goals
*   **Zero Drift:** The system should report 0 errors when all "Laws" are followed.
*   **CI Integration:** The tool must return exit code 1 on failure to block PR merges in GitHub Actions.

## 5. `ArchitecturalGuard` Service

* Create `ArchitecturalGuard` Service in `src/core/kernel`
* Not a *Global* Service. *Runtime* Service
* Analysis Tool AND **Boot-time** Validator; A **Service** and NOT a *Static* class
* `GuardUnit` contract `src/core/kernel/contracts/guard.py`
* Associated Exceptions in `src/core/kernel/exceptions.py`
* Target **Implementation Sections:** in `src/core/engine/kernel/police/guards/`
    - `HorizontalGuard` e.g. Roots cannit import Roots
    - `VerticalGuard` e.g. 
    - `AnatomyGuard` e.g. Records CANNOT have IDs
    - `CompositionGuard` e.g. verify all the 4-file set for Roots, 3 for others with 1 optional
    - `SOPGuard` e.g. check and enforce *Screaming* rules
* Find **Every** `[X VIOLATION]` and enroll it in the Service