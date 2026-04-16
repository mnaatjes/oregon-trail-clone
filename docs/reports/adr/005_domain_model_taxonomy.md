---
title: "Domain Model Taxonomy"
description: "Classification of domain entities into Roots, Records, Blueprints, and Value Objects."
type: "explanation"
status: "stable"
created_at: "2026-04-15 00:00:00"
updated_at: "2026-04-15 00:00:00"
owner: "Michael Naatjes"
tags: ["adr", "domain", "taxonomy", "typing"]
version: "0.1.0"
---

# ADR 005: Domain Model Taxonomy

This document covers the **Static Classification** of the **Anemic Aggregate Packages** that compose a `domain/package`

**Structural Taxonomy (The "Species")**

Taxonomy is the classification of things based on shared characteristics. This is the **Type Enforcement** of the package's "DNA."

* **Focus:** "What is this thing?"

* **Enforcement:** Inheritance (isinstance(obj, DomainRoot)), Python Type Hints, and Class Attributes.

* **Scope:** The individual package and its immediate internal files (models.py, logic.py).

* **Purpose:** To ensure that a Character package follows the "Screaming" rules of a Root and that its models.py uses the correct DomainBlueprint.

Taxonomy answers the question: "Does this folder have the physical components and inheritance required to be called a Root?"

## Context

We MUST define Abstract Contracts in order to use Normal Typing Enforcement and Standardize Domain Packages and entities, thereby defining Taxonomy.

## Decision

### 1. Global Template: `DomainBlueprint`

**What it does:** Represents the "Global Truth." It is the static template defined by your game design (e.g., a "Farmer" profession or a "Wagon" model).

**What it needs:** A unique slug for lookup. It must be read-only and shared across many instances.

**Package Role:** It serves as the "DNA" used by a Service to initialize state. It lives in `models.py.`

**Anemic Context:** It is the data input for Logic. Logic reads a Blueprint to determine how a state should be modified (e.g., a "Blizzard" blueprint dictates the severity of a health penalty).

### 2. Data Bundle: `DomainValueObject`

Domain Value Objects are NOT `models` but they are REQUIRED for the logic within the Package to execute correctly. They ARE **Shared Kernels** or Common Entities stored in `domain/common/`

* Used to turn a raw value (int, str, etc) into a **Business Concept** 

* Bundles Primatives that belong together and enforces that these values are NEVER separated

**Examples:**

* **Money:** An int (amount) and a str (currency).

        Why? Because 100 is useless if you don't know if it's "Gold Doubloons" or "U.S. Dollars."

* **Coordinates:** A float (x) and a float (y).

        Why? A latitude without a longitude is just a line. Together, they are a specific point on the map.

* **HealthRange:** A min (0) and a max (100).

        Why? It prevents a logic error where someone sets current_hp to 150 when the max is 100. The Value Object can validate this during creation.

* **Measurement:** A float (value) and a str (unit, e.g., "lbs").

**Directory Structure** (Relative to Leaf, Root)

```text
src/
└── domain/
    ├── common/               <-- THE SHARED KERNEL (Value Objects & Types)
    │   ├── __init__.py
    │   ├── money.py          <-- Money(amount, currency)
    │   ├── measure.py        <-- Weight(value), Distance(value)
    │   └── spatial.py        <-- Coordinate(x, y)
    │
    ├── leaves/               <-- Standalone Logic
    │   └── health/
    │
    └── roots/                <-- Aggregates
        └── character/
```

### 3. Leaf-Level State: `DomainRecord`

Defined as a *passive*, **Anemic** snapshot of a specific state.

The Leaf-Level State `DomainRecord` Contract represents both the **Physical Location** `domain/leaf/package/` AND the **Logical Structure** of behavior (Domain Intent and Bounded Context).

**Physical Location vs. Logical Structure**

* **The Leaf (The Package):** "Leaf" describes the package’s position in your structural hierarchy. It tells you, "This folder has no sibling dependencies."

* **The Record (The Object):** "Record" describes the behavior of the data inside that package.

**The Anemic "Row" Logic**

If the `Health` package is a Table, then the `DomainRecord` is a Single Row. 

It is a **Passive Data Structure**. It doesn't "act"; it is "recorded" and "mutated" *by Logic*. It’s a ledger entry of a character's vitality or a wagon's durability.

Relationships: `logic.py`

**Composition and Taxonomy**

When you build your `DomainRoot` (The Aggregate), you are composing it out of these sub-details.

    "A Character (Root) is composed of several Records (Health, Stats, Inventory)."

**Workflow**

1. You create a Leaf Package in `domain/leaf/health/`.

2. Inside that package, you define a `HealthRecord` that inherits from `DomainRecord`.

3. The `DomainRecord` contract ensures that HealthRecord is **anemic**, **cloneable**, and **validatable**.

### 4. Aggregate Root: `DomainRoot`

* **What it does:** Represents the sovereign "Actor" and the anchor of identity for a Root Package. It is the conceptual "Master File" that coordinates and composes Blueprints and Records into a singular entity.

* **What it needs:** A unique UID (Identity) and the ability to hold references to multiple Leaf Records and Global Blueprints.

* **Package Role:** The fundamental unit of a Root Package (e.g., domain/roots/character/). It is the primary object that the Engine and Orchestrator interact with.

* **Anemic Context:** It is the Orchestration Hub. While it is anemic (containing no logic), it acts as the "Mise en Place" for the Service. A CharacterService receives a DomainRoot, decomposes its internal Records, sends them to their respective Leaf Logics, and then reassembles the updated DomainRoot.

* **Workflow:**

    1. You create a Root Package in domain/roots/character/.

    2. You define a CharacterRoot that inherits from DomainRoot.

    3. The DomainRoot contract ensures the object has a persistent UUID, making it distinct even if two characters have identical stats.

### Conclusion

**The Taxonomy Rule of Composition:**

1. A `DomainRoot` may contain many `DomainRecords`. 

2. A `DomainRecord` may contain many `DomainValueObjects`. 

3. However, a `DomainRecord` (Leaf) MUST NOT contain a `DomainRoot`. This enforces the hierarchical flow of your Oregon Trail world.

| Term | Analogy | Technical Mapping |
| :--- | :--- | :--- |
| **DomainRoot** | The "Actor" | An Object with a UID. |
| **DomainRecord** | The "Status" | A Data Row with State. |
| **DomainValueObject** | The "Type" | A Bundle with Semantic Meaning. |
| **DomainBlueprint** | The "Class" | A Template with Static Data. |