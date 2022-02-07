import aiohttp
from pokemon_showdown_rl.state.state import user
from pokemon_showdown_rl.util.logging import get_logger

async def get_assertion_no_auth(challstr, username):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            r'https://play.pokemonshowdown.com/action.php',
            json = {
                'act': 'getassertion',
                'userid': username,
                'challstr': challstr
            }
        ) as response:
            return await response.text()

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'init' and msg_data == 'chat':
        logger = get_logger(context.username)
        assertion = await get_assertion_no_auth(context.challstr, context.username)
        logger.write(f'|/trn {context.username},0,{assertion}\n')
        await websocket.send(f'|/trn {context.username},0,{assertion}')
        context.update_state(user)
