# Game Character Domains and Systems



## Charater Identity

### Questions

1. Should we treat `age` as an *indentity* or *state* property? 
> * `age` is a derived property from DOB

### Character DataClasses
```mermaid
classDiagram

    class CharacterIdentity {
        <<DataClass>>
        +str fname
        +str lname
        +str profession
        +str dob
        +str gender
        +int height
    }

    class Player {
        +list companions
    }

    class Companion {
    }

    CharacterIdentity <|-- Player
    CharacterIdentity <|-- Companion

```

### Notes

### Questions

1. Do we need to track coordinates/location?
    - Are coordinates/location part of "State"? Yes

## Top-Level Character diagram

```mermaid
classDiagram
    class Character {
        +CharacterIdentity identity
        +CharacterStats stats
        +CharacterState state
    }

    class CharacterIdentity { <<Fixed>> }
    class CharacterStats { <<Fixed>> }
    class CharacterState { <<Stateful>> }

    Character *-- CharacterIdentity
    Character *-- CharacterStats
    Character *-- CharacterState
```
## Physical and Temporal Systems

```mermaid
classDiagram
    class CharacterState {
        +float current_weight
        +int time_on_trail
        +CharacterHealth health
        +current_age() int
        +is_obese() bool
    }

    class CharacterHealth {
        %% Details hidden here, focused on State ownership
    }

    CharacterState *-- CharacterHealth
```

## Medical and Malady System

```mermaid
classDiagram
    class CharacterHealth {
        +int current_hp
        +list maladies
        +is_alive() bool
        +is_sick() bool
        +is_injured() bool
        is_conscious() bool
        is_sane() bool
    }

    class Malady {
        <<Abstract>>
        +str name
        +int damage_per_day
        +on_tick(health)
    }

    class Disease {
        +float contagious_factor
    }

    class Injury {
        +bool requires_splint
    }

    CharacterHealth "1" *-- "many" Malady
    Malady <|-- Disease
    Malady <|-- Injury
```
### Health Infrastructure

```mermaid
classDiagram
    class MaladyRegistry {
        +get_malady(name) Malady
    }

    class HealthService {
        +resolve_tick(character)
        +apply_medicine(character, item)
    }

    HealthService ..> CharacterHealth : manipulates
    HealthService ..> MaladyRegistry : fetches from
```

## Infrastructural Entities

```mermaid
classDiagram
    class Registry
    class CompanionRegistry
    class MaladyRegistry
```

## Service Providers