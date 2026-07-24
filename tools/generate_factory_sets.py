#!/usr/bin/env python3
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_URL = "https://pkmn.github.io/smogon/data/sets/gen9.json"
CONSTANTS = ROOT / "include/constants"
MON_DATA = ROOT / "src/data/battle_frontier/battle_frontier_mons.h"
MON_CONSTANTS = CONSTANTS / "battle_frontier_mons.h"
MANIFEST = ROOT / "src/data/battle_frontier/generated_factory_sets.json"
GENERATED_START = 882
SPECIES_NAME_OVERRIDES = {
    "arceus": "SPECIES_ARCEUS_NORMAL",
}
SPECIES_FAMILY_CAPS = {
    "arceus": 4,
}
FINAL_POOL_SPECIES = {
    "SPECIES_ARCEUS_NORMAL",
}

BAD_FORMAT_PARTS = (
    "vgc", "doubles", "littlecup", "lc", "monotype", "1v1", "draft",
    "hackmons", "balancedhackmons", "almostanyability", "aaa", "stabmons",
    "mixandmega", "anythinggoes", "nationaldexag", "sharedpower", "camomons",
    "inverse", "godlygift", "sketchmons", "metronome", "theorymon",
)
FORMAT_SCORE = {
    "zu": 1,
    "pu": 2,
    "nu": 3,
    "ru": 4,
    "uu": 5,
    "ou": 6,
    "ubers": 7,
}
ANCHORS = {
    "Annihilape", "Baxcalibur", "Ceruledge", "Dragapult", "Gholdengo",
    "Great Tusk", "Iron Valiant", "Kingambit", "Tinkaton", "Roaring Moon",
}
ABILITY_OVERRIDES = {
    "SPECIES_ALOMOMOLA": "ABILITY_REGENERATOR",
    "SPECIES_STARMIE": "ABILITY_NATURAL_CURE",
    "SPECIES_SCIZOR": "ABILITY_TECHNICIAN",
    "SPECIES_BRELOOM": "ABILITY_TECHNICIAN",
    "SPECIES_GLISCOR": "ABILITY_POISON_HEAL",
    "SPECIES_VOLCARONA": "ABILITY_FLAME_BODY",
    "SPECIES_SYLVEON": "ABILITY_PIXILATE",
    "SPECIES_MIMIKYU": "ABILITY_DISGUISE",
    "SPECIES_DRAGAPULT": "ABILITY_INFILTRATOR",
    "SPECIES_GHOLDENGO": "ABILITY_GOOD_AS_GOLD",
    "SPECIES_GARCHOMP": "ABILITY_ROUGH_SKIN",
    "SPECIES_GYARADOS": "ABILITY_INTIMIDATE",
    "SPECIES_TYRANITAR": "ABILITY_SAND_STREAM",
    "SPECIES_ROTOM_WASH": "ABILITY_LEVITATE",
    "SPECIES_FERROTHORN": "ABILITY_IRON_BARBS",
    "SPECIES_CLEFABLE": "ABILITY_MAGIC_GUARD",
    "SPECIES_TOXAPEX": "ABILITY_REGENERATOR",
    "SPECIES_AEGISLASH": "ABILITY_STANCE_CHANGE",
    "SPECIES_KINGAMBIT": "ABILITY_SUPREME_OVERLORD",
}
CONDITIONAL_ABILITIES = {
    "SPECIES_ZANGOOSE": "ABILITY_TOXIC_BOOST",
    "SPECIES_HERACROSS": "ABILITY_GUTS",
    "SPECIES_BRELOOM": "ABILITY_POISON_HEAL",
    "SPECIES_SWELLOW": "ABILITY_GUTS",
}
SHEER_FORCE_SPECIES = {
    "SPECIES_NIDOKING", "SPECIES_NIDOQUEEN", "SPECIES_LANDORUS", "SPECIES_LANDORUS_THERIAN",
    "SPECIES_DARMANITAN", "SPECIES_DARMANITAN_GALARIAN", "SPECIES_THRASIEN",
}
MAGIC_GUARD_SPECIES = {"SPECIES_CLEFABLE", "SPECIES_ALAKAZAM", "SPECIES_REUNICLUS", "SPECIES_SIGILYPH"}
WEATHER_ABILITIES = {
    "SPECIES_NINETALES": "ABILITY_DROUGHT",
    "SPECIES_NINETALES_ALOLA": "ABILITY_SNOW_WARNING",
    "SPECIES_TORKOAL": "ABILITY_DROUGHT",
    "SPECIES_PELIPPER": "ABILITY_DRIZZLE",
    "SPECIES_POLITOED": "ABILITY_DRIZZLE",
    "SPECIES_TYRANITAR": "ABILITY_SAND_STREAM",
    "SPECIES_HIPPOWDON": "ABILITY_SAND_STREAM",
    "SPECIES_ABOMASNOW": "ABILITY_SNOW_WARNING",
    "SPECIES_ABOMASNOW_MEGA": "ABILITY_SNOW_WARNING",
}
TERRAIN_ABILITIES = {
    "SPECIES_RILLABOOM": "ABILITY_GRASSY_SURGE",
    "SPECIES_INDEEDEE": "ABILITY_PSYCHIC_SURGE",
    "SPECIES_INDEEDEE_FEMALE": "ABILITY_PSYCHIC_SURGE",
    "SPECIES_PINCURCHIN": "ABILITY_ELECTRIC_SURGE",
    "SPECIES_TAPU_KOKO": "ABILITY_ELECTRIC_SURGE",
    "SPECIES_TAPU_LELE": "ABILITY_PSYCHIC_SURGE",
    "SPECIES_TAPU_FINI": "ABILITY_MISTY_SURGE",
    "SPECIES_TAPU_BULU": "ABILITY_GRASSY_SURGE",
}
ROLE_ABILITIES = {
    "SPECIES_SERPERIOR": ("ABILITY_CONTRARY", {"leaf storm", "superpower"}),
    "SPECIES_MALAMAR": ("ABILITY_CONTRARY", {"superpower", "contrary"}),
    "SPECIES_LURANTIS": ("ABILITY_CONTRARY", {"leaf storm", "superpower"}),
    "SPECIES_CLOYSTER": ("ABILITY_SKILL_LINK", {"icicle spear", "rock blast", "bullet seed"}),
    "SPECIES_CINCCINO": ("ABILITY_SKILL_LINK", {"tail slap", "bullet seed", "rock blast"}),
    "SPECIES_NIDOKING": ("ABILITY_SHEER_FORCE", {"life orb"}),
    "SPECIES_NIDOQUEEN": ("ABILITY_SHEER_FORCE", {"life orb"}),
    "SPECIES_MACHAMP": ("ABILITY_NO_GUARD", {"dynamic punch", "stone edge"}),
    "SPECIES_BLAZIKEN": ("ABILITY_SPEED_BOOST", {"protect", "swords dance"}),
    "SPECIES_YANMEGA": ("ABILITY_SPEED_BOOST", {"protect", "quiver dance"}),
    "SPECIES_NINJASK": ("ABILITY_SPEED_BOOST", {"protect", "swords dance"}),
    "SPECIES_SCOLIPEDE": ("ABILITY_SPEED_BOOST", {"protect", "swords dance"}),
    "SPECIES_HAWLUCHA": ("ABILITY_UNBURDEN", {"swords dance", "acrobatics"}),
    "SPECIES_DRAGONITE": ("ABILITY_MULTISCALE", {"dragon dance", "roost"}),
    "SPECIES_GALLADE": ("ABILITY_SHARPNESS", {"psycho cut", "sacred sword", "leaf blade"}),
    "SPECIES_KLEAVOR": ("ABILITY_SHARPNESS", {"stone axe", "night slash", "x-scissor"}),
    "SPECIES_SAMUROTT_HISUI": ("ABILITY_SHARPNESS", {"ceaseless edge", "aqua cutter"}),
    "SPECIES_CRAWDAUNT": ("ABILITY_ADAPTABILITY", {"crabhammer", "knock off"}),
    "SPECIES_PORYGON_Z": ("ABILITY_ADAPTABILITY", {"tri attack", "shadow ball"}),
    "SPECIES_DRACOVISH": ("ABILITY_STRONG_JAW", {"fishious rend", "crunch"}),
}
REGENERATOR_SPECIES = {
    "SPECIES_SLOWBRO", "SPECIES_SLOWKING", "SPECIES_SLOWKING_GALAR", "SPECIES_AMOONGUSS",
    "SPECIES_TANGROWTH", "SPECIES_TORNADUS_THERIAN", "SPECIES_TOXAPEX",
}
PRANKSTER_SPECIES = {
    "SPECIES_GRIMMSNARL", "SPECIES_KLEFKI", "SPECIES_WHIMSICOTT", "SPECIES_SABLEYE",
    "SPECIES_TORNADUS", "SPECIES_THUNDURUS", "SPECIES_MURKROW", "SPECIES_LIEPARD",
}
UNAWARE_SPECIES = {
    "SPECIES_QUAGSIRE", "SPECIES_DONDOZO", "SPECIES_PYUKUMUKU", "SPECIES_CLODSIRE",
}


