---
title: "Game World Domains"
description: "Archived design document concerning game world domains and global dataclasses."
type: "explanation"
status: "depreciated"
created_at: "2026-04-16 04:00:00"
updated_at: "2026-04-16 04:00:00"
owner: "Michael Naatjes"
tags: [archived, design, legacy, world]
version: "0.1.0"
---

# Game World Domains

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
