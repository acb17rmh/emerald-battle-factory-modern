# Battle Factory Set Review

This document is the worksheet for building the new Battle Factory roster.

The final roster will contain a curated selection from Generations 1–9. It will use the existing Factory table and progression rules, but the set IDs and set data will be redesigned.

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

The final roster will use the existing Factory progression pools rather than introducing a new tier system.

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

## First audit

The first audit should create a small cross-generation sample containing:

- At least one Pokémon from every generation.
- Several primary roles.
- At least one candidate for every Factory pool where practical.
- A mixture of ordinary, Legendary, Mythical, and alternate-form candidates where suitable.

This sample is for testing the review rules. It is not yet the final roster.

## Initial candidate sample

These candidates are a starting point for the audit. They are not approved sets.

| Generation | Candidate | Primary role | Reason for inclusion | Review status |
| ---: | --- | --- | --- | --- |
| 1 | Starmie | Special attacker | Fast special attacker with offensive and utility options | Candidate |
| 2 | Scizor | Physical attacker | Distinct physical role and strong ability-based set options | Candidate |
| 3 | Breloom | Status/disruption | Clear status strategy and unusual Factory play patterns | Candidate |
| 4 | Gliscor | Defensive | Durable defensive role with several possible set directions | Candidate |
| 5 | Volcarona | Setup | Strong setup identity and a clear late-game role | Candidate |
| 6 | Sylveon | Defensive | Specially oriented defensive and support options | Candidate |
| 7 | Mimikyu | Setup | Distinct setup strategy and ability-driven identity | Candidate |
| 8 | Dragapult | Mixed attacker | Flexible modern attacker with different offensive directions | Candidate |
| 9 | Gholdengo | Utility | Modern ability and item interactions with a clear battlefield role | Candidate |

The next review pass should find source templates for these candidates, check legality, identify unsupported gimmick dependencies, and assign provisional quality tiers.

## First source-backed templates

These are provisional templates for the first audit. They have been adapted to remove unsupported gimmicks where necessary. They are not yet approved for the Factory table.

| Generation | Pokémon | Ability | Item | Moves | Nature | EVs | Role | Pool | Source | Status |
| ---: | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Starmie | Natural Cure | Colbur Berry | Scald / Recover / Teleport / Rapid Spin | Timid | 252 HP / 4 SpA / 252 Spe | Defensive | 0 | National Dex RU, 2026-07-24 | Candidate |
| 2 | Scizor | Technician | Choice Band | Bullet Punch / U-turn / Close Combat / Knock Off | Adamant | 252 Atk / 4 SpD / 252 Spe | Physical attacker | 0 | UU, 2026-07-24 | Candidate |
| 3 | Breloom | Technician | Black Belt | Bullet Seed / Close Combat / Mach Punch / Rock Tomb | Adamant | 252 Atk / 4 SpD / 252 Spe | Physical attacker | 0 | National Dex RU, 2026-07-24 | Adapted candidate |
| 4 | Gliscor | Poison Heal | Toxic Orb | Spikes / Earthquake / Toxic / Protect | Careful | 244 HP / 36 Def / 228 SpD | Defensive | 0 | OU, 2026-07-24 | Candidate |
| 5 | Volcarona | Flame Body | Heavy-Duty Boots | Quiver Dance / Flamethrower / Bug Buzz / Roost | Timid | 248 HP / 200 Def / 60 Spe | Setup | 0 | National Dex, 2026-07-24 | Adapted candidate |
| 6 | Sylveon | Pixilate | Leftovers | Wish / Protect / Calm Mind / Hyper Voice | Bold | 252 HP / 212 Def / 44 Spe | Defensive | 0 | NU, 2026-07-24 | Candidate |
| 7 | Mimikyu | Disguise | Lum Berry | Play Rough / Shadow Claw / Swords Dance / Shadow Sneak | Jolly | 252 Atk / 4 SpD / 252 Spe | Setup | 0 | OU, 2026-07-24 | Adapted candidate |
| 8 | Dragapult | Infiltrator | Expert Belt | Dragon Darts / Hex / Will-O-Wisp / U-turn | Naive | 4 Atk / 252 SpA / 252 Spe | Mixed attacker | 0 | OU, 2026-07-24 | Adapted candidate |
| 9 | Gholdengo | Good as Gold | Air Balloon | Shadow Ball / Make It Rain / Trick / Recover | Timid | 252 SpA / 4 SpD / 252 Spe | Utility | 0 | National Dex, 2026-07-24 | Candidate |

The source sets include format-specific assumptions and, in some cases, optional Terastallization or other mechanics. The listed versions are the starting point for the Factory review, not direct imports. The Volcarona set replaces Hidden Power Ground with Roost because Hidden Power depends on IVs that the Factory controls separately. The Gliscor set resolves the source's slash options toward a single defensive build.

## Filtered API results

The first pull used the generation-wide Gen 9 data on 2026-07-24. Only the approved singles formats were included.

| Pokémon | Available formats | Available source set names |
| --- | --- | --- |
| Starmie | National Dex RU | Defensive, Offensive |
| Scizor | OU, UU, National Dex, National Dex UU | Choice Band, Offensive Swords Dance, Pivot, Swords Dance, Utility, Bulky Swords Dance |
| Breloom | RU, National Dex RU | Poison Heal, Choice Band, Swords Dance |
| Gliscor | OU, Ubers, National Dex | Defensive, Swords Dance, Utility |
| Volcarona | Ubers, National Dex | Quiver Dance, Bulky Quiver Dance, Offensive Quiver Dance, Substitute + Swarm |
| Sylveon | NU, National Dex RU | Choice Specs, Wish, Cleric |
| Mimikyu | OU, UU, RU, National Dex | Swords Dance, Trick Room, Offensive Utility |
| Dragapult | OU | Boots Pivot, Choice Specs, Mixed Offensive |
| Gholdengo | OU, Ubers, National Dex | Bulky Nasty Plot, Choice Scarf, Offensive Nasty Plot, Thunder Wave + Hex, Nasty Plot |

This confirms that the generation-wide file gives us useful variety without importing doubles, Little Cup, or non-standard formats. The next pass can select distinct roles from this list instead of inventing them manually.

The sample still needs to be assigned across the existing Factory pools. It is not necessary for every pool to contain every generation, but each pool should contain enough variety to preserve the original progression.

The current generated roster uses 920 source-backed entries for 381 species, with at most four distinct sets per species, split into eight progression pools. The existing progression rows select from these pools, with stronger ranges used by later rows. The generated roster covers the intended Gen 1–9 generation spread.

Run `python3 tools/validate_factory_sets.py` after generation to check the roster manifest, constants, abilities, items, moves, EV totals, gimmick filters, duplicate sets, and pool distribution.
