---
title: "Major Domains, Entities, and Objects (Apple II - 1985)"
description: "Analysis of the core domain entities and objects from the original 1985 Apple II version of The Oregon Trail."
type: "explanation"
status: "stable"
created_at: "2026-04-16 00:00:00"
updated_at: "2026-04-16 00:00:00"
owner: "Michael Naatjes"
tags: ["historical", "apple-ii", "1985", "entities"]
version: "0.1.0"
---

# Major Domains, Entities, and Objects (Apple II - 1985)

This document outlines the core domain entities and objects represented in the 1985 Apple II version of The Oregon Trail.

## 1. The Party
The central unit of the game, representing the pioneers traveling to Oregon.
- **Leader (Player):** The main character whose profession determines starting cash and score multiplier.
- **Companions:** Four named members. Their survival is critical for a high final score.
- **Health State:** Each member has an individual health level (Good, Fair, Poor, Very Poor, Dead).
- **Status Effects:** Diseases (Dysentery, Cholera, Typhoid, Measles) or injuries (Broken Leg, Exhaustion).

## 2. The Wagon
The primary container for all resources.
- **Inventory Items:**
    - **Oxen:** Pairs of oxen (yokes) that pull the wagon. If all die, the game ends.
    - **Food:** Pounds of rations. Consumed daily based on the "Rations" setting.
    - **Clothing:** Sets of clothes to protect against weather.
    - **Ammunition:** Boxes of 20 bullets for hunting and defense.
    - **Spare Parts:** Wagon Wheels, Wagon Axles, and Wagon Tongues.
- **Condition:** The wagon itself can break down (e.g., "Broken Wagon Tongue"), requiring a spare part or time to repair.

## 3. The Environment
- **Locations:**
    - **Settlements:** Forts (e.g., Fort Laramie) and Independence, MO. Places to buy supplies or talk to travelers.
    - **Landmarks:** Geographic features (e.g., Chimney Rock).
    - **River Crossings:** Strategic points requiring a crossing method (Ford, Caulk, Ferry).
- **Date/Time:** The game tracks the current day, month, and year (starting in 1848).
- **Weather:** Dynamic conditions (Sunny, Rain, Snow, Cold, Hot) that affect health and travel speed.

## 4. Economic Entities
- **Professions:** Banker ($1600, 1x score), Carpenter ($800, 2x score), Farmer ($400, 3x score).
- **Currency:** Cash used at general stores and for ferry fees.
- **Trading:** A system where players can exchange items with other travelers.
