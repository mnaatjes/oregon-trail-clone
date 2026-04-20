---
id: TDD-017
parent_adr: ADR-014
title: "TDD: Domain Discovery Scanner"
status: draft
created_at: 2026-04-20
updated_at: 2026-04-20
component: engine
type: "explanation/design"
feature_link: https://github.com/mnaatjes/oregon-trail-clone/issues/42
---

# TDD: Domain Discovery Scanner

## 1. Overview
The `DomainScanner` is a specialized Engine utility designed to bridge the gap between the physical filesystem and the logical Domain Layer. It automates the detection of `DomainContext` manifests, allowing the game engine to "self-assemble" by discovering and loading all available domain packages at runtime.

## 2. Infrastructure & Tooling
The scanner utilizes three primary Python standard library modules to perform reflection and dynamic loading.

### A. Filesystem Navigation: `pathlib.Path`
*   **Purpose**: Recursively traverses the `src/domain` directory to find package entry points.
*   **Input**: A filesystem directory path.
*   **Output**: A generator of `Path` objects pointing to `__init__.py` files.
*   **Implementation Note**: We use `.rglob("__init__.py")` to ensure we find nested domains in `roots/`, `leaves/`, and `common/`.

### B. Dynamic Importing: `importlib.util`
*   **Purpose**: Loads Python code from a file path into memory without requiring a static `import` statement.
*   **Input**: A physical file path.
*   **Output**: A loaded Python Module object.
*   **Example Code**:
    ```python
    import importlib.util
    from pathlib import Path

    def load_module_from_path(path: Path):
        # Create a unique name for the dynamic module to avoid collisions
        module_name = f"discovery.{path.parent.name}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    ```

### C. Attribute Introspection: `getattr`
*   **Purpose**: Safely extracts the `__CONTEXT__` object from the loaded module.
*   **Input**: The loaded module object.
*   **Output**: The `DomainContext` instance.
*   **Example Code**:
    ```python
    # Safely extract the manifest
    manifest = getattr(module, "__CONTEXT__", None)
    
    if not manifest:
        raise DiscoveryError(f"Package at {path} is missing __CONTEXT__ manifest.")
    ```

## 3. Structural Design

### Location (Pillar Mirroring)
Following the `src/{layer}/{pillar}/{role}` standard:
*   **Path**: `src/engine/domain/scanner.py`
*   **Layer**: `engine` (Active system logic)
*   **Pillar**: `domain` (Domain management responsibility)
*   **Role**: `scanner` (Utility service)

### Class Architecture
To support future extensibility (e.g., `AssetScanner`, `UIScanner`), the system employs an abstract base class.

#### The Base Contract
*   **Location**: `src/core/kernel/contracts/scanner.py`
*   **Definition**:
    ```python
    from abc import ABC, abstractmethod
    from pathlib import Path
    from typing import List, Generic, TypeVar

    T = TypeVar("T")

    class BaseScanner(ABC, Generic[T]):
        @abstractmethod
        def scan(self, target_path: Path) -> List[T]:
            """Scans a path and returns a list of discovered entities of type T."""
    ```

#### The DomainScanner Implementation
*   **Class Type**: **Stateless Service**.
*   **Instantiation**: It is instantiated by the `Kernel` and registered in the `ServiceContainer`.
*   **State**: It maintains no internal state, allowing it to be safely reused or tested against different directories.
*   **DI Key**: `engine.domain_scanner`

## 4. Integration & Usage

### Usage with DomainOrchestrator
The `DomainScanner` is a primary dependency of the `DomainOrchestrator`.

1.  **Boot Phase**: The `DomainOrchestrator` receives the `DomainScanner` via constructor injection.
2.  **Discovery**: The Orchestrator calls `scanner.scan(Path("src/domain"))`.
3.  **Handoff**: The Orchestrator receives a `List[DomainContext]` and passes them to the `DomainRegistrar` for wiring.

### Separation of Concerns
By separating the `Scanner` from the `Orchestrator`:
*   The **Scanner** handles filesystem IO and Python import "magic."
*   The **Orchestrator** handles the logical boot sequence and priority graphing.
*   **Testing**: We can test the Orchestrator with a "Mock Scanner" that returns hardcoded contexts, avoiding slow and brittle filesystem tests in the Orchestrator suite.

## 5. Testing & Validation

### Tooling Verification (Filesystem Isolation)
To test the scanner without it scanning the entire project, use the `pytest` `tmp_path` fixture.

```python
def test_scanner_identifies_valid_manifests(tmp_path):
    # 1. Setup: Create a fake domain package
    domain_dir = tmp_path / "mock_domain"
    domain_dir.mkdir()
    init_file = domain_dir / "__init__.py"
    
    # Write a valid manifest to the fake file
    init_file.write_text("from src.core.domain.contracts.context import DomainContext\n"
                         "__CONTEXT__ = DomainContext(family='ROOT', species='TEST')")

    # 2. Act
    scanner = DomainScanner()
    results = scanner.scan(tmp_path)

    # 3. Assert
    assert len(results) == 1
    assert results[0].species == 'TEST'
```

### Major Methods to Verify
1.  **`scan(path)`**: Ensure it ignores directories without `__init__.py`.
2.  **`validate(manifest)`**: Ensure it raises `DiscoveryError` if `__CONTEXT__` is the wrong type or missing.
3.  **`path_resolution`**: Ensure it handles relative and absolute paths correctly across different OS environments (Linux/Windows).

## 6. Diagnostic Checklist
- [ ] `BaseScanner` contract implemented in `src/core/kernel/contracts/`.
- [ ] `DomainScanner` correctly ignores `__pycache__` and non-package folders.
- [ ] `DiscoveryError` provides the specific file path of the failing package.
- [ ] Scanning is performant (< 100ms for entire domain layer).
