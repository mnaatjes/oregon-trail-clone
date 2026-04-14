# Glossary

This document defines the architectural terms and design patterns used in the Oregon Trail engine. Using industry-standard terminology ensures consistency and clarity for developers.

## A
### Architecture Contract (Service Contract)
A formal definition of the "plug shape" that a module or domain must take to be compatible with the engine. It dictates the required interfaces (Protocols) that a component must implement to "sign the contract" with the system.

## C
### Component Template
A reusable structural pattern that defines the mandatory files, classes, or interfaces that a module must implement. It acts as a "scaffold" for new features, ensuring consistency across a large codebase.

### Contract-First Design
A development methodology where the interfaces and interaction rules (the "contracts") are defined before writing any implementation logic. This ensures that different systems (e.g., Health and Character domains) can integrate seamlessly.

## D
### Dependency Injection (DI) Container
A central object (often called a `ServiceContainer`) that manages the instantiation and lifecycle of services. Instead of components creating their own dependencies, the container "injects" them, allowing for easier testing and modularity.

### Domain Archetype (System Archetype)
A structural template or "recipe" that mandates every functional sub-system must implement a specific set of components (e.g., Blueprint, State, Logic, Service). This ensures that all domains are structurally identical from the engine's perspective.

### Domain-Driven Design (DDD)
An approach to software development that centers the design on the "Domain" (the core logic of the Oregon Trail). It uses concepts like **Entities**, **Value Objects**, and **Bounded Contexts** to organize complex logic.

## I
### Inversion of Control (IoC)
An architectural principle where the flow of the program is inverted: instead of the domain logic calling the framework, the framework (the engine) calls the domain logic via predefined contracts (the Domain Protocol).

## M
### Microkernel Architecture
An architectural pattern that separates a minimal functional core (the kernel) from extended game logic and features (plugins). In this project, the `ServiceContainer` and `Engine` act as the kernel, while domain packages like `health` and `character` act as plugins.

### Modular Architecture
An industry-standard practice of breaking a system into independent, interchangeable parts with strict boundaries. This enforces the "Zero-Dependency Leaf Policy," ensuring that individual domain packages (like `health`) remain isolated and testable.

### Modular Kernel (Orchestrator)
The core "Engine" that coordinates the execution of various domains without knowing their internal details. It interacts only with the **Architecture Contracts** (Ports) to trigger game logic.

## P
### Platform-Oriented Architecture
A design philosophy where the system is built as a reusable "Platform" (the Engine) that provides core services (lifecycle, storage, events), while specific game mechanics are implemented as "Applications" or "Features" that run on top of it.

## S
### Screaming Architecture
An organizational pattern where the folder structure "screams" the purpose of the application (e.g., `domain/health/`, `domain/character/`) rather than the technical tools used (e.g., `models/`, `views/`, `controllers/`).

### Service Provider Pattern
A pattern used to handle the two-phase lifecycle (**Register** and **Boot**) of a module. Service Providers are responsible for wiring a domain's logic and assets into the **DI Container**.

### Standardized Component Archetype
An architectural pattern that mandates a uniform internal structure and interface for all components within a system. This ensures predictable integration and enables polymorphic orchestration by the host environment or engine.

## U
### Universal Domain Blueprint (UDB)
A project-specific internal term for the implementation of a **Standardized Component Archetype**. It mandates that every domain package (e.g., `health`, `character`) follows a specific structural contract (Assets -> Registry -> Service -> Provider) to ensure compatibility with the Oregon Trail engine.
