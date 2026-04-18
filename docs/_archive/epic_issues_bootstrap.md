# GitHub Epic Issue Bootstrap Document

This document contains the copy-paste content for the 10 foundational Epic Issues required for the Oregon Trail Project Ledger. Use this to populate the "New Issue" forms in the GitHub Web UI.

---

## [ADR-001] Screaming MVC Architecture

### 🔗 Chain of Custody
- **ADR:** [ADR-001: Screaming MVC Architecture](./docs/explanation/reports/adr/001_screaming_mvc.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Establish the foundational "Screaming MVC" pattern as the project's primary organizational framework. This Epic ensures that the folder structure reveals the game's intent (Domain) rather than just technical roles (Models/Views).

### 🎯 Strategic Goals
- Separates the Spec (Core), the Model (Domain), the Controller (Engine), and the View (UI).
- Implements the Facade Pattern in domain packages via `__init__.py`.
- Protects the core logic from external I/O via Adapter patterns.

### 🛠 Implementation Checklist
- [ ] Define Core Contracts for MVC Pillars
- [ ] Implement Domain Facade Enforcement
- [ ] Set up directory structure for src/core, src/domain, src/engine, src/ui

### ✅ Acceptance Criteria
- [ ] Folder structure matches ADR-001 mapping.
- [ ] Every domain package exports its Nouns and Verbs through a Facade.
- [ ] Zero leakage of I/O logic into the Domain layer.

---

## [ADR-002] Domain Hierarchy & Composition

### 🔗 Chain of Custody
- **ADR:** [ADR-002: Domain Hierarchy](./docs/explanation/reports/adr/002_domain_hierarchy.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Rationalize the Domain Level Architecture by defining a rigid hierarchy of Sovereignty (Roots) and atoms (Leaves). This Epic eliminates circular dependencies through structural typing and vertical composition.

### 🎯 Strategic Goals
- Implements Taxonomy Species: DomainRoot, DomainRecord, DomainValueObject, DomainBlueprint.
- Enforces the Zero-Dependency Policy for Leaf packages.
- Enables lateral interaction via Duck Typing (typing.Protocol).

### 🛠 Implementation Checklist
- [ ] Implement Taxonomy Contracts (Root, Record, ValueObject)
- [ ] Create structural protocol templates for lateral interaction
- [ ] Define Root-to-Leaf composition patterns

### ✅ Acceptance Criteria
- [ ] No direct imports between sibling Leaf packages.
- [ ] Roots interact with other Roots via Protocols only.
- [ ] All entities inherit from foundational Taxonomy contracts.

---

## [ADR-003] Anemic Aggregator Domains

### 🔗 Chain of Custody
- **ADR:** [ADR-003: Anemic Aggregator Domains](./docs/explanation/reports/adr/003_anemic_aggregator_domains.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Enforce the "Aggregator" rule where Roots manage related Leaf records. This Epic ensures total serializability of game state through frozen dataclasses and anemic purity.

### 🎯 Strategic Goals
- Ensures 100% snapshotability of the game state.
- Separates Model (State) from Logic (Math) and Services (Flow).
- Implements UUID assignment for Sovereign Roots.

### 🛠 Implementation Checklist
- [ ] Implement `@dataclass(frozen=True)` enforcement
- [ ] Define Root aggregation logic for Leaf hydration
- [ ] Set up IdentityService for UUID management

### ✅ Acceptance Criteria
- [ ] Game state is serializable to JSON without side effects.
- [ ] Mutation of state always returns a new instance (clone/replace).
- [ ] Models contain zero behavioral logic.

---

## [ADR-004] Domain Package Anatomy

### 🔗 Chain of Custody
- **ADR:** [ADR-004: Domain Package Anatomy](./docs/explanation/reports/adr/004_domain_package_anatomy.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Codify the physical folder structure of domain packages. This Epic standardizes the "Package Anatomy" into four mandatory files: `models.py`, `logic.py`, `services.py`, and `__init__.py`.

### 🎯 Strategic Goals
- Predictability: Developers know exactly where to find math vs. data.
- Enforces the "Calculator vs. Operator" distinction.
- Protects internal domain details via `__all__` exports.

### 🛠 Implementation Checklist
- [ ] Create domain package templates
- [ ] Implement `__all__` linting rules
- [ ] Verify separation of Service (Flow) from Logic (Math)

### ✅ Acceptance Criteria
- [ ] Every domain package contains the mandatory 4-file set.
- [ ] Logic.py remains pure math with zero I/O or side effects.
- [ ] Facade exports are explicitly defined.

---

## [ADR-005] Domain Model Taxonomy

### 🔗 Chain of Custody
- **ADR:** [ADR-005: Domain Model Taxonomy](./docs/explanation/reports/adr/005_domain_model_taxonomy.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Establish the "DNA" of the system by defining the four species of data. This Epic focuses on type enforcement and composition rules for all domain models.

### 🎯 Strategic Goals
- Distinguishes stateful actors (Roots) from anonymous fragments (Records).
- Defines the role of Static Blueprints (Global Truth) and semantic Value Objects.
- Enforces composition constraints (e.g., Records cannot contain Roots).

### 🛠 Implementation Checklist
- [ ] Implement DomainBlueprint loading logic
- [ ] Define common ValueObjects (Money, Coord)
- [ ] Enforce taxonomic rules in model declarations

### ✅ Acceptance Criteria
- [ ] All domain objects are classified into one of the four species.
- [ ] Composition rules (ADR-005) are followed in all new models.

---

## [ADR-006] Domain Behavioral Ontology

### 🔗 Chain of Custody
- **ADR:** [ADR-006: Domain Behavioral Ontology](./docs/explanation/reports/adr/006_domain_behavioral_ontology.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Define how domain packages sit in the "World of the Engine." This Epic focuses on metadata signatures and the sequential boot process required to build the game state.

### 🎯 Strategic Goals
- Implements package discovery via `__DOMAIN_SPECIES__` and `__DOMAIN_INTENT__`.
- Establishes a predictable Boot Priority (Infrastructure -> Environment -> Actors -> UI).
- Maps ServiceProviders to the DI container.

### 🛠 Implementation Checklist
- [ ] Implement Orchestrator discovery logic
- [ ] Define Boot Priority constants
- [ ] Set up metadata enforcement for `__init__.py`

### ✅ Acceptance Criteria
- [ ] Orchestrator can discover and register all domain packages automatically.
- [ ] Packages boot in the sequence defined by their priority.

---

## [ADR-007] Domain Ecosystem & Orchestration

### 🔗 Chain of Custody
- **ADR:** [ADR-007: Domain Ecosystem](./docs/explanation/reports/adr/007_domain_ecosystem.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Establish the interaction rules for the "Living World." This Epic focuses on the Event Bus (The Nervous System) and the Heartbeat (Metabolic Tick) that drives game progression.

### 🎯 Strategic Goals
- Decouples Roots via event-based communication.
- Implements the "Metabolic Tick" for world progression.
- Centralizes state tracking via the StateRegistry for total snapshotting.

### 🛠 Implementation Checklist
- [ ] Implement Core Event Bus
- [ ] Define System Tick / Turn Protocol
- [ ] Set up StateRegistry for save-game management

### ✅ Acceptance Criteria
- [ ] Roots communicate exclusively via events or protocols.
- [ ] The world state can be captured in a single snapshot from the Registry.
- [ ] Leaves remain silent and speak only through their parent Roots.

---

## [ADR-008] Diátaxis Documentation Framework

### 🔗 Chain of Custody
- **ADR:** [ADR-008: Diátaxis Documentation Framework](./docs/explanation/reports/adr/008_diataxis_documentation.md)
- **TDD:** N/A
- **Component:** `Core`

### 📝 Overview
Adopt the Diátaxis framework to standardize project knowledge. This Epic organizes all documentation into four distinct quadrants to serve different user needs.

### 🎯 Strategic Goals
- Organizes docs into Tutorials, How-To, Explanation, and Reference.
- Ensures predictable discovery of architectural and technical guides.
- Standardizes the physical structure of the `docs/` directory.

### 🛠 Implementation Checklist
- [ ] Reorganize existing docs into Diátaxis quadrants
- [ ] Create templates for each documentation type
- [ ] Implement frontmatter standards for all docs

### ✅ Acceptance Criteria
- [ ] Every document resides in the correct quadrant folder.
- [ ] All docs follow the standardized frontmatter schema.

---

## [ADR-009] Technical Design Document (TDD) Workflow

### 🔗 Chain of Custody
- **ADR:** [ADR-009: Technical Design Documentation](./docs/explanation/reports/adr/009_technical_design_doc.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Formalize the transition from abstract architecture (ADR) to concrete code via the TDD process. This Epic ensures that every line of code in `src/` is preceded by an approved blueprint.

### 🎯 Strategic Goals
- Enforces the "Law of the Spec."
- Standardizes TDD sections (Overview, Goals, Detailed Design).
- Bridges the gap between Documentation and Execution layers.

### 🛠 Implementation Checklist
- [ ] Create TDD Markdown Template
- [ ] Implement TDD validation in the lifecycle workflow
- [ ] Define Mermaid diagram standards for designs

### ✅ Acceptance Criteria
- [ ] No feature code is written without a linked and approved TDD.
- [ ] TDDs contain sufficient detail for autonomous implementation.

---

## [ADR-011] Development Lifecycle and Workflow

### 🔗 Chain of Custody
- **ADR:** [ADR-011: Development Lifecycle and Workflow](./docs/explanation/reports/adr/011_development_lifecycle_workflow.md)
- **TDD:** PENDING
- **Component:** `Core`

### 📝 Overview
Enshrine the "Four Laws of Engineering" and the mandatory "Chain of Custody." This Epic focuses on the rigorous lifecycle required to maintain architectural integrity as the project scales.

### 🎯 Strategic Goals
- Implements the Law of Provenance (ADR -> TDD -> Issue -> Code).
- Establishes the GitHub Project as the authoritative metadata ledger.
- Defines the branching and PR strategies (Atomic PRs, Squash & Merge).

### 🛠 Implementation Checklist
- [ ] Set up GitHub Project Ledger (v2)
- [ ] Implement Branch Naming Enforcement (e.g., via Git Hooks)
- [ ] Standardize Issue and PR templates

### ✅ Acceptance Criteria
- [ ] Every commit/PR is traceable to an Issue and a TDD/ADR.
- [ ] Architectural Police checks are integrated into the CI/CD pipeline.
