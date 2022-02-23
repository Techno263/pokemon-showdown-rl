import asyncio
import aiohttp
import aiofiles
import json
import os.path as path
import re

import time


dirname = path.dirname(__file__)

basic_url = r'https://www.smogon.com/dex/_rpc/dump-basics'
pokemon_url = r'https://www.smogon.com/dex/_rpc/dump-pokemon'
move_url = r'https://www.smogon.com/dex/_rpc/dump-move'
item_url = r'https://www.smogon.com/dex/_rpc/dump-item'
ability_url = r'https://www.smogon.com/dex/_rpc/dump-ability'


alpha_re = re.compile(r'[^a-zA-z0-9\-]')


def name_to_alias(name):
    name = name.replace(' ', '-')
    name = re.sub(alpha_re, '', name)
    return name


def handle_null_pokemon_resp(alias):
    if '-mega' in alias:
        return alias.replace('-mega', '')


def is_pokemon_valid(pokemon_data):
    return pokemon_data['isNonstandard'] == 'Standard'


async def get_pokemon_data(session, gen, pokemon_data):
    post_json = {
        'alias': name_to_alias(pokemon_data['name'].lower()),
        'gen': gen.lower(),
        'language': 'en'
    }
    async with session.post(pokemon_url, json=post_json) as resp:
        r_data = await resp.json()
    if r_data is None:
        r_data = {
            'learnset': []
        }
    oob = pokemon_data['oob']
    if oob is None:
        oob = {
            'dex_number': 0,
            'evos': [],
            'alts': [],
            'genfamily': []
        }
    assert len(set(pokemon_data['types'])) == len(pokemon_data['types'])
    assert len(set(pokemon_data['abilities'])) == len(pokemon_data['abilities'])
    assert len(set(r_data['learnset'])) == len(r_data['learnset'])
    assert len(set(oob['evos'])) == len(oob['evos'])
    assert len(set(oob['alts'])) == len(oob['alts'])
    return {
        'name': pokemon_data['name'],
        'dex_num': oob['dex_number'],
        'hp': pokemon_data['hp'],
        'atk': pokemon_data['atk'],
        'def': pokemon_data['def'],
        'spa': pokemon_data['spa'],
        'spd': pokemon_data['spd'],
        'spe': pokemon_data['spe'],
        'weight': pokemon_data['weight'],
        'height': pokemon_data['height'],
        'types': pokemon_data['types'],
        'abilities': pokemon_data['abilities'],
        'learnset': r_data['learnset'],
        'evos': oob['evos'],
        'alts': oob['alts']
    }


def is_move_valid(move_data):
    return move_data['isNonstandard'] == 'Standard'


async def get_move_data(session, gen, move_data):
    post_json = {
        'alias': name_to_alias(move_data['name'].lower()),
        'gen': gen.lower()
    }
    async with session.post(move_url, json=post_json) as resp:
        r_data = await resp.json()
    # This assert is to check if move flags is being used for something
    # Historically it has always been empty, and I want to know when/if it is
    #   used for something in the future
    assert len(move_data['flags']) == 0, 'move flags has values'
    assert len(set(r_data['pokemon'])) == len(r_data['pokemon'])
    return {
        'name': move_data['name'],
        'category': move_data['category'],
        'power': move_data['power'],
        'accuracy': move_data['accuracy'],
        'priority': move_data['priority'],
        'pp': move_data['pp'],
        'type': move_data['type'],
        'pokemon': r_data['pokemon']
    }


def is_item_valid(item_data):
    return item_data['isNonstandard'] == 'Standard'


async def get_item_data(session, gen, item_data):
    post_json = {
        'alias': name_to_alias(item_data['name'].lower()),
        'gen': gen.lower()
    }
    async with session.post(item_url, json=post_json) as resp:
        r_data = await resp.json()
    return {
        'name': item_data['name'],
        'pokemon': sorted(set(r_data['pokemon']))
    }


def is_ability_valid(ability_data):
    return ability_data['isNonstandard'] == 'Standard'


async def get_gen_data(session, gen_num, gen_data):
    gen = gen_data['shorthand']
    post_json = {'gen': gen.lower()}
    async with session.post(basic_url, json=post_json) as resp:
        r_data = await resp.json()
    pokemon_awaits = [
        get_pokemon_data(session, gen, pokemon)
        for pokemon in r_data['pokemon']
        if is_pokemon_valid(pokemon)
    ]
    move_awaits = [
        get_move_data(session, gen, move)
        for move in r_data['moves']
        if is_move_valid(move)
    ]
    item_awaits = [
        get_item_data(session, gen, item)
        for item in r_data['items']
        if is_item_valid(item)
    ]
    ability_data = [
        ability['name']
        for ability in r_data['abilities']
        if is_ability_valid(ability)
    ]
    type_data = [
        {
            'name': type_info['name'],
            'atk_eff': type_info['atk_effectives']
        }
        for type_info in r_data['types']
    ]
    pokemon_data = await asyncio.gather(*pokemon_awaits)
    move_data = await asyncio.gather(*move_awaits)
    item_data = await asyncio.gather(*item_awaits)
    return {
        'gen': gen,
        'num': gen_num,
        'name': gen_data['name'],
        'pokemon': pokemon_data,
        'moves': move_data,
        'abilities': ability_data,
        'items': item_data,
        'types': type_data
    }


async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.post(basic_url) as response:
            gens = await response.json()
        gen_awaits = [
            get_gen_data(session, gen_num, gen_data)
            for gen_num, gen_data in enumerate(gens, start=1)
        ]
        gen_data = await asyncio.gather(*gen_awaits)
        for data in gen_data:
            gen_num = data['num']
            gen = data['gen'].lower()
            filename = f'gen{gen_num}_{gen}.json'
            json_str = json.dumps(data, separators=(',', ':'))
            full_filename = path.join(dirname, filename)
            async with aiofiles.open(full_filename, 'wt') as fp:
                await fp.write(json_str)

    # need this so the aiohttp client session can close cleanly
    await asyncio.sleep(0.1)
        

def main():
    asyncio.run(get_data())


if __name__ == '__main__':
    main()
