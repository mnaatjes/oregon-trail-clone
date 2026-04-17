---
id: EXP-WORKFLOW
title: "Development Lifecycle and Workflow Philosophy"
status: stable
created_at: 2026-04-17
updated_at: 2026-04-17
component: core
type: explanation
---

# Development Lifecycle and Workflow

This document explains the philosophy and mechanics of the Oregon Trail development process. It defines how we move from a strategic architectural decision to a verified line of code in the `src/` directory.

## The "Screaming" Engineering Philosophy

In a **Screaming MVC** architecture, the code must never outpace the design. Every component exists for a reason, and every reason must be documented. We utilize a **Chain of Custody** to ensure that "Dark Matter" code—code without a traceable origin—is never introduced into the system.

---

## 1. The Four Laws of the Trail

To maintain architectural integrity, every contributor must adhere to these four fundamental laws:

### I. The Law of Provenance
**No code enters the `src/` directory unless it can be traced back to an Issue, which traces back to a TDD, which traces back to an ADR.**
*   **Why:** To ensure every feature is intentional and authorized.
*   **Verification:** Automated "Architectural Police" tests verify the `id` and `parent_adr` links in documentation and pull requests.

### II. The Law of the Spec
**A TDD is considered "Done" only when its Detailed Design contains enough information for an LLM or another developer to write the implementation stubs without asking clarifying questions.**
*   **Why:** To eliminate ambiguity during the execution phase and enable autonomous implementation.

### III. The Law of Atomic PRs
**One Issue = One Branch = One Pull Request.**
*   **Why:** To prevent feature creep and ensure that reviews are focused and manageable. Never mix unrelated systems (e.g., "Weather" and "Health") in a single PR.

### IV. The Law of Verification
**Every PR must pass the "Architectural Police" tests (Taxonomy, Ontology, and Isolation checks) before being merged into `main`.**
*   **Why:** To enforce the physical boundaries of the architecture automatically.

---

## 2. The Hierarchy: Documentation vs. Project Management

We decouple the **Documentation Layer** (The Specification) from the **Project Management Layer** (The Execution) to maintain a single source of truth while allowing for flexible scheduling.

| Documentation Layer | Project Management Layer | Scale | Responsibility |
| :--- | :--- | :--- | :--- |
| **ADR** | **Epic** | Large / Strategic | "We will use an Event Bus for interaction." |
| **TDD** | **User Story / Feature** | Medium / Tactical | "The Health Domain must handle damage events." |
| **Contract Spec** | **Issue / Task** | Small / Operational | "Create the HealthRecord dataclass." |

---

## 3. Step-by-Step Workflow

### Phase 1: Strategic Decision (The ADR)
**Guide:** [How to Create an ADR](../how-to/development-lifecycle/create-adr.md)

1.  **Identify Need:** Recognize an architectural requirement or a change in the "Laws of Physics."
2.  **Draft ADR:** Create a new document in `docs/explanation/reports/adr/`.
3.  **Assign Identity:** Provide a unique `id` (e.g., `ADR-012`).
4.  **Sync PM:** Open a corresponding **Epic Issue** in the GitHub Project and link it via the `epic_link` frontmatter.

### Phase 2: Tactical Design (The TDD)
**Guide:** [How to Draft a TDD](../how-to/development-lifecycle/draft-tdd.md)

1.  **Draft Blueprint:** Once an ADR is "Adopted," create the technical design in `docs/explanation/design/`.
2.  **Link Parent:** Assign a unique `id` (e.g., `TDD-005`) and link it to the `parent_adr`.
3.  **Define Spec:** Complete the **Detailed Design** section with class signatures, data schemas, and diagrams.
4.  **Sync PM:** Open a **Feature Issue** (User Story) and link it via the `feature_link` frontmatter.

### Phase 3: Operational Task (The Issue)
**Guide:** [How to Manage GitHub Issues](../how-to/development-lifecycle/manage-github-issues.md)

1.  **Decompose Work:** Break the TDD down into atomic coding tasks (e.g., "Implement Record," "Implement Logic").
2.  **Create Tasks:** Open individual **GitHub Issues** for each task, "Parented" to the Feature/Epic on the Project Board.
3.  **Audit Links:** Ensure each issue contains the `TDD Link` and `ADR Link` in the GitHub Project custom fields.

### Phase 4: Implementation & Verification (The PR)
**Guide:** [How to Implement and Verify a Feature](../how-to/development-lifecycle/implement-and-verify.md)

