---
author: Michael Naatjes
email: michael.naatjes87@gmail.com
updated_at: 2026-04-12
---

# Oregon Trail Clone

## Directory Tree

```text
./
├── assets/             # ASCII art text files
├── docs/            
├── src/
│   ├── core/           # Technical engine (asset loading, events)
│   ├── domain/         # Pure logic (models, services, interfaces)
│   ├── engine/         # MVC Controller / Orchestrator
│   ├── storage/        # Data persistence (JSON/File system)
│   ├── ui/             # MVC View (Textual/Asciimatics)
│   └── main.py         # Gateway entry point
├── tests/              # Pytest files
├── .venv/              # Virtual environment
├── pyproject.toml
└── requirements.txt
```