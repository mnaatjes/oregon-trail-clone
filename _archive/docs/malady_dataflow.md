1. The Raw Asset (The Blueprint)

    Entity: maladies.json

    Location: assets/maladies.json

    Role: A static JSON file containing the "base stats" for every possible ailment (e.g., base damage, contagion chance, name, description).

2. The Infrastructure Loader (The Reader)

    Entity: JSONLoader

    Location: src/storage/loaders.py

    Role: A technical utility that handles the OS-level task of opening the file and parsing the string into a Python dictionary. It doesn't know what a "Malady" is; it only knows how to read JSON.

3. The Domain Registry (The Catalog)

    Entity: MaladyRegistry

    Location: src/domain/health/registry.py

    Role:

        Input: Receives the raw dictionary from the loader.

        Hydration: Loops through the dict and instantiates concrete Disease or Injury objects (subclasses of the Malady ABC).

        Storage: Stores them in its private _maladies{} map.

        Function: Provides a get_template(malady_id) method that returns a copy (or prototype) of the requested ailment.

4. The Orchestrator (The Wiring)

    Entity: HealthServiceProvider

    Location: src/engine/providers.py (or src/main.py)

    Role:

        Calls JSONLoader.load("assets/maladies.json").

        Instantiates MaladyRegistry(data).

        Instantiates HealthService(registry=malady_registry).

        Registers these instances into the ServiceContainer.

5. The Runtime Environment (The Service Container)

    Entity: ServiceContainer

    Location: src/core/container.py

    Role: A central "hub" where the Engine or Controller can grab the fully prepared HealthService whenever a character steps on a rusty nail or drinks swamp water.

Summary of the Flow
Step	Action	Entity	Layer
1	Read File	JSONLoader	Storage/Infra
2	Create Templates	MaladyRegistry	Domain (Health)
3	Inject Registry	HealthServiceProvider	Engine/Core
4	Resolve & Use	HealthService	Domain (Health)
One Critical Builder Tip:

When the HealthService uses the MaladyRegistry to infect a character, make sure it creates a Deep Copy of the template.

    Why? If two characters have "Cholera" and they both point to the exact same object in the Registry, then changing the days_active for Character A will accidentally change it for Character B.


## Components

The Components of Your Blueprint
Component	Responsibility	Enforcement Method
Asset	Static JSON data	Schema Validation (JSONSchema)
Registry	Template Hydration	Inherit from BaseRegistry
Service	Rules/Logic	Inherit from BaseService
Provider	Injection/Wiring	Inherit from BaseServiceProvider