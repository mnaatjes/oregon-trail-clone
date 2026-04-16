---
title: "Anemic Aggregator Domains"
created_at: 2026-04-15
updated_at: 2026-04-15
status: pending
---

# Anemic Aggregator Domains: Roots and Leafs

The Oregon Trail Domain needs a Comprehensive Structural Digest which outlines the rules and composition of *Packages* within `domain/` (the Model Concern of the established [Screaming MVC Architecture](./001_screaming_mvc.md))

## Context

The Planned Architecture MUST:

1. Maintain **Structural Siblings**

    * `domain/` directory will maintain a flat structure divided into `leafs` and `roots`

    * Allows for a *leaf* to be accessed in a **Conceptual Hierarchy** by many *roots*. Therefore a *leaf* can be re-used by any *roots* which need it.

2. Allow for **Conceptual Hierarchy**: 

    * An Aggregator *Root* can contain multiple *Leaf* properties; e.g. a Character (root) has leafs: health, inventory, identity

    * An Aggregator *Root* can possess another *Root* Package as a sub-domain; e.g. Shop (root) has sub-domain Character(Shopkeeper)


3. Establish the *Package* **Fascade** in `domain/<package_name>/__init__.py`

## Decisions

## Consequences

## Status

**Pending** 2026-04-15