from pokemon_showdown_rl.state.state import request
from pokemon_showdown_rl.util.logging import get_logger
from pokemon_showdown_rl.showdown.pokemon import Pokemon

async def handle(context, websocket, room_id, msg_type, msg_data):
    logger = get_logger(context.username)
    if msg_type == 'turn':
        logger.write(f'{context.room_id}|/choose default\n')
        await websocket.send(f'{context.room_id}|/choose default')
        context.update_state(request)
    elif msg_type == 'faint':
        logger.write(f'{context.room_id}|/choose default\n')
        await websocket.send(f'{context.room_id}|/choose default')
    elif msg_type == 'switch':
        context.battle.apply_switch(msg_data)
    elif msg_type == 'drag':
        context.battle.apply_drag(msg_data)
    elif msg_type == 'move':
        # TODO: Update state based on move
        pass
    elif msg_type == 'damage':
        context.battle.apply_damage(msg_data)
    logger.write(f'[battle state] {context.battle}\n')
