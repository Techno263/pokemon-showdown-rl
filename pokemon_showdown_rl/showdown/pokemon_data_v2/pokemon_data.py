import pokemon_showdown_rl.showdown.pokemon_data_v2.load_pokemon_data as load_pokemon_data
from pokemon_showdown_rl.showdown.pokemon_data_v2.get_pokemon_data import data_exists


# Ensure showdown data is downloaded
data_exists()


def showdown_formats():
    return load_pokemon_data.load_formats()


def get_format_info(showdown_format):
    formats = load_pokemon_data.load_formats()
    return formats[showdown_format]


def get_pokemon_data(showdown_format):
    format_info = get_format_info(showdown_format)
    team_builder = load_pokemon_data.load_team_builder()
    mod = team_builder['base']
    if format_info.mod != team_builder['base']:
        pass
