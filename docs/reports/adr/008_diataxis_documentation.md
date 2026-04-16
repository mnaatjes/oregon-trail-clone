---
title: "Adoption of Diataxis Documentation"
description: "Formal adoption of the Diátaxis framework for project documentation to improve maintainability and onboarding."
type: "explanation"
status: "stable"
created_at: "2026-04-16 02:53:00"
updated_at: "2026-04-16 03:05:00"
owner: "Michael Naatjes"
tags: ["adr", "diataxis", "documentation"]
version: "0.1.0"
---

# ADR 009: Adoption of Diátaxis Documentation Framework

# Context

The Oregon Trail Clone project requires a robust documentation strategy to manage increasing complexity in backend game logic, state persistence, and deployment workflows. Without a formal structure, documentation risks becoming a disorganized collection of "readme" files, making it difficult for contributors to distinguish between step-by-step guides and deep architectural explanations.

The Diátaxis framework is selected to solve this by categorizing content into four distinct quadrants based on user needs: Tutorials (learning-oriented), How-to Guides (task-oriented), Explanation (understanding-oriented), and Reference (information-oriented).
Decision

### Organization 

All project documentation will be organized according to the Diátaxis framework.

* **Location:** All documentation will reside in the /docs directory of the repository.

* **Formatting:** Documents must be written in Markdown (.md).

* **Naming:** Files will use kebab-case and be descriptive (e.g., persistence-layer-logic.md).

* **Enforcement:** Documentation updates will be required for any "architecturally significant" changes as defined in the ADR process.

* **Archiving:** All depreciated documenation belongs in `docs/_archive/`. The frontmatter of documents moved to the archive MUST be updated to *depreciated*

### Frontmatter

Each document must contain the following five keys:

* **title:** A clear, concise heading for the page.

* **description:** A one-sentence summary (aids the "Skim-read" requirement of the ADR process).

* **type:** The Diátaxis quadrant (tutorial, how-to, explanation, reference).

* **status:** The maturity of the document (draft, stable, deprecated).

* **created_at:** The date of creation in YYYY-MM-DD H:I:S format.

* **updated_at:** The date of the last significant revision in YYYY-MM-DD H:I:S format.

* **owner:** The primary maintainer of the document.

* **tags:** A list of keywords for filtering (e.g., [backend, persistence, logic]).

* **version:** The version of the software this document currently describes.

## Consequences

**Clearer Onboarding:** New developers can follow specific Tutorials without getting lost in technical Reference data.

**Reduced Cognitive Load:** Separating "how-to" tasks from "why" explanations prevents cluttered files.

**Maintainability:** The directory structure provides a predictable location for every piece of information.

**Sample Directory Tree**

*The following structure demonstrates how the Oregon Trail Clone documentation is organized under this decision:*

```
docs/
├── _archive/                        # Old / Depreciated Documentation
├── tutorials/
│   ├── getting-started.md           # Setting up the dev environment
│   └── building-a-game-module.md    # Creating a simple "Random Event" module
├── how-to/
│   ├── deploy-to-staging.md         # CI/CD and server configuration
│   ├── configure-difficulty.md      # Adjusting JSON-based game constants
│   └── test-persistence-layer.md    # Running integration tests for SQLite/PostgreSQL
├── explanation/
│   ├── architecture/
│   │   ├── game-loop-design.md      # Why the loop is structured this way
│   │   └── state-machine-logic.md   # Handling travel vs. town states
│   └── terminology/
│       └── oregon-trail-terms.md    # Disambiguating "Fording," "Caulking," etc.
├── reference/
│   ├── api-endpoints.md             # REST API specification
│   ├── schema-definitions.md        # Database and JSON event schemas
│   └── cli-commands.md              # Documentation for custom bash management scripts
└── design/
    └── reports/
        └── adr/
```

## Status

**Approved** 2026-04-16