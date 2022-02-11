import aiohttp
from pokemon_showdown_rl.state.client_state import lobby

# Join lobby state
# Uses challstr to create an unauthenticated account
# Once logged in moves to user state

name = 'join_lobby'

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

async def handle(context, websocket, msg_type, msg_data, tags):
    if msg_type == 'init' and msg_data == 'chat':
        assertion = await get_assertion_no_auth(context.challstr, context.username)
        await websocket.send(f'|/trn {context.username},0,{assertion}')
        context.update_state(lobby)
        context.in_lobby_event.set()
