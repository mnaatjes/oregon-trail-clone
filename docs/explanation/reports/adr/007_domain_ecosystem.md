---
id: ADR-007
title: "Domain Ecosystem"
status: adopted
created_at: 2026-04-15
updated_at: 2026-04-18
component: core
type: "explanation/adr"
epic_link: "https://github.com/mnaatjes/oregon-trail-clone/issues/7"
---

# ADR 007: The Domain Ecosystem

**The Domain Ecosystem (The World)**

While the *Kernel* is the mechanism, the **Ecosystem** is the totality.

## Decision

### 1. The Event Bus (The Nervous System)
Communication between Roots must be decoupled. 
* **Rule:** Roots emit events; other Roots listen. 
* **Constraint:** Leaves are silent. They only speak through their parent Root.

### 2. The Heartbeat (Metabolic Tick)
The world progresses via a system-wide "Tick" event.
* **Metabolism:** When the Tick occurs, the Orchestrator notifies the Roots, who then invoke their respective Leaf Logics to update their anemic state.

### 3. Total Snapshotting
The StateRegistry collects every active `DomainRoot` in the world. Saving a game is simply a JSON dump of the StateRegistry.

## Status
**Adopted** 2026-04-16
