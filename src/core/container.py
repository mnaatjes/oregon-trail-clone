from typing import Dict, Any, Union, Type, TypeVar, Callable, cast

# T represents the generic type of the class being resolved
T = TypeVar('T')

class ServiceContainer:
    """
    The Dependency Injection Hub.
    Handles service registration, resolution, and singleton management 
    using both string keys and class-type keys.
    """

    def __init__(self):
        # Stores either the raw object or a factory function (lambda)
        # Keys can be strings ("json_loader") or classes (HealthService)
        self._services: Dict[Union[str, Type], Any] = {}
        
        # Caches instantiated singletons to ensure the same instance 
        # is returned throughout the application lifecycle.
        self._instances: Dict[Union[str, Type], Any] = {}

    def register(self, key: Union[str, Type[T]], service: Any) -> None:
        """
        Bind a service to the container.
        
        Args:
            key: A unique string identifier or the Class type itself.
            service: A live object, a class definition, or a factory function.
        """
        self._services[key] = service

    def bind(self, key: Union[str, Type[T]], service: Any) -> None:
        """Alias for register, for more intuitive access."""
        self.register(key, service)

    def resolve(self, key: Union[str, Type[T]]) -> T:
        """
        Retrieve a service from the container. 
        If the service was registered as a factory, it is executed and cached.
        
        Returns:
            The instantiated service, type-hinted to the requested Class.
        """
        # 1. Return cached instance if it exists
        if key in self._instances:
            return self._instances[key]

        # 2. Check if the service is registered at all
        if key not in self._services:
            raise KeyError(f"Service '{key}' not found in the container.")

        creator = self._services[key]

        # 3. Handle instantiation
        # If the creator is a callable (like a lambda), we pass 'self' (the container)
        # to allow for nested dependency resolution.
        if callable(creator):
            instance = creator(self)
        else:
            instance = creator

        # 4. Cache as a singleton and return
        self._instances[key] = instance
        return cast(T, self._instances[key])

    def get(self, key: Union[str, Type[T]]) -> T:
        """Alias for resolve, for more intuitive access."""
        return self.resolve(key)

    def has(self, key: Union[str, Type]) -> bool:
        """Check if a service is registered in the container."""
        return key in self._services
    
    def all_services(self) -> Dict[Union[str, Type], Any]:
        """Return a dictionary of all registered services (for debugging)."""
        return self._services
    
    def all_instances(self) -> Dict[Union[str, Type], Any]:
        """Return a dictionary of all instantiated singletons (for debugging)."""
        return self._instances
    
    def clear(self) -> None:
        """Clear all registered services and cached instances (useful for testing)."""
        self._services.clear()
        self._instances.clear()