1. Is "Framework-Oriented" a Pattern or Practice?

It is a Practice that utilizes a combination of Patterns to create a custom Architecture.

    The Architecture: It is a variant of Plugin Architecture. By standardizing how a domain is "plugged in," the core of your game (the Engine) doesn't actually know what a "Malady" or "Weather" is—it just knows how to boot a Provider.

    The Patterns: It primarily uses the Inversion of Control (IoC) and Dependency Injection patterns.

    The Practice: It is the discipline of treating your game systems as "Library Code" and your Engine as "Client Code."