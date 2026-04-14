# Domain Protocol

Set of rules that dictates how an object is allowed to move through the system.

By defining these "plug-shapes," you ensure that a Blueprint can never accidentally be modified by a Service, and a Value Object can never be confused with a stateful Entity.Here is the extrapolation of those relationships and the "Interface Points" for each contract.1. The Contract Relationship MapContractPrimary "Plug" PartnerInteraction TypeConstraintDomainBlueprintRegistryFetch-OnlyMust be immutable; cannot be instantiated by Services.DomainValueObjectEntityCompositionIdentitiless; replaced entirely rather than updated.DomainStateServiceMutationMust be owned by an Entity; can be cloned for snapshots.DomainEntityServiceOrchestrationThe only component with a UID; the target of Service logic.2. Defining the "Plug Shapes"A. The Blueprint ↔ Registry PlugThe Registry is the only component allowed to "hold" the master list of Blueprints.Rule: If a Service needs a Blueprint, it must ask the Registry. It cannot "make" one.Rigidity: Prevents "Magic Numbers" from being hardcoded in your logic.B. The State ↔ Service PlugThe Service is the "Surgeon" for the State.Rule: An Entity provides its DomainState to a Service. The Service returns a modified version or updates it in place.Rigidity: The Entity itself remains "Anemic" (it doesn't have heal() or starve() methods); the Service holds the rules.C. The Value Object ↔ Entity PlugThe Value Object is the "Passport" of the Entity.Rule: Value Objects are "Pass-by-Value." If a character changes their name, the Service replaces the CharacterIdentity object entirely.Rigidity: Prevents accidental side effects where changing one attribute ripples through the system unexpectedly.3. The "Rigorous Architecture" LifecycleUsing your Oregon Trail domains (Health, Character, Wagon), every interaction follows this standardized "Plug" flow:Request: The Engine (Controller) triggers an event (e.g., "Daily Tick").Resolution: The Registry provides the necessary Blueprints (e.g., "Dysentery").Access: The Service grabs the Entity (e.g., "Player").Transformation: The Service applies the Blueprint logic to the Entity's State (e.g., state.hp -= blueprint.damage).Validation: The State contract ensures the new values are mathematically sound.4. How to Enforce This (The "Linter" Strategy)To make this "hard to confuse," you can use Python's Type Hinting and Generics to enforce these plugs at the code level:

### Example Enforcement

```py
# The Service only accepts a specific type of Entity and State
class CharacterService:
    def process_injury(self, target: DomainEntity, injury: DomainBlueprint):
        # target.state is guaranteed to be a DomainState via the contract
        # injury is guaranteed to be a DomainBlueprint
        pass
```

Why this is a "Sound Choice":
This creates Structural Documentation. A new developer (or an AI agent) looking at your code doesn't need to guess how to add a "Weather" system. They see the "Plug Shapes" and know:

Create a WeatherBlueprint (assets).

Create a WeatherState (to track current storms).

Create a WeatherService (to bridge the two).

Extrapolation Summary:
You are moving from "Writing a Game" to "Building a Game Engine." This framework—tellurion—is becoming a platform where the rules of the Oregon Trail are just one possible "Implementation" of these four core contracts.

Contract,"Primary ""Plug"" Partner",Interaction Type,Constraint
DomainBlueprint,Registry,Fetch-Only,Must be immutable; cannot be instantiated by Services.
DomainValueObject,Entity,Composition,Identitiless; replaced entirely rather than updated.
DomainState,Logic,Mutation,Must be owned by an Entity; can be cloned for snapshots.
DomainEntity,Service,Orchestration,The only component with a UID; the target of Service logic.

Contract,Plug-Partner,Nature of Interaction,Semantic Clarity
DomainState,Logic,Internal/Functional,"State is ""processed"" by pure logic functions."
DomainEntity,Service,External/Orchestral,"Entities are ""managed"" by the service provider."

2. Logic vs. Service: The "Functional" Distinction
Following your Internal Package Blueprint, logic.py contains pure functions. These functions should be "Anemic-Friendly," meaning they don't care about the Service Container or the Database; they only care about the math.

The State ↔ Logic Relationship:
Logic takes a DomainState, applies a Blueprint, and returns a new (or modified) DomainState.

Semantic: "The Logic calculates the result of the infection on the health state."

The Entity ↔ Service Relationship:
The Service coordinates the world. it fetches the Entity from storage, passes its state into the Logic, and saves the result.

Semantic: "The HealthService manages the character's recovery process."

3. Is it less intuitive?
Actually, it is more intuitive for a "Builder" mindset. It creates a hierarchy of responsibility:

Service (The Manager): Knows when to do something and who to do it to.

Logic (The Specialist): Knows exactly how to calculate the change.

State (The Patient): Holds the data while it's being operated on.

If you say "State interacts with Logic," you are emphasizing that the Rules (Logic) are what change the Status (State). This prevents your Services from becoming "Fat" with math and keeps your Logic from becoming "Fat" with orchestration.

4. Implementation Example
In your src/domain/health/ package, it would look like this:

```py
# logic.py (Pure Domain Logic)
def calculate_starvation(state: CharacterState, blueprint: MaladyBlueprint):
    # This function ONLY sees the State and the Blueprint
    state.hp -= blueprint.tick_damage
    return state

# services.py (The Orchestrator)
class HealthService:
    def process_daily_health(self, character: Character):
        # The Service manages the ENTITY
        blueprint = self.registry.get("starvation")
        
        # The LOGIC manages the STATE
        logic.calculate_starvation(character.state, blueprint)
```

The Verdict on Your Lexicon
DomainState ↔ Logic: This is a Mathematical relationship. (Pure, predictable, testable).

DomainEntity ↔ Service: This is a Managerial relationship. (Stateful, registry-aware, event-driven).

This distinction is extremely powerful for TDD. You can test your logic.py by passing in dummy DomainState objects without ever needing to boot the ServiceContainer or create a full Character entity.

## Protocol Enforcement

In Python, you can enforce this "Domain Protocol" using a combination of Abstract Base Classes (ABC), Generics (TypeVar), and Structural Subtyping (Protocol).

Since you are building the tellurion framework to be a rigorous engine, you want more than just documentation—you want the code to "refuse to compile" (or fail linting) if a Service tries to plug into a Blueprint incorrectly.

1. The "Interface Recipe" (The Protocol)
In Python, typing.Protocol defines a Structural Contract. Unlike a standard class, it says: "I don't care who your parents are; if you have these specific methods and properties, you are a valid partner for this plug."

We can define a DomainPackageProtocol that enforces the relationship between your four core components.

```py
from typing import Protocol, TypeVar, Generic, runtime_checkable
from src.core.contracts import DomainEntity, DomainState, DomainBlueprint

# Define Generics so the Protocol knows which "Flavor" of domain it is checking
E = TypeVar("E", bound=DomainEntity)
S = TypeVar("S", bound=DomainState)
B = TypeVar("B", bound=DomainBlueprint)

@runtime_checkable
class DomainBinding(Protocol[E, S, B]):
    """
    The 'Recipe' for a valid Tellurion Domain Package.
    Enforces the relationship between Entity, State, and Blueprint.
    """
    def orchestrate(self, entity: E) -> None: 
        """Services must orchestrate Entities."""
        ...

    def transform(self, state: S, blueprint: B) -> S:
        """Logic must transform State using a Blueprint."""
        ...
```

2. Enforcing the "Plug Shapes" via TypeVars
To make the "plug-shapes" rigid, you use Bound TypeVars in your base classes. This ensures that a HealthService can only accept a CharacterEntity and never accidentally a WagonEntity.

#### The Service "Plug" (Orchestration)

```py
# src/core/contracts/service.py
from typing import Generic, TypeVar
from .entity import DomainEntity

T = TypeVar("T", bound=DomainEntity)

class BaseDomainService(Generic[T], ABC):
    @abstractmethod
    def execute_logic(self, entity: T) -> None:
        """Enforces that this service ONLY plugs into its specific Entity type."""
        pass
```

#### The Logic "Plug" (Transformation)

```py
# src/domain/health/logic.py
from .models import CharacterState, MaladyBlueprint

def apply_infection(state: CharacterState, blueprint: MaladyBlueprint) -> CharacterState:
    """
    The 'Plug' is enforced by the type hints. 
    Mypy/Pyright will error if you pass a 'WagonState' here.
    """
    return state.clone(current_hp=state.current_hp - blueprint.potency)
```

3. Verification: The "Architectural Linter"
You can use isinstance(obj, DomainBinding) in your Meta-Tests to ensure that every package in src/domain/ has correctly "wired" its components.

Component,"Role in the ""Recipe""",Enforcement Mechanism
Generics,"The ""Plug Shape""",Ensures only compatible types connect.
Protocols,"The ""Interface""",Defines the behavior (Orchestrate vs Transform).
ABC,"The ""Base""","Prevents ""naked"" instantiation."

4. Why this is your "Domain Protocol"
By implementing this, you aren't just writing code; you are writing a Specification.

If you decide to add a Weather domain:

If your WeatherService tries to use CharacterState, the IDE highlights it in red.

If your WeatherLogic tries to modify a Blueprint, Python raises a FrozenInstanceError.

If your WeatherEntity is missing a UID, the BaseEntity constructor fails.

The Final "Lexicon" of Plugs:
Service ↔ Entity: The Control Port.

Logic ↔ State: The Data Port.

Registry ↔ Blueprint: The Source Port.

## Domain Binding Continued

The DomainBinding is best understood as a Meta-Contract. It is not a data type or a service itself; it is the Architectural Glue that defines how a specific Domain Package (like Health or Character) must be wired together to be compatible with the tellurion engine.

1. Where does it live?
It belongs in src/core/contracts/. Specifically, I would place it in src/core/contracts/domain.py.

It is a Core Component because it defines the "Interface for a Domain." It acts as the blueprint for the package itself, rather than a blueprint for a game object.

2. The Relationship: Service, Logic, and Binding
You are exactly right: orchestrate() is the signature of the Service, and transform() is the signature of the Logic.

However, we don't "inject" them into the Binding. Instead, the Service and Logic satisfy the Binding. Think of the Binding as a "Job Description." Any Service or Logic function that follows those rules "fits" the description.

The Protocol Definition (src/core/contracts/domain.py)

```py
from typing import Protocol, TypeVar, runtime_checkable
from .entity import DomainEntity
from .blueprint import DomainBlueprint
from .state import DomainState

E = TypeVar("E", bound=DomainEntity, contravariant=True)
S = TypeVar("S", bound=DomainState)
B = TypeVar("B", bound=DomainBlueprint, contravariant=True)

@runtime_checkable
class DomainBinding(Protocol[E, S, B]):
    """
    The 'Job Description' for a Tellurion Domain.
    """
    def orchestrate(self, entity: E) -> None: ...
    def transform(self, state: S, blueprint: B) -> S: ...
```

3. How the "Injection" Happens
Since you are using a ServiceContainer (Dependency Injection Hub), the "Injection" happens at the ServiceProvider level. When you boot your game, you register a Service that "binds" a specific Entity to a specific Logic.

The Implementation (src/domain/health/services.py)
Your HealthService doesn't just inherit from BaseService; it "implements" the orchestrate part of the recipe.

```py
from .logic import apply_damage # This is your transform() implementation

class HealthService(BaseDomainService[CharacterEntity]):
    
    def orchestrate(self, entity: CharacterEntity) -> None:
        """
        The Orchestrator implementation.
        It pulls the Blueprint and calls the Logic.
        """
        blueprint = self.registry.get("dysentery")
        
        # This is where the Logic is 'injected' or called
        entity.state = apply_damage(entity.state, blueprint)
```

4. Why this is an "Abstracted Contract"
The DomainBinding allows your Engine (Controller) to be completely agnostic of what a domain actually does. The Engine doesn't need to know about "Health" or "Wagons"; it only needs to know how to call orchestrate().

The Engine's Perspective:

```py
# src/engine/orchestrator.py

class GameEngine:
    def process_tick(self, domain: DomainBinding):
        """
        The engine can take ANY domain that follows the recipe.
        """
        for entity in self.get_active_entities(domain):
            domain.orchestrate(entity)
```

5. Summary of the "Plug" Architecture
The Binding (core/contracts): Defines the shape of the plug (The Protocol).

The Logic (domain/health/logic.py): Implements the transform() logic (The Math).

The Service (domain/health/services.py): Implements the orchestrate() behavior (The Management).

The Container (core/container.py): Acts as the switchboard that connects the Engine to the specific Domain Service.

By using DomainBinding, you have created a system where you can literally "plug and play" new game mechanics. If you want to add a "Morale" system, you just build a package that fulfills the DomainBinding protocol, and the Engine will know exactly how to run it.

### Contracts Directory Structure for Domains

Based on your Linux environment and the Screaming Architecture directives, moving these into a dedicated domain/ subdirectory within contracts is the right call. It keeps the core "rules of the game" isolated from other technical contracts (like provider.py).

1. Proposed Directory Structure
Move the domain-specific base classes into a subdirectory and use __init__.py to export them as the public API for the core.contracts package.

```
src/core/contracts/
├── domain/
│   ├── __init__.py      <-- Exports all below
│   ├── binding.py       <-- The "DomainBinding" Protocol
│   ├── blueprint.py
│   ├── entity.py
│   ├── state.py
│   └── value_object.py
├── provider.py
└── registry.py
```

Under this structure, your file should be named binding.py.

2. Why "DomainBinding" vs. "Domain"?
The choice of "Binding" over "Domain" or "Package" is a deliberate architectural distinction based on Intent and Ambiguity:

Avoids Name Collisions: You already have a top-level directory called src/domain/. Calling a class Domain creates cognitive (and potentially namespace) friction. In code, from domain.health import ... vs. class Domain: is confusing.

Indicates Action (The "Plug"): A "Domain" is a noun—a place where things live. A "Binding" is a functional concept. It represents the act of tying together your disparate parts (Entity, State, Blueprint) into a single functional unit that the Engine can talk to.

The "Glue" Factor: In design patterns, a "Binding" usually refers to the mapping between an interface and its implementation. This class is exactly that: it defines how the Engine (the interface) binds to the Logic/Service (the implementation).

3. The Meta-Contract: src/core/contracts/domain/binding.py
To make this truly a "recipe," the binding.py file should use the DomainBinding class to define the structural requirements.

```py
# src/core/contracts/domain/binding.py

from typing import Protocol, TypeVar, runtime_checkable
from .entity import DomainEntity
from .state import DomainState
from .blueprint import DomainBlueprint

# Generics to ensure the plug-shapes match
E = TypeVar("E", bound=DomainEntity)
S = TypeVar("S", bound=DomainState)
B = TypeVar("B", bound=DomainBlueprint)

@runtime_checkable
class DomainBinding(Protocol[E, S, B]):
    """
    The Protocol defining the structural interface for a Domain Pillar.
    It binds the Orchestrator (Service) to the Transformer (Logic).
    """
    def orchestrate(self, entity: E) -> None: 
        """Implementation found in the Domain Service."""
        ...

    def transform(self, state: S, blueprint: B) -> S:
        """Implementation found in the Domain Logic."""
        ...
```

4. Implementation in __init__.py
To maintain the clean import style you likely want, your src/core/contracts/domain/__init__.py should look like this:

```py
from .binding import DomainBinding
from .blueprint import DomainBlueprint
from .entity import DomainEntity
from .state import DomainState
from .value_object import DomainValueObject

__all__ = [
    "DomainBinding",
    "DomainBlueprint",
    "DomainEntity",
    "DomainState",
    "DomainValueObject",
]
```

This setup allows the rest of your app to simply call from src.core.contracts.domain import DomainBinding. It treats the directory as a single cohesive unit of "Domain Rules."