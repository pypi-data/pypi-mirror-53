from typing import List, Optional

from sc2reader.data import Unit, UnitType
from sc2reader.resources import Replay


PRODUCTION_STRUCTURE_TYPES = [
    "CommandCenter",
    "Nexus",
    "Barracks",
    "Gateway",
    "Factory",
    "RoboticsFacility",
    "Starport",
    "Stargate"
]


def is_unit_produced(unit: Unit) -> bool:
    return (
        not unit.hallucinated
        and unit.name is not None
        and unit.name not in ["MULE", "AutoTurret"] and (
            "TechLab" in unit.name or
            "Reactor" in unit.name or
            "Liberator" in unit.name or
            "Cyclone" in unit.name or
            unit.is_army or
            unit.is_worker))


def production_structure_types() -> List[str]:
    return PRODUCTION_STRUCTURE_TYPES


def get_production_duration(unit_type: UnitType, replay: Replay) -> float:
    if "Reactor" in unit_type.name:
        build_time = 50
    elif "TechLab" in unit_type.name:
        build_time = 25
    elif unit_type.name == "Cyclone":
        build_time = 45
    elif unit_type.name == "Liberator":
        build_time = 60
    elif unit_type.name == "BattleHellion":
        build_time = 30
    else:
        matching_build_times = [
            ability.build_time
            for ability
            in replay.datapack.abilities.values()
            if ability.is_build and ability.build_unit.name == unit_type.name]

        if not matching_build_times:
            raise Exception("Unknown build time for unit: " + unit_type.name)

        build_time = matching_build_times[0]

    return build_time / 1.44


def get_unit_type(unit: Unit) -> Optional[UnitType]:
    return next(iter(unit.type_history.values()), None)


def get_unit_type_name(unit: Unit) -> str:
    unit_type = next(iter(unit.type_history.values()), None)
    return unit_type.name if unit_type is not None else ""


def get_structure_type(unit_type: UnitType) -> str:
    unit_name = unit_type.name

    if "Barracks" in unit_name:
        return "Barracks"

    if "Factory" in unit_name:
        return "Factory"

    if "Starport" in unit_name:
        return "Starport"

    if unit_name == "SCV":
        return "CommandCenter"

    if unit_name in ["Marine", "Marauder", "Reaper", "Ghost"]:
        return "Barracks"

    if unit_name in ["Hellion", "BattleHellion", "Cyclone", "SiegeTank", "Thor", "WidowMine"]:
        return "Factory"

    if unit_name in ["Medivac", "Viking", "Liberator", "Raven", "Banshee", "Battlecruiser"]:
        return "Starport"

    if unit_name in ["Probe", "MothershipCore", "Mothership"]:
        return "Nexus"

    if unit_name in ["Zealot", "Stalker", "Adept", "Sentry", "DarkTemplar", "HighTemplar"]:
        return "Gateway"

    if unit_name in ["Immortal", "WarpPrism", "Colossus", "Disruptor", "Observer"]:
        return "RoboticsFacility"

    if unit_name in ["Phoenix", "VoidRay", "Carrier", "Tempest", "Oracle"]:
        return "Stargate"

    return "Unknown"