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
1.  **Identify Need:** Recognize an architectural requirement or a change in the "Laws of Physics."
2.  **Draft ADR:** Create a new document in `docs/explanation/reports/adr/`.
3.  **Assign Identity:** Provide a unique `id` (e.g., `ADR-012`).
4.  **Sync PM:** Open a corresponding **Epic Issue** in the GitHub Project and link it via the `epic_link` frontmatter.

### Phase 2: Tactical Design (The TDD)
1.  **Draft Blueprint:** Once an ADR is "Adopted," create the technical design in `docs/explanation/design/`.
2.  **Link Parent:** Assign a unique `id` (e.g., `TDD-005`) and link it to the `parent_adr`.
3.  **Define Spec:** Complete the **Detailed Design** section with class signatures, data schemas, and diagrams.
4.  **Sync PM:** Open a **Feature Issue** (User Story) and link it via the `feature_link` frontmatter.

### Phase 3: Operational Task (The Issue)
1.  **Decompose Work:** Break the TDD down into atomic coding tasks (e.g., "Implement Record," "Implement Logic").
2.  **Create Tasks:** Open individual **GitHub Issues** for each task, "Parented" to the Feature/Epic on the Project Board.
3.  **Audit Links:** Ensure each issue contains the `TDD Link` and `ADR Link` in the GitHub Project custom fields.

### Phase 4: Implementation & Verification (The PR)
1.  **Branch:** Create a feature branch (e.g., `42-health-record-dataclass`).
2.  **Execute:** Implement the code strictly following the TDD spec.
3.  **Automate Closure:** Use the `Closes #42` keyword in the PR description to update the ledger.
4.  **Pass Police:** Ensure all **Architectural Police** tests pass in CI/CD.
5.  **Merge:** Finalize the work into `main`.

---

## 4. Compliance and Auditing

We utilize **GitHub Project Views** to monitor the workflow:
*   **The Roadmap View:** Tracks the strategic progression of ADRs.
*   **The Audit View:** A tabular view that flags any Issue missing a `TDD Link` or `ADR Link`. 

**If it is not in the Ledger, it does not exist.**
