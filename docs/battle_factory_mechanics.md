# How the Battle Factory Works

The Battle Factory is about making the best team you can from whatever the game gives you. You start with six rentals, choose three, and improve your options by trading with defeated opponents.

This version keeps the original challenge structure and progression. The main change is the roster: it now includes modern, viable sets from across Generations 1–9.

Battles use the modern rules and Pokémon content available through Generation 9. The Factory does not use battle gimmicks: there is no Mega Evolution, Z-Move, Dynamax, Gigantamax, or Terastallization.

## A challenge

The Factory is played in challenges of seven battles.

At the beginning of a challenge:

1. The game creates six rental Pokémon.
2. The player chooses three of them.
3. The game creates an opponent team.
4. The player battles seven trainers, one at a time.
5. After a win, the player can exchange rentals for Pokémon used by the opponent.

Every seven wins advances you to the next challenge. Level 50 and Open Level keep separate streaks.

## What you are renting

Each rental tells you its:

- Species
- Four moves
- Held item
- EV spread
- Nature
- Ability

The level and IV quality depend on the challenge.

For the complete current roster, see the [Generated Set Catalogue](./battle_factory_sets.md).

## How sets enter the Factory

The roster is split into eight roughly even pools. The exact number of sets in each pool can change as the roster grows.

In this table, a challenge means a block of seven battles. Challenge 1 is the first seven battles, Challenge 2 is the next seven, and so on.

| Pool | Level 50 first appears | Open Level first appears |
|---:|---:|---:|
| 1 | Challenge 1 | Does not appear |
| 2 | Challenge 2 | Does not appear |
| 3 | Challenge 3 | Challenge 1 |
| 4 | Challenge 4 | Challenge 2 |
| 5 | Challenge 5 | Challenge 3 |
| 6 | Challenge 6 | Challenge 4 |
| 7 | Challenge 7 | Challenge 5 |
| 8 | Challenge 8 and later | Challenge 6 and later |

After the final challenge, the Factory continues using Pool 8. The [set catalogue](./battle_factory_sets.md) has a page for each pool.

## Improving the opening draft

The Factory tracks rental swaps separately from the win streak. Each time you swap one of your rentals for an opponent's Pokémon, the swap count goes up.

When a new streak begins, both the win streak and the swap count return to zero. During the streak, more swaps gradually improve the next opening draft.

The current rental ranks are:

| Rental swaps in the current streak | Rental rank |
|---:|---:|
| 0–14 | 0 |
| 15–21 | 1 |
| 22–28 | 2 |
| 29–35 | 3 |
| 36–42 | 4 |
| 43 or more | 5 |

The rank affects the next group of six rentals. For example, rank 2 means that two of the six Pokémon are chosen from the next better pool. The other four use the normal pool for the current challenge.

This does not change the challenge number. It only improves the quality of some Pokémon in the opening draft.

## Restrictions on teams

The initial rental draft cannot contain two Pokémon of the same species or two Pokémon with the same held item.

Unown is excluded.

The opponent generation applies similar restrictions:

- No duplicate species on the opponent team.
- No duplicate held items, except that Pokémon without an item can repeat.
- No opponent species that matches any of the player's available rental species.

## Opponent trainers and teams

The opponent trainer is selected from a challenge-dependent trainer range.

The game avoids repeating a trainer within the current seven-battle challenge. The final battle of a challenge uses a harder trainer range.

After challenge 7, the hardest trainer range continues to be used.

The trainer and the team are selected separately. A trainer's appearance tells you who you are fighting, but not which Factory sets will be on the opposing side.

## IV quality

Factory IVs improve by challenge. The current fixed IV values are:

| Challenge | Normal battle IVs | Final battle IVs |
|---:|---:|---:|
| 1 | 3 | 6 |
| 2 | 6 | 9 |
| 3 | 9 | 12 |
| 4 | 12 | 15 |
| 5 | 15 | 18 |
| 6 | 21 | 31 |
| 7 and later | 31 | 31 |

These are fixed IV values applied to each stat, not a total IV score.

The player selection screen also previews rentals using the appropriate IV value. The final opponent battle receives the higher value for that challenge.

## AI progression

Factory AI is tied to the challenge number:

- Challenges 1–2: avoids obviously bad moves.
- Challenges 3–4: uses basic trainer logic, including trying to faint the player's Pokémon and checking move viability.
- Challenge 5 onward: uses the stronger modern trainer AI.
- The Factory Brain also uses the stronger modern trainer AI.
