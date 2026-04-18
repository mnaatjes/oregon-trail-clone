---
id: ADR-001
title: "Screaming MVC System Architecture"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-18
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/1"
---

# ADR 001: Screaming Model View Controller (MVC) Architecture

This is the foundational document for the entire system. It establishes the "Laws of Physics" that allow the Ecosystem, Ontology, and Anatomy to exist.

## Context

The Oregon Trail clone requires an architecture that is modular, highly testable, and "Screams" its intent. 

We must resolve the tension between traditional MVC and modern Hexagonal (Ports & Adapters) patterns to create a "Builder-friendly" environment.

1. MVC vs. Hexagonal (Ports & Adapters)

*We have determined that MVC and Hexagonal architectures are complementary, not mutually exclusive.*

* MVC serves as our Internal Organization Pattern. It separates our state (Model), our orchestration (Controller), and our output (View).

* Ports & Adapters serves as our Boundary Pattern. It protects the MVC core from "Outer World" noise like the filesystem, database, or terminal input.

2. The Definition of "Screaming"

A "Screaming Architecture" ensures that the folder structure reveals the Intent of the Game rather than the Framework used.

* **The Scope:** "Screaming" applies primarily to the Domain (Model). While the Engine and UI follow standard structural patterns, the domain/ directory is organized by Feature Slices (e.g., health, wagon, trading).

## Decision

### 1. Unified Architectural Lexicon

We adopt Screaming MVC as the primary pattern, mapped to the following directory structure:

| MVC Concern | Directory | Linux/DevOps Analogy | Responsibility |
| :--- | :--- | :--- | :--- |
| **THE SPEC** | `src/core/` | The `/etc/` / Kernel Specs | Contracts, DI, and Base Classes. |
| **THE MODEL** | `src/domain/` | The `/bin/` / Binaries | Screaming business logic and state. |
| **THE CONTROLLER** | `src/engine/` | The `init` / `systemd` | Orchestration, Events, and Bootstrapping. |
| **THE VIEW** | `src/ui/` | The `stdout` / TTY | Presentation and User Input. |

### 2. The "Screaming" Implementation (Facade Pattern)

To ensure the Domain "Screams" its intent without exposing internal complexity:

Each domain package (e.g., domain/roots/character) acts as a Sovereign Bounded Context.

* **Discovery:** The `__init__.py` file acts as a Facade. It "lifts" the important Verbs (Service methods) and Nouns (Model DTOs) to the top level.

* **Encapsulation:** The engine interacts only with the Facade. It never reaches into the internal logic.py or models.py sub-files directly.

### 3. Boundary Protection (The Adapters)

To maintain the purity of the Anemic Model, any interaction with the "Real World" (JSON files, Terminal IO) must happen via Adapters located in the engine/ or ui/ layers. The domain/ remains a "Pure Logic" zone.

## Consequences

### Positive

* **Instant Context:** A developer looking at the src/domain/ folder immediately sees the "Rules of the Trail" (Health, Wagon, Rations) rather than generic folders like models/.

* **High Testability:** The "Model" concern is decoupled from the UI and Persistence, allowing for 100% unit test coverage of game logic.

* **Linux Alignment:** The separation of "Specs" (Core) from "Execution" (Engine) mimics the clarity of a well-organized Linux filesystem.

### Negative

* **Initial Overhead:** Requires more boilerplate in the `__init__.py` files to maintain the Facade.

* **Conceptual Complexity:** Requires developers to understand the difference between the Internal Model and the External Adapter.

## Status

**Adopted** 2026-04-16
