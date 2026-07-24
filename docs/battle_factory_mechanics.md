# Battle Factory Mechanics

This document describes the Battle Factory rules currently implemented by the expansion. It is the reference point for adding modern Pokémon sets without changing the original Factory progression.

During initial set development, the code routes all progression rows to generated entries at the end of the Factory table. The pool and challenge rules remain in place while the generated roster is reviewed.

The main implementation is in `src/battle_factory.c`. The set data is in `src/data/battle_frontier/battle_frontier_mons.h`.

## The basic loop

The Factory is played in challenges of seven battles.

At the beginning of a challenge:

1. The game creates six rental Pokémon.
2. The player chooses three of them.
3. The game creates an opponent team.
4. The player battles seven trainers, one at a time.
5. After a win, the player can exchange rentals for Pokémon used by the opponent.

The current challenge number is calculated from the Factory win streak:

```text
challenge number = win streak / 7
```

The win streak and rental count are stored separately for each battle mode and level mode.

## What a set contains

Each entry in `gBattleFrontierMons` is one complete Pokémon set. It contains:

- Species
- Four moves
- Held item
- EV spread
- Nature
- Poké Ball

The Pokémon's level, IVs, personality, ability, and trainer information are added when the game creates the actual Pokémon.

Adding a new set normally means adding one entry to this table and one matching ID in `include/constants/battle_frontier_mons.h`.

## Set ordering and quality ranges

The set table is ordered deliberately. The Factory does not choose from the whole table every time.

For Level 50 mode, the initial rental ranges are:

| Challenge number | Normal range | Better range used by some rentals |
|---:|---:|---:|
| 0 | 110–199 | 162–266 |
| 1 | 162–266 | 267–371 |
| 2 | 267–371 | 372–467 |
| 3 | 372–467 | 468–563 |
| 4 | 468–563 | 564–659 |
| 5 | 564–659 | 660–755 |
| 6 | 660–755 | 372–849 |
| 7 and later | 372–849 | 372–849 |

Open Level mode starts at a later point in the table and uses the stronger ranges. Its ranges are:

| Challenge number | Normal range | Better range used by some rentals |
|---:|---:|---:|
| 0 | 372–467 | 468–563 |
| 1 | 468–563 | 564–659 |
| 2 | 564–659 | 660–755 |
| 3 | 660–755 | 372–881 |
| 4 and later | 372–881 | 372–881 |

After the final challenge range is reached, the Factory keeps using it rather than trying to access a range beyond the end of the table.

This ordering is part of the progression system. If we add Gen 9 sets, we need to decide which quality range each set belongs to. Adding sets in the wrong place can change the difficulty of existing challenges.

## Initial rental quality

The number of previous rentals affects the initial six rentals. This is separate from the win streak.

The current rental ranks are:

| Previous rentals | Rental rank |
|---:|---:|
| 0–14 | 0 |
| 15–21 | 1 |
| 22–28 | 2 |
| 29–35 | 3 |
| 36–42 | 4 |
| 43 or more | 5 |

The first `rental rank` Pokémon in the six-Pokémon draft are chosen from the next better quality range. The remaining Pokémon use the normal range for the current challenge.

This means repeated play gradually improves the quality of the starting draft, even before considering the win streak.

## Duplicate restrictions

The initial rental draft cannot contain two Pokémon of the same species or two Pokémon with the same held item.

Unown is excluded.

The opponent generation applies similar restrictions:

- No duplicate species on the opponent team.
- No duplicate held items, except that `ITEM_NONE` can repeat.
- No opponent species that matches any of the player's available rental species.
- High-tier Pokémon are excluded from Level 50 mode.

These restrictions are implemented in `GenerateInitialRentalMons` and `GenerateOpponentMons`.

## Opponent trainers

The opponent trainer is selected from a challenge-dependent trainer range.

The game avoids repeating a trainer within the current seven-battle challenge. The final battle of a challenge uses a harder trainer range.

After challenge 7, the hardest trainer range continues to be used.

The opponent's Pokémon are selected separately from the trainer. This means the trainer identity and the Pokémon sets are two different systems.

## IV quality

Factory IVs improve by challenge. The current fixed IV values are:

| Challenge index | Normal battle IVs | Final battle IVs |
|---:|---:|---:|
| 0 | 3 | 6 |
| 1 | 6 | 9 |
| 2 | 9 | 12 |
| 3 | 12 | 15 |
| 4 | 15 | 18 |
| 5 | 21 | 31 |
| 6 and later | 31 | 31 |

These are fixed IV values applied to each stat, not a total IV score.

The player selection screen also previews rentals using the appropriate IV value. The final opponent battle receives the higher value for that challenge.

## AI progression

Factory AI is tied to the challenge number:

- Challenges 0–1: no additional Factory AI checks.
- Challenges 2–3: checks for obviously bad moves.
- Challenge 4 onward: checks for bad moves, tries to faint the player's Pokémon, and checks move viability.
- The Factory Brain uses the strongest listed AI checks.

This is controlled by `GetAiScriptsInBattleFactory` in `src/battle_factory.c`.

## What new sets must preserve

New Pokémon sets should fit the existing system rather than bypass it. Each set should have:

- A clear battle role.
- Four moves that work together.
- An item that supports the set.
- A sensible nature and EV spread.
- A place in the existing quality progression.
- No dependence on unsupported gimmicks.

The set itself should not decide when it becomes available. The Factory's ranges and challenge rules should continue to decide that.

## Planned Gen 9 work

Before adding Gen 9 data, we need to define:

1. Which Pokémon and forms are allowed.
2. Which battle mechanics are intentionally unsupported.
3. How Gen 9 sets map to the existing quality ranges.
4. Whether modern sets should be added into the existing table or placed in a separate table with the same selection rules.
5. How Level 50 and Open Level should differ for the new sets.

The safest first implementation is to add a small number of Gen 9 sets to the existing table, place them explicitly in the intended quality ranges, and verify that the original selection, duplicate, swap, IV, and AI systems continue to work unchanged.
