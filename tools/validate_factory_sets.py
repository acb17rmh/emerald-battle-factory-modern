#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTANTS = ROOT / "include/constants"
MANIFEST = ROOT / "src/data/battle_frontier/generated_factory_sets.json"
import sys
sys.path.insert(0, str(ROOT / "tools"))
from generate_factory_sets import (
    ABILITY_OVERRIDES,
    CONDITIONAL_ABILITIES,
    MAGIC_GUARD_SPECIES,
    PRANKSTER_SPECIES,
    REGENERATOR_SPECIES,
    ROLE_ABILITIES,
    SHEER_FORCE_SPECIES,
    TERRAIN_ABILITIES,
    UNAWARE_SPECIES,
    WEATHER_ABILITIES,
    GENERATED_START,
    build_ability_options,
)


def names(path, prefix):
    return set(re.findall(rf"\b{prefix}[A-Z0-9_]+", path.read_text()))


def abilities_by_species():
    result = defaultdict(set)
    for path in (ROOT / "src/data/pokemon/species_info").glob("gen_*_families.h"):
        text = path.read_text()
        for match in re.finditer(r"\[SPECIES_([A-Z0-9_]+)\].*?\.abilities\s*=\s*\{([^}]+)", text, re.S):
            result["SPECIES_" + match.group(1)].update(re.findall(r"ABILITY_[A-Z0-9_]+", match.group(2)))
    return result


SPECIES_ALIASES = {
    "SPECIES_AEGISLASH": "SPECIES_AEGISLASH_SHIELD",
    "SPECIES_MIMIKYU": "SPECIES_MIMIKYU_DISGUISED",
}


def main():
    roster = json.loads(MANIFEST.read_text())
    issues = []
    expected_ids = list(range(GENERATED_START, GENERATED_START + len(roster)))
    actual_ids = [entry["id"] for entry in roster]
    if actual_ids != expected_ids:
        issues.append("generated IDs are not contiguous")

    species_names = names(CONSTANTS / "species.h", "SPECIES_")
    move_names = names(CONSTANTS / "moves.h", "MOVE_")
    item_names = names(CONSTANTS / "items.h", "ITEM_")
    nature_names = names(CONSTANTS / "pokemon.h", "NATURE_")
    ability_names = names(CONSTANTS / "abilities.h", "ABILITY_")
    legal_abilities = defaultdict(set)
    for species, abilities in build_ability_options().items():
        legal_abilities[species].update(abilities)
    for species, ability in ABILITY_OVERRIDES.items():
        legal_abilities[species].add(ability)
    for species, ability in CONDITIONAL_ABILITIES.items():
        legal_abilities[species].add(ability)
    for species in SHEER_FORCE_SPECIES:
        legal_abilities[species].add("ABILITY_SHEER_FORCE")
    for species in MAGIC_GUARD_SPECIES:
        legal_abilities[species].add("ABILITY_MAGIC_GUARD")
    for species, ability in WEATHER_ABILITIES.items():
        legal_abilities[species].add(ability)
    for species, ability in TERRAIN_ABILITIES.items():
        legal_abilities[species].add(ability)
    for species, (ability, _) in ROLE_ABILITIES.items():
        legal_abilities[species].add(ability)
    for species in REGENERATOR_SPECIES:
        legal_abilities[species].add("ABILITY_REGENERATOR")
    for species in PRANKSTER_SPECIES:
        legal_abilities[species].add("ABILITY_PRANKSTER")
    for species in UNAWARE_SPECIES:
        legal_abilities[species].add("ABILITY_UNAWARE")
    for species in species_names:
        if species.startswith("SPECIES_ARCEUS_"):
            legal_abilities[species].add("ABILITY_MULTITYPE")
    per_species = defaultdict(list)
    exact_sets = defaultdict(set)
    formats = Counter()
    pools = Counter()

    for entry in roster:
        species = entry["species"]
        per_species[species].append(entry)
        key = (entry["item"], entry["nature"], tuple(entry["moves"]))
        exact_sets[species].add(key)
        formats[entry["source"]] += 1
        if species not in species_names:
            issues.append(f"unknown species: {species}")
        if entry["ability"] not in ability_names:
            issues.append(f"unknown ability: {entry['ability']}")
        elif entry["ability"] not in legal_abilities.get(SPECIES_ALIASES.get(species, species), set()):
            issues.append(f"illegal ability {entry['ability']} for {species}")
        if entry["item"] not in item_names:
            issues.append(f"unknown item: {entry['item']}")
        if entry["nature"] not in nature_names:
            issues.append(f"unknown nature: {entry['nature']}")
        for move in entry["moves"]:
            if move not in move_names:
                issues.append(f"unknown move {move} for {species}")
        if sum(entry["evs"]) > 510:
            issues.append(f"EV total exceeds 510 for {species}")
        if any(token in move for move in entry["moves"] for token in ("TERA", "Z_MOVE", "MAX_")):
            issues.append(f"unsupported battle gimmick in {species}")
        if any(token in entry["item"] for token in ("MEGA", "Z_", "DYNAMAX")):
            issues.append(f"unsupported item gimmick in {species}")

    for species, entries in per_species.items():
        if len(entries) > 4:
            issues.append(f"more than four sets for {species}")
        if len(exact_sets[species]) != len(entries):
            issues.append(f"duplicate set for {species}")

    constant_text = (CONSTANTS / "battle_frontier_mons.h").read_text()
    constant_indexes = {entry["constant"]: index for index, entry in enumerate(roster)}
    for pool in range(8):
        start_name = re.search(rf"POOL_{pool}_START (FRONTIER_MON_GENERATED_[A-Z0-9_]+)", constant_text).group(1)
        end_name = re.search(rf"POOL_{pool}_END (FRONTIER_MON_GENERATED_[A-Z0-9_]+)", constant_text).group(1)
        start = constant_indexes[start_name]
        end = constant_indexes[end_name]
        pools[pool] = end - start + 1

    print(f"Entries: {len(roster)}")
    print(f"Species: {len(per_species)}")
    print(f"Pools: {dict(pools)}")
    print(f"Source formats: {dict(formats)}")
    if issues:
        for issue in sorted(set(issues)):
            print(f"ERROR: {issue}")
        return 1
    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
