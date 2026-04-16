# Domain Testing Regime: Fitness Functions

To maintain the **Universal Domain Blueprint (UDB)** and **Zero-Dependency Leaf Policy**, the project employs "Architecture-as-Code" (Fitness Functions). These tests don't verify game behavior; they verify that the code *itself* follows the prescribed structural rules.

## 1. Organization: The "Guard" Pattern

Architectural tests are organized by **Concern** rather than by **Component** to keep the suite readable and modular.

```text
tests/integration/architecture/
├── conftest.py          # Domain discovery fixtures & shared providers
├── helpers.py           # Diagnostic failure formatting & assertion logic
├── constants.py         # The "Source of Truth" for UDB requirements
├── test_structure.py    # File/Folder existence & __init__.py exports
├── test_contracts.py    # Inheritance, Immutability (@frozen), Protocols
└── test_dependencies.py # Zero-Dependency Leaf Policy & Circular Imports
```

## 2. The Source of Truth (`constants.py`)

All architectural requirements are centralized here. If the UDB evolves (e.g., adding a new required file), updating this one file updates the entire enforcement suite.

```python
DOMAIN_PATH = "src/domain"
REQUIRED_COMPONENTS = [
    "models.py", 
    "services.py", 
    "registry.py", 
    "exceptions.py", 
    "constants.py"
]
SERVICE_SUFFIX = "Service"
ENTITY_DECORATOR = "dataclass"
# Mapping of component types to their required base classes
CONTRACT_MAP = {
    "Registry": "BaseRegistry",
    "Provider": "BaseServiceProvider"
}
```

## 3. Dynamic Discovery (`conftest.py`)

Tests use **Parameterized Fixtures** to automatically discover and test every domain package. This ensures that adding a new domain folder `src/domain/inventory` automatically triggers a full suite of integrity checks for that domain without manual test updates.

```python
@pytest.fixture(params=get_all_domains())
def domain_name(request):
    """Runs the dependent test once for every domain found in src/domain."""
    return request.param
```

## 4. Diagnostic Failures: "Reports, Not Stack Traces"

Unlike behavioral tests, architectural failures should provide a "Linter Report" style output. Use `pytest.fail()` with a structured message instead of `assert` or `pytest.raises`.

### The Violation Report Format
```text
[ARCHITECTURE VIOLATION] in Domain: 'health'
Category: Structural Integrity
Message:  Missing required component 'registry.py'
Expected: src/domain/health/registry.py
```

### Helper Implementation (`helpers.py`)
```python
def format_architecture_violation(domain: str, category: str, message: str, expected_loc: str = None):
    report = [
        f"\n[ARCHITECTURE VIOLATION] in Domain: '{domain}'",
        f"Category: {category}",
        f"Message:  {message}",
    ]
    if expected_loc:
        report.append(f"Expected: {expected_loc}")
    return "\n".join(report)
```

## 5. Summary of Enforcements

| Test File | Enforcement |
| :--- | :--- |
| `test_structure.py` | Presence of all 5 UDB files; Public API (`__all__`) in `__init__.py`. |
| `test_contracts.py` | `@dataclass(frozen=True)` for Models; `Service` suffix; Inheritance from Base classes. |
| `test_dependencies.py` | Zero-dependency leaf policy; Prohibiting circular imports between domains. |
