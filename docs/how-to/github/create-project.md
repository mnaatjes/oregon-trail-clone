---
id: HT-CREATE-PROJECT
title: "How to Create and Configure the GitHub Project Ledger"
status: stable
created_at: 2026-04-18
updated_at: 2026-04-18
component: core
type: how-to
---

# How to Create and Configure the GitHub Project Ledger

This guide details how to set up the GitHub Project (v2) to act as the authoritative metadata ledger for the Oregon Trail architecture.

## 1. Create the Project Board
1. In the GitHub Web UI, go to your **Profile** or **Organization** (wherever the repo is hosted).
2. Click the **Projects** tab (the one at the top level, next to 'Repositories').
3. Click **New project**.
4. Select the **Table** template (this is the "Table View" required by ADR-011 for metadata auditing).
5. Name it: `Oregon Trail Project`.

## 2. Link the Project to your Repo
1. Inside your new project, click the **Settings** (bottom of the left sidebar or the `...` menu).
2. Under **Linked repositories**, add your `oregon_trail` repository. This allows you to pull issues and PRs into the board.

## 3. Add the "Architectural Ledger" Fields (Crucial)
To follow the Law of Provenance, you must add custom columns to this project board. These columns turn a simple task list into a "Chain of Custody" ledger:

1. Click the `+` icon at the far right of the table headers.
2. Select **New field**.
3. Add the following fields:

| Field Name | Type | Options / Purpose |
| :--- | :--- | :--- |
| **ADR Link** | Text | URL to the parent ADR document in the repository. |
| **TDD Link** | Text | URL to the parent TDD document in the repository. |
| **Type** | Single select | `Epic`, `Feature`, `Task` |
| **Component** | Single select | `Core`, `Engine`, `UI`, `Domain:Root`, `Domain:Leaf` |
