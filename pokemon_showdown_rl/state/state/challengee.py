import json
from pokemon_showdown_rl.state.state import join_battle
from pokemon_showdown_rl.util.logging import get_logger

# Challengee state
# Player waits for pm from challenger and accepts it
# After accepting, moves to join battle state

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'pm':
        sender, receiver, msg = msg_data.split('|', 2)
        if receiver[1:] == context.username and sender[1:] == context.opponent:
            logger = get_logger(context.username)
            logger.write(f'|/utm {context.team}\n')
            await websocket.send(f'|/utm {context.team}')
            await websocket.send(f'|/accept {context.opponent}')
            context.update_state(join_battle)
    '''
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
    '''