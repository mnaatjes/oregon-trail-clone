---
title: "TDD: Domain Context Manifest"
description: "Technical design for the unified DomainContext manifest used to define Bounded Contexts."
type: "design"
status: "draft"
created_at: "2026-04-16 11:00:00"
updated_at: "2026-04-16 11:00:00"
owner: "Michael Naatjes"
tags: ["design", "domain", "manifest", "discovery"]
version: "0.1.0"
---

# TDD: Domain Context Manifest

## Overview
This document defines the implementation of the `DomainContext` manifest, a unified object that serves as the "Identity Card" for every Bounded Context in the Oregon Trail engine.

## Goals
- Unify fragmented metadata (`__DOMAIN_INTENT__`, `__DOMAIN_SPECIES__`) into a single object.
- Provide type-safe discovery for the Kernel's ServiceProvider and Orchestrator.
- Standardize the "Scream" of a package at the code level.

## Proposed Design

### 1. The Contract
The manifest is a frozen dataclass residing in the core contracts.

```python
# src/core/contracts/domain/context.py
from dataclasses import dataclass
from enum import Enum, auto

class DomainSpecies(Enum):
    ROOT = auto()
    LEAF = auto()

@dataclass(frozen=True)
class DomainContext:
    """
    The identity manifest for a Bounded Context.
    """
    intent: str           # The 'Scream' (e.g., 'vitality', 'character')
    species: DomainSpecies # ROOT or LEAF
    priority: int = 10    # Boot sequence priority (lower = earlier)
    version: str = "0.1.0"
```

### 2. Package Integration
Every package defines its manifest in `__init__.py`.

```python
# src/domain/roots/character/__init__.py
from src.core.contracts.domain.context import DomainContext, DomainSpecies
from .services import CharacterService
from .models import CharacterRoot

__CONTEXT__ = DomainContext(
    intent="character",
    species=DomainSpecies.ROOT,
    priority=5
)

__all__ = ["CharacterService", "CharacterRoot", "__CONTEXT__"]
```

### 3. Discovery Flow
The Kernel discovers contexts by scanning the `src/domain/` directory and inspecting the `__init__.py` of each package.

```mermaid
graph TD
    Kernel[Kernel Boot] --> Scanner[Domain Scanner]
    Scanner --> Package[src/domain/roots/character]
    Package --> Load[Import __init__.py]
    Load --> Check{Has __CONTEXT__?}
    Check -- Yes --> Register[Register with ServiceContainer]
    Check -- No --> Fail[Architectural Error / Hard Fail]
```

## Cross-Cutting Concerns
- **Validation:** The Architecture Testing Regime (Fitness Functions) will verify that `__CONTEXT__.intent` matches the physical folder name.
- **Serialization:** The manifest may be used by the State Registry to tag snapshot data with the correct version and intent.

## References
- [ADR 003: Anemic Aggregator Domains](../reports/adr/003_anemic_aggregator_domains.md)
- [ADR 006: Domain Behavioral Ontology](../reports/adr/006_domain_behavioral_ontology.md)
