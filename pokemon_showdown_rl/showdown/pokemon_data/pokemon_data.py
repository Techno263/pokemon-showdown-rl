import os.path as path
import json

from enum import IntEnum
from dataclasses import dataclass
from pokemon_showdown_rl.showdown.pokemon_data.pokemon_entry import PokemonEntry
from pokemon_showdown_rl.showdown.pokemon_data.move_entry import MoveEntry
from pokemon_showdown_rl.showdown.pokemon_data.item_entry import ItemEntry

dirname = path.dirname(__file__)


class PokemonGen(IntEnum):
    GEN_1 = 1
    RED_BLUE = GEN_1
    RB = GEN_1

    GEN_2 = 2
    GOLD_SILVER = GEN_2
    GS = GEN_2

    GEN_3 = 3
    RUBY_SAPPHIRE = GEN_3
    RS = GEN_3

    GEN_4 = 4
    DIAMOND_PEARL = GEN_4
    DP = GEN_4

    GEN_5 = 5
    BLACK_WHITE = GEN_5
    BW = GEN_5

    GEN_6 = 6
    X_Y = GEN_6
    XY = GEN_6

    GEN_7 = 7
    SUN_MOON = GEN_7
    SM = GEN_7

    GEN_8 = 8
    SWORD_SHIELD = GEN_8
    SS = GEN_8


def get_data_filename(gen):
    if gen == PokemonGen.GEN_1:
        filename = 'gen1_rb.json'
    elif gen == PokemonGen.GEN_2:
        filename = 'gen2_gs.json'
    elif gen == PokemonGen.GEN_3:
        filename = 'gen3_rs.json'
    elif gen == PokemonGen.GEN_4:
        filename = 'gen4_dp.json'
    elif gen == PokemonGen.GEN_5:
        filename == 'gen5_bw.json'
    elif gen == PokemonGen.GEN_6:
        filename = 'gen6_xy.json'
    elif gen == PokemonGen.GEN_7:
        filename = 'gen7_sm.json'
    elif gen == PokemonGen.GEN_8:
        filename = 'gen8_ss.json'
    else:
        raise Exception(f'Invalid gen, {gen}')
    return path.join(dirname, filename)


def _pokemon_data_object_hook(json_data):
    pokemon_data_keys = {
        'gen', 'num', 'name', 'pokemon', 'moves', 'abilities', 'items', 'types'
    }
    pokemon_keys = {
        'name', 'dex_num', 'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'weight',
        'height', 'types', 'abilities', 'learnset', 'evos', 'alts'
    }
    move_keys = {
        'name', 'category', 'power', 'accuracy', 'priority', 'pp', 'type',
        'pokemon'
    }
    item_keys = {'name', 'pokemon'}
    if (
        len(pokemon_data_keys) == len(json_data.keys())
        and all(key in json_data for key in pokemon_data_keys)
    ):
        return PokemonData.from_json(json_data)
    elif (
        len(pokemon_keys) == len(json_data.keys())
        and all(key in json_data for key in pokemon_keys)
    ):
        return PokemonEntry.from_json(json_data)
    elif (
        len(move_keys) == len(json_data.keys())
        and all(key in json_data for key in move_keys)
    ):
        return MoveEntry.from_json(json_data)
    elif (
        len(item_keys) == len(json_data.keys())
        and all(key in json_data for key in item_keys)
    ):
        return ItemEntry.from_json(json_data)


def get_pokemon_data(gen):
    filename = get_data_filename(gen)
    with open(filename, 'rt') as fp:
        return json.load(fp, object_hook=_pokemon_data_object_hook)


@dataclass
class PokemonData:
    gen_num: int
    gen_name: str
    gen_short_name: str
    pokemon: list
    moves: list
    abilities: list
    items: list
    types: list

    @staticmethod
    def from_json(json_data):
        return PokemonData(
            json_data['num'], json_data['name'], json_data['gen'],
            json_data['pokemon'], json_data['moves'], json_data['abilities'],
            json_data['items'], json_data['types']
        )

if __name__ == '__main__':
    x = get_pokemon_data(PokemonGen.GEN_1)
    print(x)
