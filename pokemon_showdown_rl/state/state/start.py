from pokemon_showdown_rl.state.state import init_lobby
from pokemon_showdown_rl.util.logging import get_logger

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'challstr':
        logger = get_logger(context.username)
        context.challstr = msg_data
        logger.write('|/autojoin\n')
        await websocket.send('|/autojoin')
        context.update_state(init_lobby)
