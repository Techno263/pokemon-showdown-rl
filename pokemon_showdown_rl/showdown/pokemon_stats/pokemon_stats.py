import json
import os.path as path

from pokemon_showdown_rl.showdown.stats import Stats
from pokemon_showdown_rl.showdown.stats_entry import StatsEntry


_gen1_stats = None
_gen2_5_stats = None
_gen6_stats = None
_gen7_stats = None
_gen8_stats = None

_dir_name = path.dirname(__file__)


def _stat_obj_hook(obj):
    if (
        len(obj) == 7
        and 'num' in obj
        and 'name' in obj
        and 'hp' in obj
        and 'atk' in obj
        and 'def' in obj
        and 'spe' in obj
        and 'spc' in obj
    ):
        # gen 1 stats
        return StatEntry(
            obj['num'],
            obj['name'],
            Stats(
                obj['atk'], obj['def'], obj['spc'], obj['spc'], obj['spe']
            )
        )
    elif (
        len(obj) == 8
        and 'num' in obj
        and 'name' in obj
        and 'hp' in obj
        and 'atk' in obj
        and 'def' in obj
        and 'spa' in obj
        and 'spd' in obj
        and 'spe' in obj
    ):
        # gen 2-8 stats
        return StatEntry(
            obj['num'],
            obj['name'],
            Stats(
                obj['atk'], obj['def'], obj['spa'], obj['spd'], obj['spe']
            )
        )
    return obj


def get_stats(gen):
    if gen == 1:
        if _gen1_stats == None:
            filepath = path.join(_dir_name, 'stats_gen_1.json')
            with open(filepath, 'rt') as fp:
                _gen1_stats = json.load(fp, object_hook=_stat_obj_hook)
        return _gen1_stats
    elif gen in {2, 3, 4, 5}:
        if _gen2_5_stats == None:
            filepath = path.join(_dir_name, 'stats_gen_2-5.json')
            with open(filepath, 'rt') as fp:
                _gen2_5_stats = json.load(fp, object_hook=_stat_obj_hook)
        return _gen2_5_stats
    elif gen == 6:
        if _gen6_stats == None:
            filepath = path.join(_dir_name, 'stats_gen_6.json')
            with open(filepath, 'rt') as fp:
                _gen6_stats = json.load(fp, object_hook=_stat_obj_hook)
        return _gen6_stats
    elif gen == 7:
        if _gen7_stats == None:
            filepath = path.join(_dir_name, 'stats_gen_7.json')
            with open(filepath, 'rt') as fp:
                _gen7_stats = json.load(fp, object_hook=_stat_obj_hook)
        return _gen7_stats
    elif gen == 8:
        if _gen8_stats == None:
            filepath = path.join(_dir_name, 'stats_gen_8.json')
            with open(filepath, 'rt') as fp:
                _gen8_stats = json.load(fp, object_hook=_stat_obj_hook)
        return _gen8_stats
