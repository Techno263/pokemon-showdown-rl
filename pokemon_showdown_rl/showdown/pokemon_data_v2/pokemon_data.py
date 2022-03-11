import pokemon_showdown_rl.showdown.pokemon_data_v2.load_pokemon_data as load_pokemon_data
from pokemon_showdown_rl.showdown.pokemon_data_v2.get_pokemon_data import data_exists

# Ensure showdown data is downloaded
data_exists()


def showdown_formats():
    return load_pokemon_data.load_formats()


def get_pokemon_data(showdown_format):
    pass