def read_names(path, prefix):
    text = path.read_text()
    return set(re.findall(rf"\b{prefix}[A-Z0-9_]+", text))


def normalise(name):
    name = name.replace("♀", " F").replace("♂", " M")
    return re.sub(r"[^A-Za-z0-9]", "", name).lower()


def family_name(species_name):
    if normalise(species_name).startswith("arceus"):
        return "arceus"
    return species_name


def build_species_map():
    names = read_names(CONSTANTS / "species.h", "SPECIES_")
    result = {}
    for name in names:
        result.setdefault(normalise(name.removeprefix("SPECIES_")), name)
    for source_name, species in SPECIES_NAME_OVERRIDES.items():
        if species in names:
            result[source_name] = species
    return result


def build_abilities():
    result = {}
    for species, abilities in build_ability_options().items():
        if abilities:
            result[species] = abilities[0]
    return result


def build_ability_options():
    result = {}
    for path in (ROOT / "src/data/pokemon/species_info").glob("gen_*_families.h"):
        current_species = None
        for line in path.read_text().splitlines():
            species = re.search(r"\[SPECIES_([A-Z0-9_]+)\]", line)
            if species:
                current_species = "SPECIES_" + species.group(1)
            if current_species:
                abilities = re.findall(r"ABILITY_[A-Z0-9_]+", line)
                available = result.setdefault(current_species, [])
                for ability in abilities:
                    if ability not in available:
                        available.append(ability)
    return result


