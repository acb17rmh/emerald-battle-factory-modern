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

POKEMON_NAME_OVERRIDES = {
    "SPECIES_ARCEUS_NORMAL": "Arceus",
    "SPECIES_BASCULEGION_F": "Basculegion-F",
    "SPECIES_CALYREX_ICE": "Calyrex-Ice",
    "SPECIES_CHIEN_PAO": "Chien-Pao",
    "SPECIES_CHI_YU": "Chi-Yu",
    "SPECIES_DEOXYS_ATTACK": "Deoxys-Attack",
    "SPECIES_DEOXYS_SPEED": "Deoxys-Speed",
    "SPECIES_HO_OH": "Ho-Oh",
    "SPECIES_INDEEDEE_F": "Indeedee-F",
    "SPECIES_KOMMO_O": "Kommo-o",
    "SPECIES_LYCANROC_DUSK": "Lycanroc-Dusk",
    "SPECIES_MAUSHOLD_FOUR": "Maushold-Four",
    "SPECIES_NECROZMA_DUSK_MANE": "Necrozma-Dusk-Mane",
    "SPECIES_ORICORIO_POM_POM": "Oricorio-Pom-Pom",
    "SPECIES_ORICORIO_SENSU": "Oricorio-Sensu",
    "SPECIES_ROTOM_FROST": "Rotom-Frost",
    "SPECIES_ROTOM_HEAT": "Rotom-Heat",
    "SPECIES_ROTOM_MOW": "Rotom-Mow",
    "SPECIES_ROTOM_WASH": "Rotom-Wash",
    "SPECIES_SINISTCHA_MASTERPIECE": "Sinistcha-Masterpiece",
    "SPECIES_TAUROS_PALDEA_AQUA": "Tauros-Paldea-Aqua",
    "SPECIES_TAUROS_PALDEA_BLAZE": "Tauros-Paldea-Blaze",
    "SPECIES_TING_LU": "Ting-Lu",
    "SPECIES_URSHIFU_RAPID_STRIKE": "Urshifu-Rapid-Strike",
    "SPECIES_WO_CHIEN": "Wo-Chien",
    "SPECIES_ZACIAN_CROWNED": "Zacian-Crowned",
    "SPECIES_ZAMAZENTA_CROWNED": "Zamazenta-Crowned",
    "SPECIES_ZARUDE_DADA": "Zarude-Dada",
}


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


def display_pokemon_name(value):
    if value in POKEMON_NAME_OVERRIDES:
        return POKEMON_NAME_OVERRIDES[value]
    name = display_constant(value)
    form_suffixes = (
        " Alola",
        " Galar",
        " Hisui",
        " Paldea",
        " Origin",
        " Therian",
        " Dragon",
        " Black",
        " White",
        " Attack",
        " Defense",
        " Speed",
        " Bloodmoon",
        " Cornerstone",
        " Hearthflame",
        " Wellspring",
        " Sky",
        " Aqua",
        " Blaze",
    )
    for suffix in form_suffixes:
        if name.endswith(suffix):
            return f"{name.removesuffix(suffix)}-{suffix.strip()}"
    return name


def display_item_name(value):
    return display_constant(value).replace("Heavy Duty", "Heavy-Duty")


def display_move_name(value):
    return display_constant(value).replace("U Turn", "U-turn").replace("Will O Wisp", "Will-O-Wisp")


def format_evs(evs):
    labels = ("HP", "Atk", "Def", "SpA", "SpD", "Spe")
    return " / ".join(f"{value} {label}" for label, value in zip(labels, evs) if value)


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
    level_50 = f"Challenge {pool + 1}" if pool < 7 else "Challenge 8 and later"
    open_level = "Does not appear" if pool < 2 else f"Challenge {pool - 1}" if pool < 7 else "Challenge 6 and later"
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
        species = display_pokemon_name(entry["species"])
        if species != current_species:
            lines.extend([f"### {species}", ""])
            current_species = species
        lines.extend([
            f"**{entry['name']}**",
            "```text",
            f"{species} @ {display_item_name(entry['item'])}",
            f"Ability: {display_constant(entry['ability'])}",
            f"EVs: {format_evs(entry['evs'])}",
            f"{display_constant(entry['nature'])} Nature",
            *(f"- {display_move_name(move)}" for move in entry["moves"]),
            "```",
            "",
        ])
    return lines


def render_index(manifest, pools, by_pool):
    lines = [
        "# Generated Battle Factory Set Catalogue",
        "",
        "This is the complete roster currently used by the Battle Factory. Each set is shown in a format that can be copied into Pokémon Showdown or PokéPaste.",
        "",
        "For the rules behind the pools and challenge progression, see [How the Battle Factory Works](./battle_factory_mechanics.md).",
        "",
        f"The current roster contains **{len(manifest)} sets** for **{len({entry['species'] for entry in manifest})} species**.",
        "",
        "A challenge is a block of seven battles. Challenge 1 is the first seven battles, Challenge 2 is the next seven, and so on.",
        "",
        "Choose a pool below to see its sets and the challenges where it can appear.",
        "",
        "| Pool | Level 50 first appears | Open Level first appears | Sets |",
        "| --- | --- | --- | ---: |",
    ]
    for pool in range(8):
        level_50, open_level = pool_criteria(pool)
        lines.append(f"| [Pool {pool + 1}](./battle_factory_pool_{pool}.md) | {level_50} | {open_level} | {len(by_pool[pool])} |")
    return "\n".join(lines) + "\n"


def render_pool(pool, pools, by_pool):
    level_50, open_level = pool_criteria(pool)
    lines = [
        f"# Battle Factory Pool {pool + 1}",
        "",
        f"This pool appears in **Level 50: {level_50}** and **Open Level: {open_level}**.",
        "",
        "A challenge is a block of seven battles. Challenge 1 is the first seven battles, Challenge 2 is the next seven, and so on.",
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
