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
│   │   ├── contracts/      # ABCs & Protocols (The Specification)
│   │   │   ├── provider.py # BaseServiceProvider ABC
│   │   │   ├── registry.py # BaseRegistry ABC
│   │   │   └── service.py  # BaseService ABC / Protocols
│   │   ├── container.py    # Service/Dependency Injection Container
│   │   └── events.py       # Global Event Bus / Observer logic
│   ├── domain/             # THE HEART: Functional sub-systems (UDB Pattern)
│   │   ├── character/      # Character Identity & Stats package
│   │   │   ├── __init__.py # Public API for Character
│   │   │   ├── models.py   # Identity & Stats entities
│   │   │   └── logic.py    # Identity-based rules (e.g. Age calculation)
│   │   ├── health/         # Isolated Health & Malady package
│   │   │   ├── __init__.py # Public API for Health
│   │   │   ├── models.py   # HP & HealthState entities
│   │   │   ├── maladies.py # Disease, Injury, & MentalIllness logic
│   │   │   └── services.py # Resolution logic (Disease/Sanity resolvers)
│   │   └── wagon/          # Wagon & Inventory package (Future expansion)
│   ├── engine/             # MVC Controller: Orchestrates domain interactions
│   │   └── providers/      # Concrete implementations of core/contracts/
│   ├── storage/            # Infrastructure: JSON Repository/Persistence
├── ui/                 # MVC View: Textual-based TUI components
    └── main.py             # App entry point & Bootstrap loop
├── tests/                  # Test suites mirrored to src/ structure
│   ├── architecture/       # Meta-tests for Contract/Blueprint enforcement
│   ├── domain/
│   │   ├── character/
│   │   └── health/
├── pyproject.toml
└── requirements.txt

## Structural / Architectural Rules

### The "Pillar Mirroring" Pattern
To allow for parallel systems, we should adopt a pattern where each architectural layer (`src/core`, `src/engine`) mirrors the top-level pillars (`src/domain`, `src/ui`, `src/storage`).

*   **`src/core/`**: Reserved for "Specs" (Protocols, ABCs) and "Passive" components (Registries, DTOs).
*   **`src/engine/`**: Partitioned by pillar (e.g., `src/engine/domain/`) for active orchestration logic.
    *   **Rule**: Create `src/engine/domain/` and move domain-specific orchestration there.

```