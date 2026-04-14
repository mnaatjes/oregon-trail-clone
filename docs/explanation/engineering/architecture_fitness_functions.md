# Architecture Fitness Functions

Moving from "simple tests" to "Architecture-as-Code" (often called Architecture Fitness Functions) requires a shift in how we treat the test suite itself.

 1. Defining Constants: The "Source of Truth"
  I recommend placing architecture-wide constants in a tests/integration/architecture/constants.py file and
  exposing them via fixtures in conftest.py.

2. Organizing for Readability: The "Guard" Pattern
  To stop the tests from looking "jumbled," split them by Concern rather than by Component. Instead of one
  test_domain_integrity.py, use a modular structure:

```text
.tests/integration/architecture/
   ├── conftest.py          # Domain discovery fixtures
   ├── helpers.py           # Shared logic (check_naming, check_inheritance)
   ├── constants.py         # The "Source of Truth" for the UDB
   ├── test_structure.py    # File/Folder existence & __init__.py exports
   ├── test_contracts.py    # Inheritance, Immutability (@frozen), Protocols
   └── test_dependencies.py # Zero-Dependency Leaf Policy & Circular Imports
```
 3. Failure Format: "Reports, Not Just Stack Traces"
  For architecture tests, do not use pytest.raises. That is for testing code behavior. For architecture, you want
  Diagnostic Failures.

   * Format: Use pytest.fail() with a structured, multi-line string. It should feel like a "Linter Report."
   * Recommendation: Develop a helper that aggregates "Architecture Violations." If a domain is missing three
     files, don't fail three times; fail once with a report of all three missing files.
   * Unification: Use a helper in conftest.py or a dedicated helpers.py that formats the output using rich style or
     a clean ASCII box.