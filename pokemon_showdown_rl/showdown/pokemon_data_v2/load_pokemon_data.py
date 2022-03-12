import json
import pokemon_showdown_rl.showdown.pokemon_data_v2.data_file_paths as dp
from pokemon_showdown_rl.showdown.pokemon_data_v2.showdown_format import ShowdownFormat


_formats_keys = {
    'name', 'mod', 'section', 'desc', 'game_type', 'team', 'ruleset', 'banlist',
    'unbanlist', 'restricted'
}


def formats_object_hook(json_data):
    if (
        len(_formats_keys) == len(json_data.keys())
        and all(k in _formats_keys for k in json_data)
    ):
        return ShowdownFormat.from_json(json_data)
    return json_data


def load_abilities():
    with open(dp.abilities_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_formats_data():
    with open(dp.formats_data_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_formats():
    with open(dp.formats_path, 'rt') as fp:
        return json.load(fp, object_hook=formats_object_hook)


def load_items():
    with open(dp.items_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_learnset():
    with open(dp.learnset_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_moves():
    with open(dp.moves_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_pokedex():
    with open(dp.pokedex_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_team_builder():
    with open(dp.team_builder_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)


def load_typechart_builder():
    with open(dp.typechart_path, 'rt') as fp:
        return json.load(fp, object_hook=json_object_hook)