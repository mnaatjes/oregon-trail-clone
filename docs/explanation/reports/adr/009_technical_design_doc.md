---
title: "Technical Design Documentation (TDD)"
description: "Formal adoption of TDD format and process"
type: "explanation"
status: "adopted"
created_at: "2026-04-16 04:24:00"
updated_at: "2026-04-17 15:00:00"
owner: "Michael Naatjes"
tags: ["adr", "tdd", "documentation"]
version: "0.1.0"
---

# Technical Design Documentation (TDD)

## Context

This Oregon Trail Clone need a Technical Design Document ruleset in the Design Workflow (from ADR to Implementation).

In the industry, these are most commonly referred to as Design Docs or RFCs (Request for Comments).
The Standard Template (The "Google" Pattern)

A professional TDD is not just a brain dump; it is a proposal meant for critique. The industry standard usually follows this structure:

## Decision

### 1. Document Composition

**Required TDD Categories**

* **Overview:** High-level summary

* **Goals:** What will this design accomplish? 

* **Design:** Detailed text and mermaid diagram explanation of component, data structures, etc.

**Full List of TDD Categories**

*Table illustrated major sections of TDD Documents*

| Section | Purpose |
| :--- | :--- |
| **Overview** | A high-level summary of the problem and the proposed solution. |
| **Context/Background** | Why are we doing this? (Links to ADRs). |
| **Goals & Non-Goals** | Crucial. Defines what the design will and will not do to prevent feature creep. |
| **Proposed Design** | The heart of the doc. High-level architecture and Mermaid diagrams. |
| **Detailed Design** | Class-level details, data structures, and state management. |
| **Alternatives Considered** | Why didn't you use a simpler or different pattern? |
| **Cross-Cutting Concerns** | Security, Observability (Logging), and Performance impacts. |

### 2. Design Section Contents

The Design section of a Technical Design Document (TDD) is where the abstract decisions from your ADRs meet the "cold, hard reality" of the code. If the ADR is the Constitution, the Design section of the TDD is the Engineering Blueprint.

It serves as the bridge that ensures your code doesn't just "work," but that it adheres to the strict architectural boundaries you've spent so much time defining.

1. **Proposed Architecture (High-Level)**

This sub-section focuses on the component's place in the ecosystem.

* **Component Diagram (C4 Level 3):** A Mermaid diagram showing how the domain interacts with other systems (e.g., how the Health leaf interacts with the Event Bus).

* **Dependency Graph:** A list of what this component is allowed to import (e.g., domain/common and core/contracts) and what it is strictly forbidden from touching.

2. **Detailed Design (Low-Level)**

This is where the actual engineering happens. It should include:

* **The Data Schema:** A definition of your Anemic Models. What fields are in the Record? What are the types?

* **The Interface/Contract:** The public methods of your Service and their signatures.

* **Sequence Diagrams:** A visual representation of a "Transaction." How does data flow from the Service → Logic → Model → Return?

* **State Management:** If the domain has state transitions (e.g., a "Character" moving from Healthy → Sick → Deceased), include a State Machine Diagram.

### 3. Role of the TDD in Design

The TDD isn't just "extra work"—it’s a diagnostic tool. It forces you to solve "invisible" coding problems before they become "unfixable" bugs. It aids in the design of:

1. **Edge Cases and "The Sad Path"**

While coding, we often focus on the "Happy Path" (everything working). The TDD forces you to design for failure:

* **Example:** What happens if the HealthLogic receives a negative damage value? * What happens if the InventoryRecord is full but receives a new item?

* **The TDD Result:** You design your validation and error-handling strategies before you type a single try/except block.

2. **Circular Dependency Avoidance**

This is critical for your Screaming MVC setup. By drawing the imports in the TDD, you’ll catch yourself trying to make the Health domain aware of the Wagon domain.

* **The TDD Result:** You realize you need a Protocol or an Event instead of a direct import.

3. **State Transitions and "Illegal" States**

A TDD helps you design the "Logic Gates" of your game.

* **Example:** Can a Character have 0 HP but still have the status Healthy?

* **The TDD Result:** You design the logic in logic.py to ensure that state changes are atomic and follow the "Metabolism" rules of the domain.

4. **Performance and Resource Bounds**

Even in a TUI game, you have to think about memory.

* **Example:** If the Weather domain updates every tick, does it create a new DTO every time or modify a reference?

* **The TDD Result:** You decide on using @dataclass(frozen=True) to ensure immutability and predictable memory usage.

### 4. Role in Design Workflow

1. ADR Document Created in `docs/explanation/reports/adr`

2. ADR Document Approved

3. [Optional] ADR integrated into `.context` for hydration

4. Draft TDD in `docs/explanation/design`

5. TDD Approved

6. Component Implemented

## Consequences

The TDD Ensures that a Component is fully developed and that edge-cases and other possible failure-points are solved for before implementation begins

## Status

**Adopted** 2026-04-16

## Addendum (2026-04-17)

### TDD Frontmatter Properties for Workflow Integration
To support the **Law of Provenance** and integration with the GitHub Project Metadata Ledger (as proposed in ADR-011), all TDD documents are now REQUIRED to include the following frontmatter properties:

*   **id**: (Required) Unique sequential identifier (e.g., `TDD-005`).
*   **parent_adr**: (Required) The ID of the ADR that authorized the design (e.g., `ADR-011`).
*   **title**: (Required) Clear, concise heading.
*   **status**: (Required) Current state of the design (e.g., `pending`, `stable`).
*   **feature_link**: (Required) URL to the corresponding GitHub Feature/User Story Issue.
*   **component**: (Required) The "Screaming" domain (e.g., `domain:health`, `core`, `engine`).