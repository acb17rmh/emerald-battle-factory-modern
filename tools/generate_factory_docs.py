#!/usr/bin/env python3
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src/data/battle_frontier/generated_factory_sets.json"
CONSTANTS = ROOT / "include/constants/battle_frontier_mons.h"
OUTPUT = ROOT / "docs/battle_factory_sets.md"
POOL_OUTPUTS = [ROOT / f"docs/battle_factory_pool_{pool}.md" for pool in range(8)]


def display_name(value):
    value = value.removeprefix("SPECIES_")
    special_names = {
        "NIDORAN_M": "Nidoran♂",
        "NIDORAN_F": "Nidoran♀",
        "FARFETCHD": "Farfetch'd",
        "MR_MIME": "Mr. Mime",
        "MIME_JR": "Mime Jr.",
        "MR_RIME": "Mr. Rime",
        "SIRFETCHD": "Sirfetch'd",
        "HOOPA_UNBOUND": "Hoopa Unbound",
    }
    if value in special_names:
        return special_names[value]
    return value.replace("_", " ").title()


def display_constant(value):
    for prefix in ("SPECIES_", "ABILITY_", "ITEM_", "MOVE_", "NATURE_"):
        if value.startswith(prefix):
            value = value.removeprefix(prefix)
            break
    return display_name(value)


def format_evs(evs):
    labels = ("HP", "Atk", "Def", "SpA", "SpD", "Spe")
    return ", ".join(f"{label} {value}" for label, value in zip(labels, evs) if value)


def load_pools(manifest):
    constants = {}
    for line in CONSTANTS.read_text().splitlines():
        match = re.match(r"#define (FRONTIER_MON_GENERATED_[A-Z0-9_]+) (\S+)$", line)
        if match:
            constants[match.group(1)] = match.group(2)

    by_constant = {entry["constant"]: entry["id"] for entry in manifest}
    pools = {}
    for pool in range(8):
        start_name = constants[f"FRONTIER_MON_GENERATED_POOL_{pool}_START"]
        end_name = constants[f"FRONTIER_MON_GENERATED_POOL_{pool}_END"]
        pools[pool] = (by_constant[start_name], by_constant[end_name])
    return pools


def pool_criteria(pool):
    level_50 = f"Challenge {pool}" if pool < 7 else "Challenge 7 and later"
    open_level = "Does not appear" if pool < 2 else f"Challenge {pool - 2}" if pool < 7 else "Challenge 5 and later"
    return level_50, open_level


def group_entries(manifest):
    pools = load_pools(manifest)
    by_pool = defaultdict(list)
    for entry in manifest:
        for pool, (start, end) in pools.items():
            if start <= entry["id"] <= end:
                by_pool[pool].append(entry)
                break
    return pools, by_pool


def render_entries(entries):
    lines = []
    current_species = None
    for entry in sorted(entries, key=lambda entry: (entry["species"], entry["name"], entry["id"])):
        species = display_constant(entry["species"])
        if species != current_species:
            lines.extend([f"### {species}", ""])
            current_species = species
        moves = ", ".join(display_constant(move) for move in entry["moves"])
        lines.extend([
            f"**{entry['name']}**  ",
            f"Ability: {display_constant(entry['ability'])}  ",
            f"Item: {display_constant(entry['item'])}  ",
            f"Nature: {display_constant(entry['nature'])}  ",
            f"Moves: {moves}  ",
            f"EVs: {format_evs(entry['evs'])}  ",
            "",
        ])
    return lines


def render_index(manifest, pools, by_pool):
    lines = [
        "# Generated Battle Factory Set Catalogue",
        "",
        "This is the complete roster currently used by the Battle Factory. Each entry shows the Pokémon, ability, item, moves, nature, and EVs.",
        "",
        "For the rules behind the pools and challenge progression, see [How the Battle Factory Works](./battle_factory_mechanics.md).",
        "",
        f"The current roster contains **{len(manifest)} sets** for **{len({entry['species'] for entry in manifest})} species**.",
        "",
        "Choose a pool below to see its sets and the challenges where it can appear.",
        "",
        "| Pool | Level 50 | Open Level | Sets |",
        "| --- | --- | --- | ---: |",
    ]
    for pool in range(8):
        level_50, open_level = pool_criteria(pool)
        lines.append(f"| [Pool {pool}](./battle_factory_pool_{pool}.md) | {level_50} | {open_level} | {len(by_pool[pool])} |")
    return "\n".join(lines) + "\n"


def render_pool(pool, pools, by_pool):
    level_50, open_level = pool_criteria(pool)
    lines = [
        f"# Battle Factory Pool {pool}",
        "",
        f"This pool appears in **Level 50: {level_50}** and **Open Level: {open_level}**.",
        "",
        "The pool is selected by the Factory's existing challenge progression. It is not a separate difficulty setting, and sets do not move between pools during a run.",
        "",
        f"This pool contains **{len(by_pool[pool])} sets**.",
        "",
        "[Back to the complete set catalogue](./battle_factory_sets.md)",
        "",
    ]
    lines.extend(render_entries(by_pool[pool]))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    pools, by_pool = group_entries(manifest)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != render_index(manifest, pools, by_pool):
            raise SystemExit("Battle Factory documentation is out of date")
        for pool, path in enumerate(POOL_OUTPUTS):
            if not path.is_file() or path.read_text() != render_pool(pool, pools, by_pool):
                raise SystemExit("Battle Factory documentation is out of date")
    else:
        OUTPUT.write_text(render_index(manifest, pools, by_pool))
        for pool, path in enumerate(POOL_OUTPUTS):
            path.write_text(render_pool(pool, pools, by_pool))


if __name__ == "__main__":
    main()
