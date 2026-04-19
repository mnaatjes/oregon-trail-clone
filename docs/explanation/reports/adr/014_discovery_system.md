---
id: ADR-014
title: "Automated Domain Discovery System"
status: proposed
created_at: 2026-04-19
updated_at: 2026-04-19
component: engine
type: "explanation/adr"
epic_link: PENDING
---

# ADR-014: Automated Domain Discovery System

## Context
As the project grows, the number of Domain Packages (ROOT and LEAF) will increase. Manually registering each package in the Engine Orchestrator or Service Container is error-prone, violates "Screaming MVC" (where the folder should be the source of truth), and creates a bottleneck for developers.

## Decision
We will implement an automated **Discovery System** within the Engine. The Engine will reflectively scan the `src/domain/` directory at boot time to identify and register packages.

## Implementation Strategy
1.  **Reflection:** Use Python's `pkgutil` or `importlib` to walk the `src/domain/` sub-directories.
2.  **Manifest Identification:** A directory is recognized as a valid Domain Package ONLY if its `__init__.py` contains a `DomainContext` instance assigned to `__CONTEXT__`.
3.  **Registration Sequence:**
    - Collect all `__CONTEXT__` objects.
    - Sort by `priority` (0-100).
    - Validate that all `requirements` (Kernel Subsystems) are available.
    - Instantiate the package's `service` (if applicable) and register it in the `ServiceContainer`.

## Consequences
- **Positive:** New domains are "plug-and-play." Developers only need to create the folder and `__init__.py`.
- **Positive:** Strong enforcement of architectural rules (e.g., failing boot if a `ROOT` package lacks a manifest).
- **Negative:** Minor boot-time overhead due to filesystem scanning (negligible for this project size).
- **Neutral:** Requires strict adherence to the `__CONTEXT__` naming convention.
