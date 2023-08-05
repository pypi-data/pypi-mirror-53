import itertools

from typing import Set, List, Tuple

from sc2reader.objects import Player
from sc2reader.resources import Replay
from sc2reader.data import Unit

CREEP_TUMOUR_COOLDOWN_BLIZZARD_SECONDS = 15 * 1.4


def _get_creep_tumours(player: Player, replay: Replay) -> Set[Unit]:
    return set([
        event.unit for event in replay.events
        if (event.name in ["UnitBornEvent", "UnitDoneEvent"] and event.unit.
            owner == player and event.unit.name == "CreepTumorBurrowed")
    ])


def creep_tumours_built_before_second(second: int, player: Player,
                                      replay: Replay) -> int:
    creep_tumours = _get_creep_tumours(player, replay)
    creep_tumour_started_times = [
        int(creep_tumour.started_at / (1.4 * replay.game_fps))
        for creep_tumour in creep_tumours
    ]
    return len([time for time in creep_tumour_started_times if time < second])


def creep_tumour_state_changes(player: Player,
                               replay: Replay) -> List[Tuple[int, int]]:
    def calculate_start_and_finish(
            creep_tumour: Unit) -> List[Tuple[int, int]]:
        start = creep_tumour.started_at
        finish = creep_tumour.finished_at + CREEP_TUMOUR_COOLDOWN_BLIZZARD_SECONDS * replay.game_fps
        return [(int(start), 1), (int(finish), -1)]

    creep_tumours = _get_creep_tumours(player, replay)
    creep_tumour_start_and_finish = [
        calculate_start_and_finish(creep_tumour)
        for creep_tumour in creep_tumours
    ]
    creep_tumour_states: List[Tuple[int, int]] = list(
        itertools.chain(*creep_tumour_start_and_finish))
    creep_tumour_states.sort(key=lambda x: x[0])
    return creep_tumour_states
