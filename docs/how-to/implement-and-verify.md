---
id: HT-IMPLEMENT-VERIFY
title: "How to Implement and Verify a Feature"
status: stable
created_at: 2026-04-17
updated_at: 2026-04-17
component: core
type: how-to
---

# How to Implement and Verify a Feature

Follow these steps to move from an issue to a verified line of code in the source tree.

## 1. Prepare the Environment
*   **Branch:** Create a new branch from `main` using the Issue ID and a short description:
    ```bash
    git checkout -b 42-health-record-dataclass
    ```

## 2. Execute the Implementation
*   **The Law:** Strictly follow the TDD's **Detailed Design**. 
*   **Constraint:** Do not perform unrelated refactoring. Stay focused on the atomic task.
*   **Test-First:** Draft a unit test that verifies the logic defined in the TDD.

## 3. Submit for Verification
1.  **Commit:** Use clear, concise commit messages.
2.  **Push:** `git push origin 42-health-record-dataclass`.
3.  **GitHub UI: Open Pull Request:**
    *   **Title:** Use the Issue ID (e.g., `Metabolism: Implement HealthRecord`).
    *   **Description:** Use the keyword `Closes #42` to automatically link the issue and update the project ledger.
    *   **Labels:** Add the `Architectural Police` label if applicable.

## 4. Finalize the Merge
*   **Verify CI:** Ensure all automated tests (Taxonomy, Isolation, etc.) pass.
*   **Merge:** Once checks pass, merge into `main` and delete the branch.
*   **Post-Check:** Verify the GitHub Project board shows the task as **Done**.
