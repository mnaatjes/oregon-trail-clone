---
title: "Domain Ecosystem"
created_at: 2026-04-15
updated_at: 2026-04-16
status: pending
---

# ADR 007: The Domain Ecosystem

**The Domain Ecosystem (The World)**

While the *Kernel* is the mechanism, the **Ecosystem** is the totality.

* **The Metaphor:** If the Kernel is the Laws of Physics and Biology, the Ecosystem is The Oregon Trail itself.

    Why use this term? It describes the complex, symbiotic relationships between your independent "Sovereign" packages.

* **The Interaction:** A "Blizzard" (Weather Leaf) affects "Health" (Character Leaf), which changes "Morale" (Stats Leaf), which might cause a "Merchant" (Shop Root) to raise prices.

The *Kernel* doesn't care about the blizzard; the **Ecosystem** is where that story happens.

Use **Ecosystem** when you are talking about the collection of Roots and Leaves interacting during gameplay.

## Context

### 1. Symbiotic Interaction (Handshake)

Must address HOW the **Symbiotic Interaction** - the functional *Handshake* that allows two separate layers of a system to thrive without direct coupling - actually happens

**Interaction between Taxonomy and Ontology**

* **The Taxonomy (The Biology):** Provides the physical hooks. It guarantees that a package has a models.py and a `__DOMAIN_SPECIES__`.

* **The Ontology (The Role):** Provides the systemic context. It says, "Since this is a ROOT (Taxonomy), I will assign it a BOOT_PRIORITY of 5 (Ontology)."

* **The Symbiosis:** The System Kernel uses the Taxonomic signature to decide which Ontological rules to apply. Without Taxonomy, the Kernel is blind; without Ontology, the code is just "dead matter" that never gets booted or prioritized. They rely on each other to move from "Code" to "System."

> NOTE: As the number of **Domain Packages** (Roots/Leaves) grows, direct point-to-point communication creates a 'Big Ball of Mud.' We need a formal definition for how independent packages interact symbiotically while remaining blissfully unaware of each other's internal implementation.

## Decision

### 1. Orchestrator and Kernel

**The "Manager" (The Orchestrator)**

If you are looking for the specific name of the component inside the Kernel that performs the act of "overseeing," that is the Domain Orchestrator.

The Domain Orchestrator is the part of your **System Kernel** that:

1. Scans the directory (Awareness).

2. Vets the Inheritance (Taxonomy).

3. Wires the Service Providers (Ontology).

4. Monitors the **Bounded Context** boundaries (Enforcement).

Use **Orchestrator** when talking about *Movement and Sequence*. The Orchestrator is the active, living component that "does the work." It is represented by the Core *Engine* or a Domain *Service*

Use **System Kernel** when you are talking about your Core code that handles the ServiceContainer and bootstrapping.

| Term | Scope | Focus | Analogy |
| :--- | :--- | :--- | :--- |
| **System Kernel** | The Engine Core | Laws & Logic. | The Government / Physics. |
| **Domain Ecosystem** | The Whole Game | Interactions & Life. | The Wilderness / Society. |
| **Orchestrator** | The Registry/Booter | Coordination & Setup. | The Conductor |

### 2. The Communication Protocol (Nervous System)

In a healthy ecosystem, siblings shouldn't always be "managed"; sometimes they react to the environment.

#### Event Bus

* **The Definition:** the *Event Bus* (or Signal System) is the **Nervous System** of the Ecosystem.

* **The Rule:** Roots/Leaves emit **Events** (e.g., `CharacterHungry`, `BlizzardStarted`). The **Orchestrator** or other **Siblings** listen and react. This prevents a "Blizzard" package from needing to know that a "Health" package even exists.

#### Event Ownership / Sovereignty

* **The Rule:** Only a Root Service is allowed to emit a Public Event. Leaves must remain silent to the outside world.

* **Why:** If a HealthRecord (Leaf) starts shouting events directly to the Shop (Root), you’ve bypassed the "Sovereign" protection of the Character Root.

* **Implementation:** Events are a Root-level privilege. Leaves report changes to their parent Root; only the Root broadcasts to the Ecosystem.

### 3. Lifecycle of the Ecosystem - Hearbeat (Tick)

An ecosystem in a game like Oregon Trail relies on the progression of time.

* **The Definition:** The Tick/Turn Protocol.

* **The Logic:** A **Broadcast Event** occurs, emitted by the Orchestrator, ensuring any **Metabolic** needs are met

* **Why:** If the Orchestrator calls process_day() on every Root, it must import every Root (or a common interface). This creates a "Dependency Funnel."

* **The Ontological Hook:** This ties back to your `BOOT_PRIORITY`. The Ecosystem needs a Tick Priority to ensure "Weather" is calculated before "Health" is penalized.

### 4. The "World State" (The Ecosystem Container)

Where does the data for the "Totality" live?

* **The Definition:** The State Registry.

* **The Logic:** While individual Roots hold their own state, the Ecosystem needs a way for the Persistence Pillar to grab the entire "World Snapshot" (every Root and Leaf currently active) for a save-game.


## Consequences

### 1. Implications for the Ecosystem

| Concept | Responsibility | Implementation |
| :--- | :--- | :--- |
| **Sovereignty** | Package isolation. | Enforced by Kernel. |
| **Symbiosis** | Cross-domain reaction. | Facilitated by Event Bus. |
| **Metabolism** | Time-based progression. | Enforced by System Tick. |
| **Persistence** | State Snapshotting. | Facilitated by the State Registry. |

## Status

**Pending** 2026-04-16

## Appendix 

### Review of Taxonomy and Ontology of the Domain

| Feature | Structural Taxonomy (Species) | Behavioral Ontology (Existence) |
| :--- | :--- | :--- |
| **Focus** | Identity: "What is this thing?" | Purpose: "What does it do and where?" |
| **Metaphor** | The Uniform (Chef's Whites). | The Station (The Saute Station). |
| **Verification** | Class Inspection (`issubclass`) & Signature. | Registry Manifest & Metadata Evaluation. |
| **Key Artifacts** | `DomainRoot`, `__DOMAIN_SPECIES__`. | `BOOT_PRIORITY`, `REQUIRED_PILLARS`. |
| **System Goal** | Discovery: Is this a valid Root? | Orchestration: When/how do we boot it? |
| **Constraint** | Inheritance: "Must have a Slug/DTO." | Topological: "Must boot before the UI." |
| **Responsibility** | Package Internal Integrity. | System Inter-connectivity & Boundaries. |
| **Scope** | Self-Contained: Introspective focus. | Boundary-Crossing: Relational focus. |
| **Failure Mode** | `TaxonomyError` / `TypeError`. | `SystemHang` / `CircularDependency`. |