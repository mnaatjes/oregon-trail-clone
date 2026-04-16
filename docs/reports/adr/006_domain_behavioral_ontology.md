---
title: "Domain Behavioral Ontology"
created_at: 2026-04-15
updated_at: 2026-04-15
status: pending
---

# ADR 006: Domain Behavioral Ontology

This document relates to the **Systemic Topology** of the Domain (Model Concern). This will be termed **Behavioral Ontology**

The Bootstrap and Engine Systems need a reliable way to Identify, Load, and Interact with Domain Aggregate Root and Leaf Packages.

**Behavioral Ontology (The "Essence")**

**Ontology** is the study of the nature of being and the relationships between entities. This is the Systemic Enforcement, i.e. the rules that govern HOW a *Package* sits in the "World" of the *Engine*.

* **Focus:** "What does this thing do, and where does it fit?"

* **Enforcement:** Bootstrap priority, Service Registration, Event-Bus permissions, and Lifecycle Hooks.

* **Scope:** The Shared Kernel (`domain/common`) and the System Kernel. This is where the Bounded Context is realized.

* **Purpose:** To define the Boundedness—knowing that the Shop Root must be initialized after the Inventory Leaf but before the UI Pillar.

**Ontology** answers the question: "Now that I know this is a Root, what is its scope of authority over the Engine, and which other siblings is it allowed to see?"

## Context

Currently Domain Packages are **Aggregate**, **Structural Sibling** flat arrangements differentiated by the Filesystem by `domain/roots/` and `domain/leaves`.

* We require a robust, **Type Enforced** approach with Contracts - not just for the entities within the Aggregate Packages (`DomainBlueprint`, `DomainRecord`, etc) - the **Taxonomy** - but ALSO their **Ontology** and place within the larger *System Kernel*.

* We need a way to allow the **System Kernel** to understand not just WHAT a file is, but WHERE it belongs in the life cycle of the game.

## Decision

### 1. The Class-Level Metadata (Ontological Details)

Implementation details of `DomainRoot` as `domain/roots/<package-name>/model.py`

These properties in `<Package>Root` define the **Ontology** - the nature of the package's existence - and its relationship to the rest of the system at the **Class-Level**.

**`BOOT_PRIORITY = 5`**

* **The Use-Case:** Sequence Control.

* **The Function:** The Orchestrator uses this to resolve "Chicken and Egg" problems. For example, your Map domain might have a priority of 1, while Character has a 5, and UI has a 10.

* **The Result:** This ensures that the world exists before the character is placed in it, and the character exists before the UI tries to draw their health bar. It prevents *NullPointer* errors during the startup sequence.

**`REQUIRED_PILLARS = ["Persistence", "Events"]`**

* **The Use-Case:** Dependency Guarding.

* **The Function:** This tells the ServiceContainer exactly which "Kernel Pillars" (Core Services) must be initialized and "Healthy" before this domain is allowed to wake up.

* **The Result:** If your Persistence pillar (Save/Load system) fails to mount because of a disk error, the Kernel will catch it and refuse to boot the Character domain. It’s a safety fuse that prevents the game from running in a broken state.

**`DOMAIN_SCOPE = "Global"`**

* **The Use-Case:** Lifecycle Management.

* **The Function:** Defines the "Boundary of Existence."

* **Global:** The domain lives for the entire duration of the application (e.g., the Player).

* **Scene:** The domain is wiped and reloaded when the trail moves from a "Town" to the "Open Prairie" (e.g., specific NPC merchants).

* **The Result:** The Orchestrator knows exactly when to call the "Garbage Collector" on a domain’s state.

### 2. The Package-Level Signature (Taxonomical Declaration)

These `__init__.py` markers define the **Taxonomy** — i.e. the classification of the *Package Species* during the initial *Discovery* scan.

**`__DOMAIN_SPECIES__ = "ROOT"`**

* **The Use-Case:** Structural Validation.

* **The Function:** When the Kernel performs a directory scan, it reads this string first. It acts as a "Pass/Fail" check for your architectural rules.

* **The Result:** If the Kernel finds a package in the domain/leaves/ folder, but its signature says "ROOT", the Kernel can throw a TaxonomyError during development. This is your "Architectural Police" in action, ensuring no one accidentally puts a complex Root where a simple Leaf should be.

**`__DOMAIN_INTENT__ = "Manage Character Identity"`**

* **The Use-Case:** Discoverability & Reflection.

* **The Function:** This is the "Scream" in Screaming MVC, made readable for the machine.

* **The Result:** You can use this for a developer_console command (e.g., list-domains) that prints out every active system and its purpose. It also aids in Self-Documenting Code—where the Engine can generate a map of the Bounded Contexts automatically.

**`__SERVICE_PROVIDER__ = "character.providers.CharacterProvider"`**

* **The Use-Case:** Bootstrap and Dependency Injection

* **The Function:** Every Root Package MUST have an associated ServiceProvider

* **The Result:** Enables lazy-loading of domain logic, ensuring the Kernel can map the ecosystem without triggering premature side-effects or circular dependencies.

## Conclusions

### 1. Summary of Interactions

**Discovery (Taxonomy):** The Kernel scans the folders. It sees `__DOMAIN_SPECIES__` and says, "Okay, you're a Root. I'll treat you like an Aggregate."

**Organization (Ontology):** The Orchestrator looks at the CharacterRoot class. It sees `BOOT_PRIORITY` and `REQUIRED_PILLARS`. It says, "I'll put you in the fifth slot of the boot sequence, but I'll wait until the Event Bus is online first."

### 2. Implications for Testing Regime

Define pytest to check *Outer to Inner*:

1. Start at `domain/` directory

2. Sort by *Package Species*: a. `domain/roots/` and b. `domain/leaves`

3. Identify required **Package-Level Signatues** and capture **Species** information (Taxonomy)

4. Ensure `model.py` corresponds with Typing Inheritance (`DomainRoot` vs `DomainRecord`(leaf))

5. Evaluate *Implemented Model Object* for **Ontological** Details 

### 3. A Note on Types `DomainValueObjects`

**`domain/common` (Shared Kernel Types)**

These are Types, not Actors.

* **The Registry:** You DO NOT "register" Money or Coordinates. You simply import them where they are needed.

* **The Shared Kernel Rule:** Because these are located in domain/common, they are "Global Language." Every Root and Leaf is allowed to import from common without violating your dependency rules. They are the "Nuts and Bolts" available to every station in the kitchen.

### 4. A Note on `DomainRecords` (Leaf)

A `HealthRecord` doesn't belong in the `ServiceContainer` because there isn't just one of them. There might be 5 characters, each with their own `HealthRecord`.

* **The Flow:** The `CharacterService` (which is in the container) holds the `CharacterRoot`, which in turn composes the `HealthRecord`.

* **The Lifecycle:** Records are created, saved, and destroyed. Services are registered once and live until the game closes.

### Conclusion

| Component | In Service Container? | In Domain Registry? | Why? |
| :--- | :--- | :--- | :--- |
| **Root Service** | Yes | Yes | It is an "Actor" that coordinates logic. |
| **Leaf Logic** | No | Yes | It is a "Skill" the Orchestrator needs to find. |
| **DomainRecord** | No | No | It is State. It's the data, not the tool. |
| **Common Type** | No | No | It is Language. It’s used for typing, not runtime logic. |

## Status

**Pending** 2026-04-15