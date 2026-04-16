---
title: "Screaming MVC System Architecture"
created_at: 2026-04-15
updated_at: 2026-04-15
status: pending
---

# ARD 001: Screaming Model View Controller (MVC) Architecture

## Context

The Oregon Trail requires a clear and thorough declaration of the overall program architecture. 

## Prerequisites

1. Clarify the distinction between [Ports & Adapters](#ports--adapters) and [MVC](#mvc) Architectures.
    * Can Ports & Adapters be used and where in architecture (model, view, and/or controller)
    * Is Hexagonal Architecture mutually exclusive to MVC Architecture?

2. Define and Resolve WHAT [Screaming](#screaming-architecture) is and HOW it will be applied
    * Define naming Conventions; a recipe
    * Map major directories

3. Determine if *Screaming* / Feature-Driven MVC will apply ONLY to `domain/` (i.e. models) or all converns (Model, View, and/or Controller)
    * Which makes sense?
    * Can this be accomplished in an intuitive manner that is not counter-productive?


## References

### Ports & Adapters

* Intended for use with ___

### MVC

* Intended for use with ___

### Screaming Architecture (MVC)

* Intended for use with ___
* Also known as *Feature-Driven MVC* or *Vertical Slice Architecture*

## Decision

1. MVC Architecture adopted as the Structural Pattern

2. *Screaming* MVC implemented

* `models/` directory renamed `domain` and rules governing concern determined in [Domain Heirarchy ADR](./002_domain_hierarchy.md)
* Directory Structure with MVC translations
```
src/
├── core/      # The Specification (Contracts & DI)
├── domain/    # THE MODEL (Screaming Business Logic: Character, Health, Wagon)
├── engine/    # THE CONTROLLER (Orchestration & Providers)
└── ui/        # THE VIEW (TUI Components)
```
* Architecture terminology for project: `Feature-Driven MVC` and `Screaming MVC` are synonymous

3. **Interface** governing the `domain/`: 

    * **Discovery** mechanism 
    
    * **Encapsulation** with *Fascade Pattern* 
    
    Use `__init__.py` to lift the functions up to the top level; e.g. character.apply_aging()



## Consequences

### Positive

* Strictly defined naming conventions
* Ability to understand Concern(s) (i.e. Model, View, and/or Controller) without technical expertise

### Negative

* If Screaming MVC only applied to Domains (Model Concern) this may cause confusion for users investigating code

## Status: Developing