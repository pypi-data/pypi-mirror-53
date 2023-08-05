import itertools
from collections import OrderedDict
from typing import Dict, Tuple, List, Set, Union

from sc2reader.data import Unit
from sc2reader.events import UnitBornEvent, UnitDoneEvent
from sc2reader.objects import Player
from sc2reader.resources import Replay

from .gametime import frame_to_second
from .util import production_structure_types, get_unit_type, get_unit_type_name, get_structure_type, get_production_duration, is_unit_produced

ORBITAL_TRANSFORMATION_DURATION = 25
PLANETARY_FORTRESS_TRANSFORMATION_DURATION = 36


def _order_by_tech_tier(args):
    structure_type = args[0]
    return (production_structure_types() + ["Unknown"]).index(structure_type)


def _extract_production_structures(unit_events: List[Union[UnitBornEvent, UnitDoneEvent]]) -> Set[Unit]:
    return set(
        event.unit
        for event
        in unit_events
        if get_unit_type_name(event.unit) in production_structure_types())


def _extract_produced_units(unit_events: List[Union[UnitBornEvent, UnitDoneEvent]]) -> Set[Unit]:
    return set(
        event.unit
        for event
        in unit_events
        if is_unit_produced(event.unit))


def _terran_production_used_and_capacity_events(
        replay: Replay,
        produced_units: Set[Unit],
        production_structures: Set[Unit],
        reactors: Set[Unit],
        limit_seconds: int = 0) -> Tuple[List[Tuple[str, float, int]], List[Tuple[str, float, int]]]:

    production_events = list(itertools.chain.from_iterable(
        filter(
            lambda x: x[1] <= limit_seconds,
            [
                (get_structure_type(get_unit_type(unit)),
                 frame_to_second(unit.finished_at) - get_production_duration(get_unit_type(unit), replay),
                 1),
                (get_structure_type(get_unit_type(unit)),
                 frame_to_second(unit.finished_at),
                 -1)])
        for unit
        in produced_units
        if unit.finished_at > 0))
    production_events.sort(key=lambda x: x[1])

    production_capacity_events = []
    for unit in production_structures:
        second_finished_at = frame_to_second(unit.finished_at)
        if second_finished_at <= limit_seconds:
            production_capacity_events.append((get_unit_type_name(unit), second_finished_at, 1))

        if unit.died_at is not None:
            second_died_at = frame_to_second(unit.died_at)
            if second_died_at <= limit_seconds:
                production_capacity_events.append((get_unit_type_name(unit), second_died_at, -1))

        was_flying = False
        for frame, unit_type in unit.type_history.items():
            if frame <= unit.finished_at:
                continue

            second = frame_to_second(frame)
            if second > limit_seconds:
                continue

            if "Flying" in unit_type.name:
                production_capacity_events.append((get_unit_type_name(unit), second, -1))
                was_flying = True
            elif was_flying:
                production_capacity_events.append((get_unit_type_name(unit), second, 1))
                was_flying = False
            elif "OrbitalCommand" in unit.name:
                production_capacity_events.append(
                    (get_unit_type_name(unit), second - ORBITAL_TRANSFORMATION_DURATION, -1))
                production_capacity_events.append((get_unit_type_name(unit), second, 1))
            elif "PlanetaryFortress" in unit.name:
                production_capacity_events.append(
                    (
                        get_unit_type_name(unit),
                        second - PLANETARY_FORTRESS_TRANSFORMATION_DURATION,
                        -1))
                production_capacity_events.append((get_unit_type_name(unit), second, 1))

    for unit in reactors:
        previous_structure_type = "Unknown"
        for frame, unit_type in unit.type_history.items():
            transformed_second = frame_to_second(frame)

            if transformed_second > limit_seconds:
                continue

            if previous_structure_type != "Unknown":
                production_capacity_events.append((previous_structure_type, transformed_second, -1))

            previous_structure_type = get_structure_type(unit_type)

            if previous_structure_type != "Unknown":
                production_capacity_events.append((previous_structure_type, transformed_second, 1))

    production_capacity_events.sort(key=lambda x: x[1])

    return production_events, production_capacity_events


def production_used_out_of_capacity_for_player(
        limit_seconds: int,
        player: Player,
        replay: Replay) -> Tuple[Dict[str, List[Tuple[float, int]]], Dict[str, List[Tuple[float, int]]]]:

    unit_events = [
        event
        for event
        in replay.events
        if (event.name in ["UnitBornEvent", "UnitDoneEvent"] and
            event.unit.owner == player)]

    produced_units = _extract_produced_units(unit_events)
    production_structures = _extract_production_structures(unit_events)

    if player.play_race == "Terran":
        reactors = set(
            event.unit
            for event
            in unit_events
            if "Reactor" in event.unit.name)

        production_used_events, production_capacity_events = _terran_production_used_and_capacity_events(
            replay,
            produced_units,
            production_structures,
            reactors,
            limit_seconds)
    else:
        production_used_events, production_capacity_events = [], []

    production_used = {}
    for structure_type, time, modified_production in production_used_events:
        if structure_type not in production_used:
            current_production = 0
            production_used[structure_type] = [(time - 0.00001, current_production)]
        else:
            current_production = production_used[structure_type][-1][1]

        production_used[structure_type].append((time, current_production + modified_production))

    production_capacity = {}
    for structure_type, time, modified_production_capacity in production_capacity_events:
        if structure_type not in production_capacity:
            current_production_capacity = 0
            production_capacity[structure_type] = [(time, current_production_capacity)]
        else:
            current_production_capacity = production_capacity[structure_type][-1][1]

        production_capacity[structure_type].append(
            (time, current_production_capacity + modified_production_capacity))

    analysis_end_second = min(limit_seconds, frame_to_second(replay.frames))

    for key in production_used.keys():
        production_used[key].append((analysis_end_second, production_used[key][-1][1]))

        if (key in production_capacity and
                production_capacity[key] and
                production_used[key] and
                    production_capacity[key][0][0] <= production_used[key][0][0]):
            production_used[key] = [(production_capacity[key][0][0], 0)] + production_used[key]

    for key in production_capacity.keys():
        production_capacity[key].append((analysis_end_second, production_capacity[key][-1][1]))

    return (
        OrderedDict(sorted(production_used.items(), key=_order_by_tech_tier)),
        OrderedDict(sorted(production_capacity.items(), key=_order_by_tech_tier)))


def production_used_till_time_for_player(
        limit_seconds: int, player: Player, replay: Replay) -> Dict[str, List[Tuple[float, int]]]:

    return production_used_out_of_capacity_for_player(limit_seconds, player, replay)[0]


def production_capacity_till_time_for_player(
        limit_seconds: int, player: Player, replay: Replay) -> Dict[str, List[Tuple[float, int]]]:

    return production_used_out_of_capacity_for_player(limit_seconds, player, replay)[1]
