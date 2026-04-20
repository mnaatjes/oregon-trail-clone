# src/core/kernel/contracts/factory.py

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Dict, Generic, Type

T = TypeVar("T")

class BaseFactory(ABC, Generic[T]):
    """
    Abstract base orchestrator for the standardized construction of project entities.

    Implementation Guidelines:
    1. Bind the Product Type: When inheriting, specify the concrete class or interface 
       in the brackets, e.g., `class CharacterFactory(BaseFactory[Character]):`.
    2. Define Target: The `target` property MUST return the concrete class object 
       (the constructor) for the same type bound to 'T'. This enables runtime 
       validation and automated instantiation logic.
    3. Method Implementation: Implement the abstract lifecycle hooks (prepare, 
       validate, instantiate, finalize) to define the specific assembly logic 
       for the product.

    The `build()` method enforces a strict lifecycle:
    Prepare (Sanitization) -> Validate (Guards) -> Instantiate (Creation) -> Finalize (Polish).
    """

    @property
    @abstractmethod
    def specification(self) -> Dict[str, Any]:
        """Returns a schema or template of the data required to build the product."""

    @property
    @abstractmethod
    def target(self) -> Type[T]:
        """Returns the Class or Interface that the product is guaranteed to implement."""

    @abstractmethod
    def validate(self, **data: Any) -> None:
        """Validate product"""
        pass

    @abstractmethod
    def prepare(self, **kwargs) -> Dict[str, Any]:
        """A hook to sanitize or transform input data"""
        pass

    @abstractmethod
    def instantiate(self, **kwargs) -> T:
        """Produces the Class, Object, or Interface defined in target"""
        pass

    @abstractmethod
    def finalize(self, instance:Any) -> T:
        """A hook for logic that must occur after the object exists but before it is returned to the caller"""
        pass

    def build(self, **raw: Any) -> T:
        """
        Concrete orchestrator
        Enforces the sequence of construction laws
        - prepare()
        - validate()
        - initialize()
        - finalize()
        """
        # 1. Transform Raw Data
        processed = self.prepare(**raw)

        # Gatekeeper
        self.validate(**processed)

        # 2. Create Object/Class instance
        instance = self.instantiate(**processed)

        # 3. Implement Post-Processing and return
        return self.finalize(instance)