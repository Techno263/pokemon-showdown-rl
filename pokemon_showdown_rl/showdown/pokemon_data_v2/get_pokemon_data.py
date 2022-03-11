import asyncio
import aiohttp
import shutil
import os
import os.path as path
import re
import json
import pokemon_showdown_rl.showdown.pokemon_data_v2.data_file_paths as dp


base_mod_regex = re.compile(
    r"^const BASE_MOD = '(?P<base_mod>[A-Za-z0-9_]+)' as ID;$",
    re.MULTILINE
)

showdown_dex_ts_url = r'https://play.pokemonshowdown.com/data/pokemon-showdown/sim/dex.ts'
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


async def run_in_node(js_code):
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
    return stdout_resp.decode('utf8')


async def get_showdown_base_mod(session):
    async with session.get(showdown_dex_ts_url) as resp:
        resp_text = await resp.text()
    match = re.search(base_mod_regex, resp_text)
    assert match != None
    base_mod = match.group('base_mod')
    return base_mod


async def scrape_json_data(
    js_code, start_text, open_brace, close_brace, js_wrapper
):
    assert js_code.find(start_text) == 0
    js_code, i = clip_to_braces(js_code, open_brace, close_brace)
    assert i == len(start_text)
    js_code = js_wrapper.format(js_code)
    json_str = await run_in_node(js_code)
    json_data = json.loads(json_str)
    return json_data


