---
author: Michael Naatjes
email: michael.naatjes87@gmail.com
updated_at: 2026-04-12
---

# Oregon Trail Clone

## Directory Tree

```text
./
├── assets/                 # ASCII art text files (.txt, .ansi)
├── docs/                   # Architecture diagrams and design docs
│   └── domain_contract_spec.yml
├── src/
│   ├── core/               # Technical foundation & Framework rules
│   │   ├── kernel/         # Global Framework (The "System" Pillar)
│   │   │   ├── contracts/  # Global ABCs & Protocols (Events, DI, Registry)
│   │   │   └── ...
│   │   ├── domain/         # Domain-specific infrastructure
│   │   │   ├── contracts/  # Domain Protocols (Roots, Records, Spores)
│   │   │   ├── registries/ # Passive data stores (SporeRegistry, etc.)
│   │   │   └── providers/  # Domain Service Providers
│   │   └── container.py    # Service/Dependency Injection Container
│   ├── domain/             # THE MODEL: Pure Business Logic & State
│   │   ├── character/      # Character Identity & Stats package
│   │   ├── health/         # Isolated Health & Malady package
│   │   └── wagon/          # Wagon & Inventory package
│   ├── engine/             # THE CONTROLLER: Orchestration & Lifecycle
│   │   ├── domain/         # Active Domain Orchestration (Orchestrator, Registrar)
│   │   └── ...
│   ├── storage/            # THE ADAPTERS: Persistence (JSON/SQL)
│   ├── ui/                 # THE VIEW: Presentation & User Input
│   └── main.py             # App entry point & Bootstrap loop
├── tests/                  # Test suites mirrored to src/ structure
│   ├── architecture/       # Meta-tests for Contract/Blueprint enforcement
│   ├── unit/
│   │   ├── core/
│   │   └── domain/
│   └── integration/
├── pyproject.toml
└── requirements.txt

## Structural / Architectural Rules

### The "Pillar Mirroring" Pattern
To allow for parallel systems, each architectural layer (`src/core`, `src/engine`) MUST mirror the top-level pillars (`src/domain`, `src/ui`, `src/storage`).

*   **Pillar-First Organization**: The folder represents the "What" (Pillar), while the sub-folders or files represent the "How" (Role).
    *   **Formula**: `src/{layer}/{pillar}/{role}/` (e.g., `src/core/domain/contracts/`)
    *   *Correct*: `src/core/domain/contracts/`
    *   *Incorrect*: `src/core/contracts/domain/`
*   **`src/core/`**: Reserved for "Specs" (Protocols, ABCs) and "Passive" components (Registries, DTOs).
*   **`src/engine/`**: Reserved for "Active" components (Orchestrators, Registrars) that manage pillar lifecycles.
*   **Vertical Alignment Example**:
    *   **Spec**: `src/core/domain/contracts/root.py`
    *   **Model**: `src/domain/wagon/models.py`
    *   **Orchestration**: `src/engine/domain/orchestrator.py`

```