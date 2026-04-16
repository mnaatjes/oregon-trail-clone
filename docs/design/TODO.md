# Oregon Trail Implementation TODO

This list tracks the tasks required to establish the foundational infrastructure, contracts, and enforcement mechanisms for the **Screaming MVC** and **Anemic Aggregate** architecture.

## Phase 1: Architectural Foundations (The Spec & Kernel)
*Goal: Establish the "Laws of Physics" and core contracts that govern the system.*

- [x] Implement `ServiceContainer` in `src/core/container.py` (Register/Resolve logic).
- [x] Implement `BaseServiceProvider` in `src/core/contracts/provider.py` (Two-phase Register/Boot).
- [ ] Implement/Refine core Taxonomy Contracts in `src/core/contracts/domain/`:
    - [ ] `DomainRoot`: Sovereign entity with UUID and metadata.
    - [ ] `DomainRecord`: Anemic state fragment for leaf packages.
    - [ ] `DomainBlueprint`: Slug-based static template (Global Truth).
    - [ ] `DomainValueObject`: Shared semantic types (Money, Coord).
- [ ] Implement `DomainBinding` Protocol in `src/core/contracts/domain/binding.py`.
- [ ] Implement `EventBus` in `src/core/events.py` for cross-pillar signaling.

## Phase 2: Architecture Testing Regime (The Guards)
*Goal: Build "Fitness Functions" to automatically enforce ADR compliance as components are developed.*

- [ ] Scaffold Testing Infrastructure in `tests/integration/architecture/`:
    - [ ] `constants.py`: Centralized source of truth for UDB requirements.
    - [ ] `helpers.py`: Diagnostic failure formatting (Linter-style reports).
    - [ ] `conftest.py`: Dynamic domain discovery and parameterized fixtures.
- [ ] Implement `test_structure.py`:
    - [ ] Verify presence of mandatory UDB files (`models.py`, `logic.py`, `services.py`, `binding.py`, `__init__.py`).
    - [ ] Enforce `__all__` exports in `__init__.py` for Encapsulation/Discovery.
- [ ] Implement `test_contracts.py`:
    - [ ] Verify inheritance from core contracts (`DomainRoot`, `DomainRecord`, etc.).
    - [ ] Enforce `@dataclass(frozen=True)` for Models and Blueprints.
    - [ ] Enforce naming conventions (e.g., `*Service`, `*Registry`).
- [ ] Implement `test_dependencies.py`:
    - [ ] Enforce **Zero-Dependency Leaf Policy**.
    - [ ] Detect and prevent circular imports between domains.

## Phase 3: Infrastructure Verification (Mock-ups)
*Goal: Use minimal functional mock-ups to verify that the foundation and tests work as intended.*

- [ ] Create `src/domain/mock_leaf/`:
    - [ ] Minimal implementation to verify UDB compliance and Leaf-level DI.
- [ ] Create `src/domain/mock_root/`:
    - [ ] Verify vertical composition (importing `mock_leaf` models).
    - [ ] Verify root-to-root interaction via Protocols.
- [ ] Verify Testing Regime:
    - [ ] Create a "broken" mock domain and ensure the architecture tests fail with descriptive reports.
- [ ] Implement `EngineOrchestrator` (Skeleton) in `src/engine/orchestrator.py`:
    - [ ] Verify the two-phase (Register -> Boot) lifecycle with mock providers.

## Phase 4: Engine Orchestration & System Lifecycle
*Goal: Complete the Microkernel that manages the game loop and state.*

- [ ] Finalize `EngineOrchestrator`:
    - [ ] Sequence control using `BOOT_PRIORITY`.
    - [ ] System Tick / Turn management.
- [ ] Implement `StateRegistry` in `src/engine/registry.py`:
    - [ ] Collect anemic state snapshots from all active `DomainRoots`.
- [ ] Initialize `src/main.py`:
    - [ ] Wire the `ServiceContainer`, `EventBus`, and `Orchestrator`.

## Phase 5: Pillar Infrastructure (UI & Storage Adapters)
*Goal: Define the boundaries for the View and Persistence layers.*

- [ ] Define Pillar Contracts:
    - [ ] `UIAdapter` (Input/Output boundary).
    - [ ] `StorageAdapter` (Persistence boundary).
- [ ] Implement "Null" Adapters:
    - [ ] Verify that the Engine can boot and tick with mock UI/Storage components.
