# Battle Factory Set Review

This document is the worksheet for building the new Battle Factory roster.

The current roster contains a generated selection from Generations 1–9. It uses the existing Factory table and progression rules, with generated set IDs and data at the end of the table.


## Review rules

- Use external sets as templates, not as automatic final answers.
- Pull set templates from the structured Smogon sets data where possible.
- Use a mixture of competitive formats, choosing the most useful source for each Pokémon.
- Record the source, format, and date for every set.
- Use legal moves, abilities, items, forms, and EV spreads.
- Specify the ability for every set, including Hidden Abilities when appropriate.
- Exclude sets whose main strategy depends on Mega Evolution, Z-Moves, Dynamax, or Terastallization.
- Adapt sets when the core strategy is sound but the Factory AI would struggle to use it.
- Allow common team support, but do not require a specific teammate.
- Give every set one primary role.
- Use the source tier as a starting point for Factory quality, then make simple manual adjustments.

The initial structured source is the [Smogon sets data](https://pkmn.github.io/smogon/data/sets/). Generation-wide files such as `gen9.json` provide sets for each Pokémon across multiple formats. Format files such as `gen9ou.json` are useful when we need to inspect one format in detail. The downloaded data should be treated as a dated snapshot because the endpoint can change.

## Combining source formats

No single competitive format matches the Factory roster. The source process is therefore:

1. Use the generation-wide data to find sets for a candidate Pokémon.
2. Consider sets from multiple singles formats, including National Dex where useful.
3. Remove duplicate or near-duplicate sets.
4. Keep the most useful distinct roles and set ideas.
5. Use the source format as a rough strength signal, not as the Factory tier.
6. Adapt the accepted set to the Factory rules.

If a Pokémon has no useful current set, check the relevant older-generation or National Dex data before rejecting it.

## Source format filter

The first data pull should include only singles formats that resemble ordinary team battles.

Use:

- OU
- UU
- RU
- NU
- PU
- ZU
- NFE when an unevolved Pokémon is being considered
- Ubers when a Legendary or Mythical set is being considered
- National Dex singles and its standard singles tiers

Exclude:

- VGC, Doubles, and National Dex Doubles
- Little Cup
- Battle Stadium and Battle Spot formats
- Monotype, 1v1, Draft, and CAP formats
- Hackmons, Balanced Hackmons, Almost Any Ability, STABmons, Mix and Mega, and similar formats
- Anything Goes and other formats whose rules do not represent an ordinary Factory battle

This is an allowlist. A new format should not be included automatically just because it appears in the API.

## Primary roles

Use one of these roles for every set:

- Physical attacker
- Special attacker
- Mixed attacker
- Defensive
- Setup
- Status/disruption
- Weather
- Utility

Setup and Weather take priority over an attacking role when they are the main idea of the set.

## Factory pools

The current roster uses the existing Factory progression pools rather than introducing a new tier system.

- Pool 0 is the earliest Level 50 pool.
- Pools 1 through 6 are the progressively stronger pools.
- Pool 7 is the final high-tier pool.

The current numeric ranges are documented in [Battle Factory Mechanics](./battle_factory_mechanics.md). The new roster does not need to use the same numeric boundaries or the same number of sets in each pool. It must keep the same number of progression pools and the same relationship between pools, challenges, and better rentals. The same Pokémon may appear in multiple pools when it has genuinely different sets. Not every generation or Pokémon needs to appear in every pool.

During review, we can use simple words such as weak, middle, or strong in notes, but those words are not part of the game design.

## Set review fields

Each reviewed set should record:

| Field | Meaning |
| --- | --- |
| Pokémon | Species or form used by the set |
| Generation | Pokémon’s original generation |
| Set name | Short name describing the build |
| Primary role | One role from the fixed list |
| Ability | Explicit intended ability |
| Moves | Four legal moves |
| Item | Held item, excluding unsupported gimmick items |
| Nature | Set nature |
| EVs | Set EV spread |
| Source | Link or named source |
| Format | Competitive format used as the template |
| Source date | Date the source was checked |
| Factory pool | Pool 0 through Pool 7 |
| Gimmick dependency | None, optional, or required |
| AI adjustment | Whether the set was changed for Factory AI |
| Review status | Candidate, accepted, rejected, or needs review |
| Notes | Short explanation of important decisions |

## Review process

1. Choose a Pokémon that fills a needed role or generation gap.
2. Find one or more suitable external sets.
3. Record the source, format, and date.
4. Remove unsupported gimmicks and reject the set if its main strategy no longer works.
5. Check moves, ability, item, form, and EV legality.
6. Adapt the set if the Factory AI cannot use its core strategy reliably.
7. Assign one primary role.
8. Choose a provisional Factory pool using the source format as a rough strength signal.
9. Make only obvious manual pool adjustments.
10. Mark the set as accepted, rejected, or needing review.

The current generated roster uses 920 source-backed entries for 381 species, with at most four distinct sets per species, split into eight progression pools. The existing progression rows select from these pools, with stronger ranges used by later rows. The generated roster covers the intended Gen 1–9 generation spread.

Run `python3 tools/validate_factory_sets.py` after generation to check the roster manifest, constants, abilities, items, moves, EV totals, gimmick filters, duplicate sets, and pool distribution.