def choose(value):
    if isinstance(value, list):
        return value[0]
    return value


def constant_name(value, prefix, names):
    value = choose(value)
    if not isinstance(value, str):
        return None
    candidate = prefix + re.sub(r"[^A-Za-z0-9]", "_", value.upper()).strip("_")
    return candidate if candidate in names else None


def valid_format(format_name):
    return not any(part in format_name.lower() for part in BAD_FORMAT_PARTS)


def unsupported_item(item):
    return item.endswith("_Z") or item.startswith("ITEM_Z_") or "_MEGA" in item


def ability_for_set(species, default, item, moves, set_name):
    if species in CONDITIONAL_ABILITIES and item in {"ITEM_TOXIC_ORB", "ITEM_FLAME_ORB"}:
        return CONDITIONAL_ABILITIES[species]
    move_names = {move.removeprefix("MOVE_").replace("_", " ").lower() for move in moves}
    if species in SHEER_FORCE_SPECIES and item == "ITEM_LIFE_ORB":
        return "ABILITY_SHEER_FORCE"
    if species in MAGIC_GUARD_SPECIES and item == "ITEM_LIFE_ORB":
        return "ABILITY_MAGIC_GUARD"
    if species in WEATHER_ABILITIES:
        weather_ability = WEATHER_ABILITIES[species]
        if any(weather in move_names for weather in ("sunny day", "rain dance", "sandstorm", "hail", "snowscape")):
            return weather_ability
    if species in TERRAIN_ABILITIES and any("terrain" in move for move in move_names):
        return TERRAIN_ABILITIES[species]
    if species in ROLE_ABILITIES:
        candidate, clues = ROLE_ABILITIES[species]
        if item == "ITEM_LIFE_ORB" and candidate == "ABILITY_ADAPTABILITY":
            return candidate
        if move_names.intersection(clues):
            return candidate
    lower_name = set_name.lower()
    if species in REGENERATOR_SPECIES and ("pivot" in lower_name or move_names.intersection({"slack off", "recover", "teleport", "u turn", "volt switch", "scald"})):
        return "ABILITY_REGENERATOR"
    if species in PRANKSTER_SPECIES and move_names.intersection({"encore", "taunt", "thunder wave", "will o wisp", "reflect", "light screen", "tailwind", "trick room"}):
        return "ABILITY_PRANKSTER"
    if species in UNAWARE_SPECIES or "unaware" in lower_name:
        return "ABILITY_UNAWARE"
    if "magic bounce" in lower_name:
        return "ABILITY_MAGIC_BOUNCE"
    return default


