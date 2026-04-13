# Architecture Contract Enforcement

How to ensure an architectural pattern is enforced.


## 1. ADR Documentation

## 2. Abstract Contracts

Aside from documentation or ADRs (Architectural Decision Records), you can enforce your standard through Code Contracts.

Abstract Base Classes (ABCs)

You can define a "contract" that every Provider must sign. If a new developer (or you, three months from now) tries to create a WeatherProvider but forgets the boot() method, the code will crash immediately upon start, telling you exactly what is missing.

```py
from abc import ABC, abstractmethod

class BaseServiceProvider(ABC):
    @staticmethod
    @abstractmethod
    def boot(container, loader):
        """Every domain MUST implement this method."""
        pass
```

## 3. Structural Typing

Structural Typing (Protocols)

Using typing.Protocol (PEP 544), you can define what a "Domain Package" should look like. This is "Static Enforcement." Your IDE (like VS Code or PyCharm) will highlight the code in red if your Provider doesn't match the expected shape before you even run the game.

What is Structural Typing?

Structural Typing is a system where the compatibility of two types is determined solely by their structure (their methods and attributes) rather than their explicit name or inheritance.

In languages like Java or C#, you usually use Nominal Typing: an object is only "of a type" if it explicitly says class MyClass implements MyInterface.

In Structural Typing (often called Static Duck Typing in Python), an object is "of a type" if it simply has the required parts. If it walks like a duck and quacks like a duck, the type-checker accepts it as a duck, even if it never formally signed a "Duck Contract."

In Python, we implement this using Protocols.

### Simple Example: The "Printer"

Imagine you want a function that can print any object, as long as that object has a .to_text() method.

```py
from typing import Protocol, runtime_checkable

@runtime_checkable
class Textable(Protocol):
    def to_text(self) -> str:
        ...

def display(obj: Textable):
    print(obj.to_text())

# These two classes have NO shared parent, but they "fit" the structure
class Book:
    def to_text(self): return "It was the best of times..."

class Note:
    def to_text(self): return "Buy milk."

display(Book()) # Works!
display(Note()) # Works!
```

## 4. Testing Regime

Test that all Domain Packages have providers

Since you have a tests/ directory, you can write a Meta-Test. This is a test that doesn't test game logic, but tests the Architecture itself.

```py
def test_all_domain_packages_have_providers():
    # Loop through src/domain/ folders
    # Check if a corresponding Provider exists in src/engine/providers/
    # If not, fail the test.
```