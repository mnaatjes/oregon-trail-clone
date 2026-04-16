---
title: "Normal Typing Strategy"
created_at: 2026-04-15
updated_at: 2026-04-15
status: presented
---

# ADR 004: Normal Typing (Structural Typing Redundant)

## Context

The Oregon Trail architecture needs to be consistent and redundencies must be removed.


## Prerequisites

1. The "Screaming-MVC" Architecture must be Accepted [Screaming MVC ADR](001_screaming_mvc.md)

2. [Domain Heirarchy](./002_domain_hierarchy.md) must be determined

3. [Hybrid Typing Strategy](./003_hybrid_typing_strategy.md) MUST be addressed and resolved

4. Clarify what [Normal Typing](./003_hybrid_typing_strategy.md) is

## Decision

1. We will ONLY institute *Normal Typing*

2. We will REMOVE *Structural Typing* mechanisms:
    * Remove `DomainBinding` object in `src/core/contracts/domain/domain_binding./py`

    
## Consequences

## Status:
Presented