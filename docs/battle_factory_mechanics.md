# Battle Factory Mechanics

This document describes the Battle Factory rules currently implemented by the expansion. It is the reference point for adding modern Pokémon sets without changing the original Factory progression.

The current Factory routes all progression rows to the generated entries at the end of the Factory table. The original vanilla entries remain available to other Frontier systems, but Factory selection uses the generated roster.

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

The Pokémon's level, IVs, personality, and trainer information are added when the game creates the actual Pokémon. Generated entries also specify an explicit ability.

New generated sets should be added through `tools/generate_factory_sets.py`, which also updates the manifest and progression pool constants.

## Set ordering and quality ranges

The generated roster contains 920 entries in eight equal pools of 115 entries. The current numeric ranges are:

| Pool | Entry IDs | Level 50 challenge | Open Level challenge |
|---:|---:|---:|---:|
| 0 | 882–996 | 0 | — |
| 1 | 997–1111 | 1 | — |
| 2 | 1112–1226 | 2 | 0 |
| 3 | 1227–1341 | 3 | 1 |
| 4 | 1342–1456 | 4 | 2 |
| 5 | 1457–1571 | 5 | 3 |
| 6 | 1572–1686 | 6 | 4 |
| 7 | 1687–1801 | 7 and later | 5 and later |

The better-rental logic uses the next progression row where one exists. After the final row, it keeps using Pool 7. The symbolic pool constants in `include/constants/battle_frontier_mons.h` are authoritative; the numeric IDs above are generated from the current roster.

The source format score is used to order generated sets from weaker to stronger before they are split into pools. Pool placement is therefore generated, not hand-entered for every set.

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
- The current generated pools do not place entries above `FRONTIER_MONS_HIGH_TIER`, so all generated sets can appear in Level 50 mode. Open Level still starts at Pool 2 and advances through the stronger pools.

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

## Generated roster workflow

The current roster is generated from Smogon singles data. The generator filters unsupported formats and gimmicks, keeps up to four distinct sets per species, infers abilities from set clues and expansion data, and writes the generated C data, constants, and manifest.

Run the following checks after regenerating the roster:

```text
python3 tools/generate_factory_sets.py
python3 tools/validate_factory_sets.py
make -j$(nproc)
```

The validator checks the manifest, IDs, pool distribution, duplicate sets, EV totals, constants, selected abilities, and unsupported gimmicks.
