# Component Template

A **Component Template** is a concrete, implementation-oriented specification used to scaffold or generate a specific module. It provides a "starter kit" or "shell" that ensures every implementation follows the structural rules defined by the Architecture.

## Taxonomy

| Attribute | Classification |
| :--- | :--- |
| **Category** | **Structural Implementation Pattern** |
| **Abstraction** | **Concrete / Scaffold** |
| **Primary Goal** | Provide a **Standardized Layout** and **Implementation Shell** for features. |

## Role in Architecture

While the Archetype defines the "Law" (What it must be), the Template provides the "Blueprint" (How it is built). In the Oregon Trail project, the Component Template mandates the exact file structure and base classes for every domain package.

```mermaid
graph TD
    subgraph "Domain Package Template (src/domain/xyz/)"
        A[models.py]
        B[logic.py]
        C[service.py]
        D[provider.py]
        E[registry.py]
        F[exceptions.py]
    end

    A -->|State Data| C
    B -->|Rules| C
    D -->|Wires| C
    E -->|Loads| C
```

## Benefits

-   **Developer Velocity**: New domains can be scaffolded in seconds by following the template.
-   **Easier Maintenance**: A developer looking at the `health` domain knows exactly where to find the logic for the `wagon` domain, as the structure is identical.
-   **Boilerplate Reduction**: Base classes can provide common functionality, leaving the developer to focus on domain-specific code.

## Python Example: Implementing the Template

The template is often realized as a set of base classes that every new module must inherit from.

```python
# The Template provides the "Shell" (src/core/contracts/provider.py)
class BaseServiceProvider(ABC):
    """
    The Structural Shell for every domain provider.
    """
    def __init__(self, container: ServiceContainer):
        self.container = container

    @abstractmethod
    def register(self) -> None:
        """Mandatory registration phase."""
        pass

    @abstractmethod
    def boot(self) -> None:
        """Mandatory bootstrapping phase."""
        pass

# The specific implementation (src/domain/health/provider.py)
class HealthServiceProvider(BaseServiceProvider):
    def register(self):
        # Implementation of the registration phase
        self.container.bind("health_service", HealthService())

    def boot(self):
        # Implementation of the bootstrapping phase
        pass
```
