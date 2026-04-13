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
├── src/
│   ├── core/               # Technical foundation (Asset loaders, Event bus)
│   ├── domain/             # THE HEART: Functional sub-systems
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
│   ├── storage/            # Infrastructure: JSON Repository/Persistence
│   ├── ui/                 # MVC View: Textual-based TUI components
│   └── main.py             # App entry point & Dependency Injection
├── tests/                  # Test suites mirrored to src/ structure
│   ├── domain/
│   │   ├── character/
│   │   └── health/
├── pyproject.toml
└── requirements.txt
```