1.  **Branch:** Create a feature branch using the mandatory naming convention (See Section 4).
2.  **Execute:** Implement the code strictly following the TDD spec.
3.  **Automate Closure:** Use the `Closes #ISS-ID` keyword in the PR description to update the ledger.
4.  **Pass Police:** Ensure all **Architectural Police** tests pass in CI/CD.
5.  **Merge:** Finalize the work into `main` via the Squash and Merge strategy.

---

## 4. Git & GitHub Strategy (The Ledger in Motion)
**Guide:** [How to Use Git and GitHub Conventions](../how-to/development-lifecycle/git-conventions.md)

To maintain the integrity of the "Law of Provenance," our Git strategy must be as disciplined as the architecture itself. Git serves as the physical implementation of our Ledger.

### 4.1 Branch Naming Conventions
To conform to the Law of Atomic PRs, branch names must be machine-readable and explicitly linked to the Project Management Layer.

**Pattern:** `type/ISS-#-short-description`

| Type | Name | Purpose | Example |
| :--- | :--- | :--- | :--- |
| **feat/** | Feature | New domain logic, services, or models (TDD-driven). | `feat/102-health-metabolism` |
| **fix/** | Bug Fix | Resolution of identified bugs or logic errors. | `fix/205-inventory-overflow` |
| **docs/** | Documentation | ADR drafting, TDD updates, or guide revisions. | `docs/ADR-013-event-schema` |
| **refactor/** | Refactor | Structural code changes without logic shifts. | `refactor/core-di-container` |
| **police/** | Police | CI/CD updates, Linter rules, or Fitness Functions. | `police/linting-rules` |

### 4.2 When to Create a Branch
The "Law of Provenance" dictates that a branch is a realization of an Issue.
*   **Trigger:** Create a branch ONLY when an Issue is moved to **In Progress** on the GitHub Project Ledger.
*   **Origin:** Always branch from a clean, updated `main`.
*   **Scope:** If you need to change code outside the scope of the current Issue, **STOP**. Create a new Issue, a new TDD (if necessary), and a new branch. No "While I'm at it" commits.

### 4.3 The Commit Message "Handshake"
Commit messages are the "DNA" of our provenance. We adopt the **Conventional Commits** standard, modified to include Issue IDs.

**Standard Format:** `type(component): description (#ISS-ID)`
*   **Bad:** `fixed health bug`
*   **Good:** `feat(health): implement damage metabolism logic (#102)`

### 4.4 The Forbidden List (Prohibited Actions)
The following actions are strictly prohibited in the `src/` and `docs/` directories:
*   **Committing Directly to `main`**: `main` is a protected branch. All code must pass through a Pull Request.
*   **"Littering" Commits**: Do not merge multiple issues into one branch.
*   **Force Pushing to Shared Branches**: Never push `--force` on `main` or active collaborative branches.
*   **Ghost Commits**: Commits without an Issue ID reference (#ISS-ID) violate the Law of Provenance.

### 4.5 The PR & Merge Strategy
To keep the Ledger clean, we use the **Squash and Merge** strategy.
*   **Atomic Commits:** Commit often during development (e.g., `added model`, `added logic`).
*   **The Squash:** When the PR is merged, GitHub squashes those into one clean, high-level commit.
*   **The Metadata:** The final merge commit message must contain the Issue ID and a link to the TDD.

### 4.6 Architectural Police in Git
Local enforcement can be implemented using Git Hooks (`.git/hooks/pre-push`):

```bash
#!/bin/bash
# Example logic for Architectural Police Hook
branch_name=$(git symbolic-ref --short HEAD)

if [[ ! $branch_name =~ ^(feat|fix|docs|refactor|police)/[0-9]+-.* ]]; then
    echo "❌ ERROR: Branch name must follow 'type/ISS-ID-slug' convention."
    exit 1
fi
```

---

## 5. Summary of the Git Lifecycle

1.  Fetch the latest `main`.
2.  Branch using the `type/ISS-ID-slug` format.
3.  Commit using Issue ID references.
4.  Push and open a PR.
5.  Verify via the CI "Architectural Police."
6.  Merge via Squash and Merge, automatically closing the Issue in the Ledger.

---

## 6. Compliance and Auditing

We utilize **GitHub Project Views** to monitor the workflow:
*   **The Roadmap View:** Tracks the strategic progression of ADRs.
*   **The Audit View:** A tabular view that flags any Issue missing a `TDD Link` or `ADR Link`. 

**If it is not in the Ledger, it does not exist.**
