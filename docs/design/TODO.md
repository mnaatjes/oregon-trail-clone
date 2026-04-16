# Oregon Trail Implementation TODO

This list tracks the architectural and domain tasks required to realize the **Screaming MVC** and **Anemic Aggregate** architecture.

## Phase 1: Core Specifications (The Spec)
- [ ] Implement foundational domain contracts in `src/core/contracts/domain/`:
    - [ ] `DomainRoot` (with UUID and metadata fields)
    - [ ] `DomainRecord` (anemic base)
    - [ ] `DomainBlueprint` (slug-based template)
    - [ ] `DomainValueObject` (shared kernel types)
- [ ] Implement `ServiceContainer` in `src/core/container.py` (Register/Resolve logic).
- [ ] Implement `BaseServiceProvider` in `src/core/contracts/provider.py` (Two-phase Register/Boot).
- [ ] Implement `EventBus` in `src/core/events.py` for cross-pillar signals.

## Phase 2: Domain Layer (The Model)
- [ ] Create Shared Kernel in `src/domain/common/`:
    - [ ] `Money` and `Coord` value objects.
    - [ ] Cross-domain `Structural Protocols` (e.g., `Payer`, `Renderable`).
- [ ] Scaffold **Leaf Packages** in `src/domain/leaves/`:
    - [ ] `health`: Models, Logic, and Service.
    - [ ] `stats`: Character attributes logic.
    - [ ] `inventory`: Item container logic.
- [ ] Scaffold **Root Packages** in `src/domain/roots/`:
    - [ ] `character`: Aggregates health, stats, and identity.
    - [ ] `wagon`: Aggregates inventory and durability.
    - [ ] `shop`: Uses Protocols to interact with characters/wagons.

## Phase 3: Engine Orchestration (The Controller)
- [ ] Implement `EngineOrchestrator` in `src/engine/orchestrator.py`:
    - [ ] Boot sequence based on `BOOT_PRIORITY`.
    - [ ] System Tick / Turn management.
- [ ] Implement `StateRegistry` in `src/engine/registry.py` for world snapshotting.
- [ ] Wire `DomainServiceProvider` for each domain package.

## Phase 4: UI and Storage Pillars
- [ ] Implement **UI Pillar** in `src/ui/`:
    - [ ] Terminal adapter (e.g., Textual or Asciimatics).
    - [ ] Renderers that satisfy `Renderable` protocols.
- [ ] Implement **Storage Pillar** in `src/storage/`:
    - [ ] JSON Persistence adapter for the `StateRegistry`.

## Phase 5: Verification and Polish
- [ ] Complete **Architecture Testing Regime** in `tests/integration/architecture/`:
    - [ ] `test_domain_integrity.py` (Taxonomy check).
    - [ ] `test_dependency_rules.py` (Zero-Dependency Leaf check).
- [ ] Ensure `src/main.py` correctly initializes the gateway and boots the kernel.
