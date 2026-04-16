---
title: "Game Character Domains and Systems"
description: "Archived design document regarding Character Identity, DataClasses, and Health Infrastructure."
type: "explanation"
status: "depreciated"
created_at: "2026-04-16 04:00:00"
updated_at: "2026-04-16 04:00:00"
owner: "Michael Naatjes"
tags: [archived, design, legacy, character]
version: "0.1.0"
---

# Game Character Domains and Systems



## Charater Identity

### Questions

1. Should we treat `age` as an *indentity* or *state* property? 
> * `age` is a derived property from DOB

### Character DataClasses
```mermaid
classDiagram
    class Profession {
        <<Blueprint>>
        +str slug
        +int starting_cash
    }

    class CharacterIdentity {
        <<ValueObject>>
        +str fname
        +str lname
        +Profession profession
    }

    class BaseCharacter {
        <<Abstract Entity>>
        +UUID uid
        +CharacterIdentity identity
        +int current_hp
    }

    class Player {
        +list companions
    }

    class Companion {
        +str loyalty_level
    }

    CharacterIdentity *-- Profession : contains
    BaseCharacter *-- CharacterIdentity : contains
    BaseCharacter <|-- Player : extends
    BaseCharacter <|-- Companion : extends

```

### Notes

### Questions

1. Do we need to track coordinates/location?
    - Are coordinates/location part of "State"? Yes

## Character / player Relationship

```mermaid
classDiagram
    class BaseCharacter {
        <<Abstract>>
        +UUID uid
        +CharacterIdentity identity
        +int current_hp
        +is_alive() bool
    }

    class Player {
        +Profession profession
        +list companions
        +manage_party()
    }

    class Companion {
        +str relationship_to_player
    }

    BaseCharacter <|-- Player : extends
    BaseCharacter <|-- Companion : extends
```

## Top-Level Character diagram

```mermaid
classDiagram
    class Character {
        <<DomainEntity>>
        +UUID uid
        +CharacterIdentity identity
        +CharacterStats stats
        +CharacterState state
    }

    class CharacterIdentity {
        <<DomainValueObject>>
        +str fname
        +str lname
        +Profession profession
    }

    class CharacterStats {
        <<DomainValueObject>>
        +int base_stamina
        +int medicine_skill
        +int repair_skill
    }

    class CharacterState {
        <<MutableState>>
        +int current_hp
        +float current_weight
        +int days_on_trail
        +CharacterHealth health
    }

    Character *-- CharacterIdentity
    Character *-- CharacterStats
    Character *-- CharacterState
```

> NOTE: Separation of Concerns
> * Stats represent Potential: *What can entity DO?*
> * Identity is static: *Who an entity IS?*
> * State is mutable: *How is an entity DOING?*

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
        +int immobility_period_days
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
    class Registry {<<Abstract>>}
    class CharacterRegistry
    class MaladyRegistry
```

## Domain Binding
```mermaid
classDiagram
    %% Core Contracts
    class DomainBinding~Entity, State, Blueprint~ {
        <<Protocol>>
        +orchestrate(Entity)
        +transform(State, Blueprint)
    }

    %% Character Domain Implementation
    class CharacterService {
        <<Service>>
        +orchestrate(Character)
    }

    class Character {
        <<DomainEntity>>
        +UUID uid
        +CharacterIdentity identity
        +CharacterStats stats
        +CharacterState state
    }

    class CharacterIdentity {
        <<DomainValueObject>>
        +str fname
        +str lname
        +Profession profession
    }

    class CharacterStats {
        <<DomainValueObject>>
        +int base_stamina
        +int medicine_skill
        +int repair_skill
    }

    class CharacterState {
        <<DomainState>>
        +int current_hp
        +float current_weight
        +int days_on_trail
    }

    class Profession {
        <<DomainBlueprint>>
        +str slug
        +int starting_cash
    }

    %% Relationships and Bindings
    DomainBinding <|.. CharacterService : satisfies
    CharacterService ..> Character : orchestrates
    CharacterService ..> CharacterLogic : uses transform()
    
    Character *-- CharacterIdentity
    Character *-- CharacterStats
    Character *-- CharacterState
    CharacterIdentity *-- Profession
    
    note for CharacterService "orchestrate() calls \nCharacterLogic.transform()"
```
---

### Relationships and Technical Implementation
```mermaid
graph TD
    subgraph Technical_Pillar [Technical Pillar: Core/Engine]
        Engine[Game Engine / Controller]
        DB_Protocol["DomainBinding (Protocol)"]
        Container[Service Container]
    end

    subgraph Domain_Pillar [Domain Pillar: src/domain/character/]
        Service[CharacterService]
        Logic[CharacterLogic / pure functions]
        
        subgraph Aggregate_Root [Character Entity]
            State[CharacterState]
            Identity[CharacterIdentity]
            Stats[CharacterStats]
        end
        
        Blueprint[Profession Blueprint]
    end

    %% Architectural Enforcement
    Engine -->|resolves| Container
    Container -->|returns| Service
    Engine -->|calls orchestrate| Service
    
    %% The Protocol "Plug"
    Service -.->|implements| DB_Protocol
    
    %% The Internal Protocol Flow
    Service -->|manages| Aggregate_Root
    Service -->|passes state to| Logic
    Logic -->|transforms| State
    Logic -.->|reads| Blueprint
    
    %% Constraints
    Identity -.->|immutable| Blueprint
    Stats -.->|derived from| Blueprint
```

## Service Providers

> ## TODOs
> * Declare abstract Service
> * Declare abstract Protocol