def candidates_for(species_name, species_map, move_names, item_names, nature_names, abilities, raw):
    species = species_map.get(normalise(species_name))
    if species is None:
        return []
    if species.startswith("SPECIES_ARCEUS_"):
        ability = "ABILITY_MULTITYPE"
    else:
        ability = ABILITY_OVERRIDES.get(species, abilities.get(species))
    if ability is None:
        return []
    candidates = []
    for format_name, sets in raw.get(species_name, {}).items():
        if not valid_format(format_name):
            continue
        score = max((value for key, value in FORMAT_SCORE.items() if key in format_name.lower()), default=0)
        if score == 0:
            continue
        for set_name, data in sets.items():
            moves = [constant_name(move, "MOVE_", move_names) for move in data.get("moves", [])]
            moves = [move for move in moves if move is not None]
            if len(moves) != 4 or any(move in {"MOVE_TERA_BLAST", "MOVE_DYNAMAX_CANNON"} for move in moves):
                continue
            item = constant_name(data.get("item"), "ITEM_", item_names)
            nature = constant_name(data.get("nature"), "NATURE_", nature_names)
            if item is None or nature is None or unsupported_item(item):
                continue
            selected_ability = ability_for_set(species, ability, item, moves, set_name)
            evs = data.get("evs", {})
            if not isinstance(evs, dict):
                continue
            values = [evs.get(key, 0) for key in ("hp", "atk", "def", "spa", "spd", "spe")]
            if any(not isinstance(value, int) or value < 0 or value > 252 for value in values):
                continue
            candidates.append({
                "species": species,
                "ability": selected_ability,
                "item": item,
                "nature": nature,
                "moves": moves,
                "evs": values,
                "score": score,
                "source": format_name,
                "name": set_name,
            })
    unique = {}
    for candidate in candidates:
        key = (candidate["item"], candidate["nature"], tuple(candidate["moves"]))
        unique.setdefault(key, candidate)
    return sorted(unique.values(), key=lambda candidate: (candidate["score"], candidate["name"]))


def render_set(constant_name, candidate):
    evs = ", ".join(str(value) for value in candidate["evs"])
    moves = ", ".join(candidate["moves"])
    return (
        f"    FRONTIER_MODERN_SET({constant_name}, "
        f"{candidate['species']}, {candidate['ability']}, {candidate['item']}, "
        f"{candidate['nature']}, {evs}, {moves}),"
    )


