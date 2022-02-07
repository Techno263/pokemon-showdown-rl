import json
from pokemon_showdown_rl.state.state import join_battle
from pokemon_showdown_rl.util.logging import get_logger

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'updatechallenges':
        challenge = json.loads(msg_data)
        if (
            context.opponent in challenge['challengesFrom']
            and challenge['challengesFrom'][context.opponent] == context.battle_format
        ):
            logger = get_logger(context.username)
            logger.write(f'|/utm {context.team}\n')
            await websocket.send(f'|/utm {context.team}')
            logger.write(f'|/accept {context.opponent}\n')
            await websocket.send(f'|/accept {context.opponent}')
            context.update_state(join_battle)
