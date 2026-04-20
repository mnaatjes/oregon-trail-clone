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

## 2. Theoretical Foundation: The Package Entry Point
In Python, an `__init__.py` file is more than just a marker; it is the **Entry Point** for a directory-based package. The scanner targets these files specifically because:
*   **Namespace Anchoring**: It marks the directory as a logical unit rather than a collection of loose files.
*   **Facade Pattern**: It allows the scanner to see "surface-level" definitions (like our Manifest) without immediately loading deep sub-modules.
*   **Metadata Storage**: It provides a standardized location for custom "Dunder" variables.

---

## 3. Infrastructure & Tooling

### A. Filesystem Navigation: `pathlib.Path`
*   **Tool**: `Path.rglob("__init__.py")`
*   **Input**: A filesystem directory path (e.g., `src/domain`).
*   **Output**: A generator of `Path` objects.
*   **Concept**: **Recursive Discovery**. We use `rglob` to find nested domains across `roots/`, `leaves/`, and `common/`.

### B. Reflection Phase 1: The Spec (The Blueprint)
*   **Tool**: `importlib.util.spec_from_file_location(name, path)`
*   **Input**: A logical name and a physical file path.
*   **Output**: A `ModuleSpec` object.
*   **Concept**: **The Blueprint**. The Spec is a passive object that knows *where* the code is but does **not** contain the code's logic or variables.
*   **Critical Properties**:
    *   `.origin`: The physical path (useful for error reporting).
    *   `.submodule_search_locations`: A list that, if populated, proves the directory is a valid **Package**.
    *   `.loader_state`: Usually `None` for standard loaders, but stores transient state for complex loading operations.

### C. Reflection Phase 2: The Module (The Reality)
*   **Tools**: `importlib.util.module_from_spec(spec)` and `spec.loader.exec_module(module)`
*   **Concept**: **The Live Object**. 
    1.  `module_from_spec`: Creates a blank namespace in memory.
    2.  `exec_module`: Triggers the "Ignition," executing the `__init__.py` code and populating the module's dictionary.
*   **Bytecode Caching**: Upon execution, Python generates a "Precompiled Bytecode Tree" (`.pyc` file in `__pycache__`). This skips the parsing/compilation phase on subsequent boots, significantly improving performance.

### D. Attribute Extraction: `getattr` & `inspect`
*   **Tool**: `getattr(module, "__CONTEXT__", None)`
*   **Concept**: **The Manifest Pattern**. 
    *   A **Manifest** is an architectural "shipping label" (`__CONTEXT__`) that declares a domain's content (Priority, Intent, Requirements) before it is fully integrated.
    *   **Custom Dunders**: We use double-under names (`__CONTEXT__`) to distinguish orchestration metadata from standard business logic.
*   **Deep Inspection**:
    ```python
    # See all variables and imports defined in the file
    all_content = vars(module) 
    
    # Identify classes explicitly
    import inspect
    classes = inspect.getmembers(module, inspect.isclass)
    ```

---

## 4. Structural Design

### Location (Pillar Mirroring)
*   **Path**: `src/engine/domain/scanner.py`
*   **Role**: `scanner` (Utility service)

### Naming Conventions & Hazards
When using `spec_from_file_location`, the `name` argument should be a clean logical identifier (e.g., `domain.root.test_package`). 
*   **The Hazard**: If the name includes `__init__.py` (e.g., `test_package.__init__`), the `spec.parent` property will incorrectly split the "Unit," which can break relative imports inside the domain.

### The Base Contract
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

---

## 5. Integration & Usage

### Usage with DomainOrchestrator
The `DomainScanner` is a stateless service injected into the `DomainOrchestrator`. It provides the `List[DomainContext]` required for the Orchestrator to build its **Priority Graph**.

### Separation of Concerns
*   **Scanner**: Handles Filesystem IO and Reflection (The "Prospector").
*   **Orchestrator**: Handles the Boot Sequence and Logic (The "Conductor").

---

## 6. Testing & Prototyping

### Tools for Verification
*   **`pytest` `tmp_path`**: Create isolated, temporary domain folders.
*   **`rich.inspect(module, methods=True)`**: Use this during prototyping to see the "Guts" of what was captured (attributes, `__dict__`, and Manifests).

### Diagnostic Checklist
- [ ] `DomainScanner` resolves absolute paths to prevent "Import Identity Mismatch."
- [ ] `DiscoveryError` provides specific file paths and line numbers if possible.
- [ ] The scanner ignores `__pycache__` and non-package folders automatically.
- [ ] `__CONTEXT__` validation ensures the object is an instance of `DomainContext`.
