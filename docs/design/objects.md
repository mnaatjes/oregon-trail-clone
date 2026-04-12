# Oregon Trail Objects 

## Global Dataclasses

### Questions

1. What years will the game take place?
    - What rate will time progress?
    - What min and max year will we permit?

### Proposed Game Properties

```mermaid
classDiagram
    class GameDate {
        +int year
        +int month
        +int day
    }
```

## Charater Related Dataclasses

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

* `Age` is a derived property from `dob` (Date of Birth)

## State Management

### Questions

1. Do we need to track coordinates/location?
    - Are coordinates/location part of "State"?
2. Do we need an `is_alive` boolean?

### State Diagrams

```mermaid
classDiagram
    class State {
        <<Abstract>>
        +self update()
    }

    class CharacterState {
        
    }

    class CharacterStats {
        +int hp
        +int age
        +int speed
        +int agility
    }

    State <|-- CharacterState
```

### Health System

```mermaid
classDiagram
    class CharacterHealth {
        +list maladies
    }
    class Malady {
        <<Abstract>>
        +str name
        +str desc
        +int damage
        +int duration
    }

    class Injury
    class Disease
    class Sanity

    class MaladyResolver {
        <<Service>>
    }

    class SanityResolver {
        <<Service>>
    }

    Malady <|-- Injury
    Malady <|-- Disease
    Malady <|-- Sanity
```

## Infrastructural Entities

```mermaid
classDiagram
    class Registry
    class CompanionRegistry
    class MaladyRegistry
```

## Service Providers