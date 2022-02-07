import aiohttp
from pokemon_showdown_rl.state.state import challengee, join_battle
import json
from pokemon_showdown_rl.util.logging import get_logger

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'updateuser':
        logger = get_logger(context.username)
        user, named, avatar, settings = msg_data.split('|')
        user_rank = user[0]
        user = user[1:]
        if user[-2:] == '@!':
            user_away = True
            user = user[:-2]
        else:
            user_away = False
        settings = json.loads(settings)
        if context.challenger:
            logger.write(f'|/utm {context.team}\n')
            await websocket.send(f'|/utm {context.team}')
            logger.write(f'|/challenge {context.opponent}, {context.battle_format}\n')
            await websocket.send(f'|/challenge {context.opponent}, {context.battle_format}')
            context.update_state(join_battle)
        else:
            context.update_state(challengee)
    elif msg_type == 'nametaken':
        raise Exception('Name taken')