def main():
    raw = json.load(urllib.request.urlopen(DATA_URL))
    species_map = build_species_map()
    abilities = build_abilities()
    move_names = read_names(CONSTANTS / "moves.h", "MOVE_")
    item_names = read_names(CONSTANTS / "items.h", "ITEM_")
    nature_names = read_names(CONSTANTS / "pokemon.h", "NATURE_")

    all_candidates = {}
    for species_name in raw:
        candidates = candidates_for(species_name, species_map, move_names, item_names, nature_names, abilities, raw)
        if candidates:
            all_candidates[species_name] = candidates

    selected_species = [name for name in all_candidates if name in ANCHORS]
    selected_species += [name for name in all_candidates if name not in ANCHORS]
    selected = []
    family_counts = {}
    for species_name in selected_species:
        candidates = all_candidates[species_name]
        family = family_name(species_name)
        limit = SPECIES_FAMILY_CAPS.get(family, 4)
        remaining = limit - family_counts.get(family, 0)
        if remaining <= 0:
            continue
        selected.extend(candidates[:remaining])
        family_counts[family] = family_counts.get(family, 0) + min(len(candidates), remaining)
    selected = sorted(selected, key=lambda candidate: (
        candidate["score"],
        candidate["species"] in FINAL_POOL_SPECIES,
        candidate["species"],
        candidate["name"],
    ))
    pool_size = (len(selected) + 7) // 8
    species_occurrences = {}
    constant_names = []
    for candidate in selected:
        species = candidate["species"].removeprefix("SPECIES_")
        species_occurrences[species] = species_occurrences.get(species, 0) + 1
        constant_names.append(f"FRONTIER_MON_GENERATED_{species}_{species_occurrences[species]}")

    constants = MON_CONSTANTS.read_text()
    constants = re.sub(r"#define FRONTIER_MON_TEST_STARMIE.*?// GENERATED FACTORY CONSTANTS START\n", "// GENERATED FACTORY CONSTANTS START\n", constants, flags=re.S)
    constants = re.sub(r"// GENERATED FACTORY CONSTANTS START\n.*?// GENERATED FACTORY CONSTANTS END\n", "", constants, flags=re.S)
    constant_lines = [f"#define {name} {GENERATED_START + index}" for index, name in enumerate(constant_names)]
    markers = []
    for pool in range(8):
        start = min(pool * pool_size, len(selected) - 1)
        end = min((pool + 1) * pool_size - 1, len(selected) - 1)
        markers.append(f"#define FRONTIER_MON_GENERATED_POOL_{pool}_START {constant_names[start]}")
        markers.append(f"#define FRONTIER_MON_GENERATED_POOL_{pool}_END {constant_names[end]}")
    generated_constants = "// GENERATED FACTORY CONSTANTS START\n" + "\n".join(constant_lines + markers) + "\n// GENERATED FACTORY CONSTANTS END\n"
    constants = re.sub(r"#define NUM_FRONTIER_MONS\s+\d+", generated_constants + f"#define NUM_FRONTIER_MONS           {GENERATED_START + len(selected)}", constants)
    constants = re.sub(r"#define FRONTIER_MONS_HIGH_TIER\s+\d+", f"#define FRONTIER_MONS_HIGH_TIER     {GENERATED_START + len(selected) - 1}", constants)
    MON_CONSTANTS.write_text(constants)

    data = MON_DATA.read_text()
    data = re.sub(r"    \[FRONTIER_MON_TEST_STARMIE\].*?    // GENERATED FACTORY DATA START\n", "    // GENERATED FACTORY DATA START\n", data, flags=re.S)
    data = re.sub(r"    // GENERATED FACTORY DATA START\n.*?    // GENERATED FACTORY DATA END\n", "", data, flags=re.S)
    generated = "\n".join(render_set(name, candidate) for name, candidate in zip(constant_names, selected))
    generated_data = "    // GENERATED FACTORY DATA START\n" + generated + "\n    // GENERATED FACTORY DATA END\n"
    data = data.replace("};\n\n#undef FRONTIER_MODERN_SET", generated_data + "};\n\n#undef FRONTIER_MODERN_SET")
    MON_DATA.write_text(data)
    manifest = []
    for index, candidate in enumerate(selected):
        manifest.append({"id": GENERATED_START + index, "constant": constant_names[index], **candidate})
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")

    factory = ROOT / "src/battle_factory.c"
    text = factory.read_text()
    level_ranges = "\n".join(
        f"    {{FRONTIER_MON_GENERATED_POOL_{pool}_START, FRONTIER_MON_GENERATED_POOL_{pool}_END}},"
        for pool in range(8)
    )
    open_ranges = "\n".join(
        f"    {{FRONTIER_MON_GENERATED_POOL_{min(pool + 2, 7)}_START, FRONTIER_MON_GENERATED_POOL_{min(pool + 2, 7)}_END}},"
        for pool in range(8)
    )
    replacement = "    // Level 50\n" + level_ranges + "\n\n    // Open level\n" + open_ranges
    text = re.sub(r"    // Level 50\n.*?\n};", replacement + "\n};", text, count=1, flags=re.S)
    factory.write_text(text)
    print(f"Generated {len(selected)} sets for {len(selected_species)} species")


if __name__ == "__main__":
    main()
