---
id: HT-CREATE-ISSUE
title: "How to Create GitHub Issues and Epics"
status: stable
created_at: 2026-04-18
updated_at: 2026-04-18
component: core
type: how-to
---

# How to Create GitHub Issues and Epics

In the Oregon Trail architecture, GitHub Issues are not merely "notes"—they are **legal contracts** for the code. Every issue must follow a standardized structure to ensure the **Law of Provenance** is maintained.

## 1. The Universal Header (Chain of Custody)

Every issue must begin with a **Reference Section**. This ensures that the "Why" (ADR) and the "What" (TDD) are always one click away from the "How" (the code).

**Note on Format:** This header MUST use **Markdown** (not YAML frontmatter) to ensure links are clickable and readable in the GitHub Web UI.

### Template
```markdown
## 🔗 Chain of Custody
- **ADR:** [ADR-XXX: Title](./path/to/adr.md)
- **TDD:** [TDD-XXX: Title](./path/to/tdd.md)
- **Component:** `Domain:Leaf (Name)`
```

---

## 2. Issue Categories & Templates

### A. The Epic Template (Strategic)
An Epic represents a major architectural decision (ADR-level). Its purpose is to track the completion of a full system or architectural shift.

*   **Overview:** High-level summary of the architectural requirement.
*   **Strategic Goals:** What the system gains from this change.
*   **Implementation Checklist:** A list of child Features/Tasks (e.g., `- [ ] #101`).
*   **Verification:** High-level criteria for closing the Epic.

### B. The Task Template (Tactical)
This is the "Work Order" for actual coding (TDD-level). It must be specific enough to pass the **Law of the Spec**.

*   **Description:** A concise explanation of the unit of work.
*   **Implementation Specs:**
    *   **Data Shape:** Link to the `models.py` contract in the TDD.
    *   **Logic Rules:** Bulleted "metabolism" rules (e.g., "HP cannot drop below 0").
*   **Acceptance Criteria (Definition of Done):**
    - [ ] Unit tests for `logic.py` pass.
    - [ ] `__init__.py` facade exports the new service.
    - [ ] Architectural Police checks pass.
*   **Technical Constraints:** Mention forbidden imports or required patterns (e.g., "Must use frozen dataclasses").

---

## 3. Automating with Issue Templates

To ensure consistency, store these templates in your repository at `.github/ISSUE_TEMPLATE/`.

### Example `task.md`
```markdown
---
name: Tactical Task
about: Use for TDD-level implementation tasks.
title: "[TASK]: "
labels: task
---

## 🔗 Chain of Custody
- **ADR:** [ADR-XXX]()
- **TDD:** [TDD-XXX]()
- **Component:** 

## 📝 Overview

## ✅ Acceptance Criteria
- [ ] Logic passes unit tests
- [ ] Architectural Police checks pass
- [ ] Facade updated
```

---

## 4. The Golden Rule of Drafting

**If an issue requires you to look at more than one TDD, it is too big.** 

Break the work down until each issue maps to a single, testable unit of your **Package Anatomy** (Model, Logic, or Service). This makes the **Law of Atomic PRs** much easier to follow.
