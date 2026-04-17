---
title: "Project Workflow Philosophy"
description: "Understanding the ADR -> TDD -> Issue chain and the discipline of Screaming Engineering."
type: "explanation"
status: "stable"
created_at: "2026-04-17 00:00:00"
updated_at: "2026-04-17 00:00:00"
owner: "Michael Naatjes"
tags: ["workflow", "philosophy", "process", "diataxis"]
version: "0.1.0"
---

# Project Workflow: From Decision to Code

In this project, we do not write code "on the fly." Because we are building a system based on strict architectural boundaries (**Screaming MVC**), every file in the `src/` directory must have a clear "Pedigree." 

This document explains the philosophy behind the **Chain of Custody** that governs how we move from an idea to a working feature.

## The Philosophical Chain

### 1. The ADR: The "Why" (The Strategy)
Every major shift in the game's world—how characters move, how data is saved, or how the UI talks to the engine—begins as an **Architectural Decision Record (ADR)**. 
*   **Focus:** High-level strategy and "Laws of Physics."
*   **Analogy:** The Constitution of a country.

### 2. The Epic: The "What" (The Project)
Once a decision is made, it is assigned to an **Epic** in our project management. This is the container for the work.
*   **Focus:** Organization and scheduling.
*   **Analogy:** A major infrastructure project (e.g., "Build the Interstate Highway").

### 3. The TDD: The "How" (The Blueprint)
Before a developer touches the `src/` directory, they must draft a **Technical Design Document (TDD)**. 
*   **Focus:** Detailed data schemas, class signatures, and sequence diagrams.
*   **Analogy:** The blue-print for a specific bridge on that highway.
*   **The Golden Rule:** If an LLM or a junior developer cannot write the code stubs just by looking at the TDD, the TDD is not finished.

### 4. The Issue: The "Work" (The Task)
A TDD is broken down into small, bite-sized **Issues**. 
*   **Focus:** Atomic units of labor.
*   **Analogy:** Laying a single mile of asphalt.
*   **The Law:** One Issue = One Branch = One PR. We never mix tasks.

### 5. The Code: The "Result" (The Reality)
The code is the final realization of the chain. It is validated against the TDD and the ADR by the **Architectural Police** (automated tests).
*   **Focus:** Correctness and idiomatic quality.
*   **Analogy:** The finished road that cars can drive on.

## Why This Much Process?

The Oregon Trail is a game of survival, and so is software engineering. By following this chain, we ensure:
1.  **Intentionality:** We never build things "just in case."
2.  **Traceability:** If a bug appears in six months, we can trace it back to the exact TDD and ADR that caused it.
3.  **Consistency:** The "Screaming" architecture stays clear. The folder structure continues to tell the story of the game's intent, not the story of a developer's weekend experiment.

## Summary of the "Chain of Custody"

| Step | Entity | Action | Result |
| :--- | :--- | :--- | :--- |
| **1** | **ADR** | You decide on the "Metabolism" of the trail. | **Strategic Agreement** |
| **2** | **Epic** | You create a container titled "Metabolism System." | **Project Organization** |
| **3** | **TDD** | You map out the classes and logic for that system. | **Engineering Blueprint** |
| **4** | **Issues** | You break the TDD into 3-5 small coding tasks. | **Atomic Work Units** |
| **5** | **Code** | You write the Python files and link the PR to the Issues. | **The Game Feature** |
