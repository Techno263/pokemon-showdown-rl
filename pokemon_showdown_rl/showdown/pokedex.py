import json
import requests

url = r'https://play.pokemonshowdown.com'

data_paths = {
    'pokedex': '/data/pokedex.json',
    'moves': '/data/moves.json'
}

def load_data(path):
    r = requests.get(url + path)
    return r.json()

data = {
    name: load_data(path)
    for name, path in data_paths.items()
}

def get_pokedex():
    return data['pokedex']

def get_abilities():
    return data['abilities']

def get_items():
    return data['items']

def get_moves():
    return data['moves']

def get_type_chart():
    return data['typechart']

print(get_pokedex())
print(get_abilities())
print(get_items())
print(get_moves())
print(get_type_chart())

print(type(get_pokedex()))
print(type(get_abilities()))
print(type(get_items()))
print(type(get_moves()))
print(type(get_type_chart()))