async def get_showdown_pokedex(session):
    # Reqeust pokedex data
    async with session.get(showdown_pokedex_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattlePokedex = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    with open(dp.pokedex_path, 'wt', encoding='utf8') as fp:
        json.dump(json_data, fp, separators=(',', ':'))


async def get_showdown_team_builder(session):
    async with session.get(showdown_team_builder_url) as resp:
        resp_text = await resp.text()
    start_text = "// DO NOT EDIT - automatically built with build-tools/build-indexes\n\nexports.BattleTeambuilderTable = JSON.parse"
    js_wrapper = 'JSON.stringify(JSON.parse{});'
    json_data = await scrape_json_data(resp_text, start_text, '(', ')', js_wrapper)
    base_mod = await get_showdown_base_mod(session)
    base_mod_keys = {
        'tiers', 'items', 'overrideTier', 'zuBans', 'monotypeBans', 'formatSlices',
        'learnsets'
    }
    mods = {
        'base': base_mod,
        'base_mod': {
            'tiers': json_data['tiers'],
            'items': json_data['items'],
            'overrideTier': json_data['overrideTier'],
            'zuBans': json_data['zuBans'],
            'monotypeBans': json_data['monotypeBans'],
            'formatSlices': json_data['formatSlices'],
            'learnsets': json_data['learnsets'],
        },
        'mods': {
            k: v
            for k, v in json_data.items()
            if k not in base_mod_keys
        }
    }
    with open(dp.team_builder_path, 'wt', encoding='utf8') as fp:
        json.dump(mods, fp, separators=(',', ':'))


async def get_showdown_learnset(session):
    async with session.get(showdown_learnset_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleLearnsets = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    learnset = {
        k: v.get('learnset', {})
        for k, v in json_data.items()
    }
    with open(dp.learnset_path, 'wt', encoding='utf8') as fp:
        json.dump(learnset, fp, separators=(',', ':'))


# Move Flag data
# bypasssub: ignores a target's substitute
# bite: power multiplied by 1.5 when used by pokemon with Strong Jaw ability
# bullet

async def get_showdown_moves(session):
    async with session.get(showdown_moves_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleMovedex = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    moves = {}
    for move_id, move_data in json_data.items():
        assert move_id not in moves
        acc = move_data['accuracy']
        never_miss = isinstance(acc, bool) and acc == True
        accuracy = 100 if never_miss else acc
        
        moves[move_id] = {
            'name': move_data['name'],
            'num': move_data['num'],
            'power': move_data['basePower'],
            'accuracy': accuracy,
            'never_miss': never_miss,
            'pp': move_data['pp'],
            'category': move_data['category'],
            'type': move_data['type'],
            'priority': move_data['priority'],
            'target': move_data['target'],
            'flags': {
                'bypasssub': move_data['flags'].get('bypasssub', 0),
                'bite': move_data['flags'].get('bite', 0)
            }
        }
    keys = set()
    flags = set()
    for obj in json_data.values():
        keys.update(obj.keys())
        if 'flags' in obj:
            flags.update(obj['flags'].keys())
    print('keys', sorted(keys))
    print('flags', sorted(flags))
    with open(dp.moves_path, 'wt', encoding='utf8') as fp:
        json.dump(json_data, fp, separators=(',', ':'))


async def get_showdown_abilities(session):
    async with session.get(showdown_abilities_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleAbilities = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    abilities = {}
    for ability_id, ability_data in json_data.items():
        assert ability_id not in abilities
        abilities[ability_id] = {
            'name': ability_data['name'],
            'rating': ability_data['rating'],
            'num': ability_data['num'],
            'desc': ability_data['desc'],
            'short_desc': ability_data['shortDesc']
        }
    with open(dp.abilities_path, 'wt', encoding='utf8') as fp:
        json.dump(abilities, fp, separators=(',', ':'))


async def get_showdown_items(session):
    async with session.get(showdown_items_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleItems = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    with open(dp.items_path, 'wt', encoding='utf8') as fp:
        json.dump(json_data, fp, separators=(',', ':'))


async def get_showdown_formats_data(session):
    async with session.get(showdown_format_data_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleFormatsData = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    with open(dp.formats_data_path, 'wt', encoding='utf8') as fp:
        json.dump(json_data, fp, separators=(',', ':'))


# conversion copied from
# https://github.com/smogon/pokemon-showdown-client/blob/623a2902d0e4c352e68d550c0af2642bea2b2425/src/battle-dex.ts#L35
def format_name_to_format_id(format_name):
    pattern = re.compile(r'[^a-z0-9]+', )
    return pattern.sub('', format_name.lower())


async def get_showdown_formats(session):
    async with session.get(showdown_formats_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.Formats = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '[', ']', js_wrapper)
    format_data = {}
    section = ''
    for item in json_data:
        if 'section' in item:
            section = item['section']
        else:
            if 'battle' in item:
                assert item['battle'] == {}
            if 'field' in item:
                assert item['field'] == {}
            if 'pokemon' in item:
                assert item['pokemon'] == {}
            showdown_format = {
                'name': item['name'],
                'mod': item.get('mod', ''),
                'section': section,
                'desc': item.get('desc', ''),
                'game_type': item.get('gameType', 'singles'),
                'team': item.get('team', ''),
                'ruleset': item.get('ruleset', []),
                'banlist': item.get('banlist', []),
                'unbanlist': item.get('unbanlist', []),
                'restricted': item.get('restricted', [])
            }
            format_id = format_name_to_format_id(item['name'])
            assert format_id not in format_data
            format_data[format_id] = showdown_format
    with open(dp.formats_path, 'wt', encoding='utf8') as fp:
        json.dump(format_data, fp, separators=(',', ':'))


async def get_showdown_typechart(session):
    async with session.get(showdown_typechart_url) as resp:
        resp_text = await resp.text()
    start_text = 'exports.BattleTypeChart = '
    js_wrapper = 'JSON.stringify({});'
    json_data = await scrape_json_data(resp_text, start_text, '{', '}', js_wrapper)
    with open(dp.typechart_path, 'wt', encoding='utf8') as fp:
        json.dump(json_data, fp, separators=(',', ':'))


async def data_exists():
    if not path.exists(dp.data_dir):
        os.mkdir(data_dir)
    awaits = []
    async with aiohttp.ClientSession() as session:
        if not path.exists(dp.pokedex_path):
            awaits.append(get_showdown_pokedex(session))
        if not path.exists(dp.team_builder_path):
            awaits.append(get_showdown_team_builder(session))
        if not path.exists(dp.learnset_path):
            awaits.append(get_showdown_learnset(session))
        if not path.exists(dp.moves_path):
            awaits.append(get_showdown_moves(session))
        if not path.exists(dp.abilities_path):
            awaits.append(get_showdown_abilities(session))
        if not path.exists(dp.items_path):
            awaits.append(get_showdown_items(session))
        if not path.exists(dp.formats_data_path):
            awaits.append(get_showdown_formats_data(session))
        if not path.exists(dp.formats_path):
            awaits.append(get_showdown_formats(session))
        if not path.exists(dp.typechart_path):
            awaits.append(get_showdown_typechart(session))
        if len(awaits) > 0:
            await asyncio.gather(*awaits)
    # Need this so the aiohttp client session can close cleanly
    await asyncio.sleep(0.01)


async def get_data():
    if not path.exists(data_dir):
        os.mkdir(data_dir)

    async with aiohttp.ClientSession() as session:
        base_mod_aw = get_showdown_base_mod(session)
        abilities_aw = get_showdown_abilities(session)
        format_data_aw = get_showdown_formats_data(session)
        formats_aw = get_showdown_formats(session)
        items_aw = get_showdown_items(session)
        learnset_aw = get_showdown_learnset(session)
        moves_aw = get_showdown_moves(session)
        pokedex_aw = get_showdown_pokedex(session)
        team_builder_aw = get_showdown_team_builder(session)
        typechart_aw = get_showdown_typechart(session)

        base_mod = await base_mod_aw
        abilities = await abilities_aw
        format_data = await format_data_aw
        formats = await formats_aw
        items = await items_aw
        learnset = await learnset_aw
        moves = await moves_aw
        pokedex = await pokedex_aw
        team_builder = await team_builder_aw
        typechart = await typechart_aw

    # Need this so the aiohttp client session can close cleanly
    await asyncio.sleep(0.1)


def main():
    if shutil.which('node') == None:
        print('Cannot process pokemon data. Missing required dependency Node.js')
        return
    asyncio.run(get_data())


if __name__ == '__main__':
    main()
