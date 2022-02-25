import asyncio
import aiohttp
import shutil
import os.path as path
import re

import json


dirname = path.dirname(__file__)

#smogon_basic_url = r'https://www.smogon.com/dex/_rpc/dump-basics'
#smogon_pokemon_url = r'https://www.smogon.com/dex/_rpc/dump-pokemon'
#smogon_move_url = r'https://www.smogon.com/dex/_rpc/dump-move'
#smogon_item_url = r'https://www.smogon.com/dex/_rpc/dump-item'
#smogon_ability_url = r'https://www.smogon.com/dex/_rpc/dump-ability'
showdown_abilities_url = r'https://play.pokemonshowdown.com/data/abilities.js'
showdown_format_data_url = r'https://play.pokemonshowdown.com/data/formats-data.js'
showdown_formats_url = r'https://play.pokemonshowdown.com/data/formats.js'
showdown_items_url = r'https://play.pokemonshowdown.com/data/items.js'
showdown_learnset_url = r'https://play.pokemonshowdown.com/data/learnsets.js'
showdown_moves_url = r'https://play.pokemonshowdown.com/data/moves.js'
showdown_pokedex_url = r'https://play.pokemonshowdown.com/data/pokedex.js'
showdown_team_builder_url = r'https://play.pokemonshowdown.com/data/teambuilder-tables.js'
showdown_typechart_url = r'https://play.pokemonshowdown.com/data/typechart.js'


def clip_to_braces(string, open_brace, close_brace):
    has_started = False
    brace_count = 0
    start_index = 0
    for i, c in enumerate(string):
        if c == open_brace:
            brace_count += 1
            if not has_started:
                start_index = i
                has_started = True
        elif c == close_brace:
            brace_count -= 1
            if brace_count == 0:
                return string[start_index:i+1], start_index
    return None, -1


async def convert_js_to_json(js_code):
    js_code = f'JSON.stringify({js_code});'
    node_exe_path = shutil.which('node')
    if node_exe_path == None:
        raise Exception('Unable to find node')
    node = await asyncio.create_subprocess_exec(
        node_exe_path, '-p',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    stdout_resp, _ = await node.communicate(input=js_code.encode('utf8'))
    assert node.returncode == 0
    return stdout_resp


async def get_showdown_pokedex(session):
    async with session.get(showdown_pokedex_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattlePokedex = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'pokedex.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_team_builder(session):
    async with session.get(showdown_team_builder_url) as resp:
        resp_text = await resp.text()
    front_text = "// DO NOT EDIT - automatically built with build-tools/build-indexes\n\nexports.BattleTeambuilderTable = JSON.parse('"
    assert resp_text.find(front_text) == 0
    json_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    filename = path.join(dirname, 'team_builder.json')
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_obj)


async def get_showdown_learnset(session):
    async with session.get(showdown_learnset_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleLearnsets = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'learnset.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_moves(session):
    async with session.get(showdown_moves_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleMovedex = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'moves.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_abilities(session):
    async with session.get(showdown_abilities_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleAbilities = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'abilities.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_items(session):
    async with session.get(showdown_items_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleItems = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'items.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_format_data(session):
    async with session.get(showdown_format_data_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleFormatsData = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'formats_data.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_formats(session):
    async with session.get(showdown_formats_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.Formats = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '[', ']')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'formats.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_showdown_typechart(session):
    async with session.get(showdown_typechart_url) as resp:
        resp_text = await resp.text()
    front_text = 'exports.BattleTypeChart = '
    assert resp_text.find(front_text) == 0
    js_obj, i = clip_to_braces(resp_text, '{', '}')
    assert i == len(front_text)
    json_data = await convert_js_to_json(js_obj)
    json_data = json_data.decode('utf8')
    filename = path.join(dirname, 'typechart.json')
    #with open(filename, 'wb') as fp:
    with open(filename, 'wt', encoding='utf8') as fp:
        fp.write(json_data)


async def get_data():
    async with aiohttp.ClientSession() as session:
        awaitables = [
            get_showdown_abilities(session),
            get_showdown_format_data(session),
            get_showdown_formats(session),
            get_showdown_items(session),
            get_showdown_learnset(session),
            get_showdown_moves(session),
            get_showdown_pokedex(session),
            get_showdown_team_builder(session),
            get_showdown_typechart(session)
        ]
        await asyncio.gather(*awaitables)
    # Need this so the aiohttp client session can close cleanly
    await asyncio.sleep(0.1)


def main():
    if shutil.which('node') == None:
        print('Cannot process pokemon data. Missing required dependency Node.js')
        return
    asyncio.run(get_data())


if __name__ == '__main__':
    main()
