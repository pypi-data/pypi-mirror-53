import itertools
from typing import Dict, List, Optional, Tuple
import sys

from sc2reader.events import *
from sc2reader.objects import Player
from sc2reader.resources import Replay
from sc2reader.data import Unit


def _find_closest_valid_hatchery_for_larva(
        larva: Unit, hatcheries: List[Unit]) -> Optional[Unit]:
    def check_if_hatchery_valid(hatchery: Unit) -> bool:
        return larva.finished_at > hatchery.finished_at and (
            hatchery.died_at is None or larva.finished_at < hatchery.died_at)

    def distance_to_larva(hatchery: Unit) -> int:
        if hasattr(hatchery, "location") and hasattr(larva, "location"):
            return (hatchery.location[0] - larva.location[0])**2 + (
                hatchery.location[1] - larva.location[1])**2
        else:
            return sys.maxsize

    valid_hatcheries = list(filter(check_if_hatchery_valid, hatcheries))
    return next(iter(sorted(valid_hatcheries, key=distance_to_larva)), None)


def _allocate_larvae_to_hatcheries(
        hatcheries: List[Unit], larvae: List[Unit]) -> Dict[Unit, List[Unit]]:
    result = dict((hatchery, []) for hatchery in hatcheries)

    for larva in larvae:
        hatchery = _find_closest_valid_hatchery_for_larva(larva, hatcheries)
        if hatchery is not None:
            result[hatchery].append(larva)

    for larvae in result.values():
        larvae.sort(key=lambda x: x.finished_at)

    return result


def _generate_larva_events(larvae: List[Unit]) -> List[Tuple[int, int]]:
    larvae_events = []
    for larva in larvae:
        larvae_events.append((larva.finished_at, 1))
        frame, _ = next(
            filter(lambda x: x[1].name == "Egg", larva.type_history.items()),
            (None, None))
        if frame is not None:
            larvae_events.append((frame, -1))
        elif larva.died_at is not None:
            larvae_events.append((larva.died_at, -1))
    return sorted(larvae_events, key=lambda x: x[0])


def larvae_blocks_per_hatchery_for_player(
        player: Player, replay: Replay) -> List[List[Tuple[int, bool]]]:
    hatcheries = list(
        set([
            x.unit for x in replay.tracker_events
            if ((isinstance(x, UnitInitEvent) or isinstance(x, UnitBornEvent))
                and x.unit.name in ["Hatchery", "Lair", "Hive"]
                and x.unit.owner == player and x.unit.finished_at is not None)
        ]))

    larvae = list(
        set([
            x.unit for x in replay.tracker_events
            if ((isinstance(x, UnitTypeChangeEvent) or isinstance(
                x, UnitBornEvent) or isinstance(x, UnitDiedEvent))
                and x.unit.name == "Larva" and x.unit.owner == player)
        ]))

    hatcheries_with_larvae = _allocate_larvae_to_hatcheries(hatcheries, larvae)
    larva_events_per_hatchery = dict(
        (hatchery, _generate_larva_events(larvae))
        for hatchery, larvae in hatcheries_with_larvae.items())

    larvae_blocks_per_hatchery = []
    for hatchery, larva_events in larva_events_per_hatchery.items():
        blocked = False
        larva_count = 0
        larvae_blocks = []
        for frame, delta in larva_events:
            larva_count += delta
            new_blocked = larva_count > 2

            if blocked != new_blocked:
                larvae_blocks.append((frame, new_blocked))

            blocked = new_blocked

        larvae_blocks_per_hatchery.append((hatchery, larvae_blocks))

    larvae_blocks_per_hatchery.sort(key=lambda x: x[0].finished_at)

    return [larvae_blocks for _, larvae_blocks in larvae_blocks_per_hatchery]
