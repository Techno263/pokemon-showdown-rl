from pokemon_showdown_rl.state.state import request
from pokemon_showdown_rl.util.logging import get_logger
from pokemon_showdown_rl.showdown.pokemon import Pokemon

# Turn state
# The player makes their turn
# Moves to request state

async def handle(context, websocket, room_id, msg_type, msg_data):
    logger = get_logger(context.username)
    if msg_type == 'turn':
        #logger.write(f'{context.room_id}|/choose default\n')
        #await websocket.send(f'{context.room_id}|/choose default')
        logger.write(f'{context.room_id}|/choose\n')
        await websocket.send(f'{context.room_id}|/choose')
        context.update_state(request)
    elif msg_type == 'move':
        # TODO: Update state based on move
        pass
    elif msg_type == 'switch':
        context.battle.apply_switch(msg_data)
    elif msg_type == 'drag':
        context.battle.apply_drag(msg_data)
    elif msg_type == 'detailscahnge':
        pass
    elif msg_type == 'replace':
        pass
    elif msg_type == 'swap':
        pass
    elif msg_type == 'cant':
        pass
    elif msg_type == 'faint':
        logger.write(f'{context.room_id}|/choose default\n')
        await websocket.send(f'{context.room_id}|/choose default')
    elif msg_type == 'error':
        pass
    elif msg_type == '-formechange':
        pass
    elif msg_type == '-block':
        pass
    elif msg_type == '-notarget':
        pass
    elif msg_type == '-miss':
        pass
    elif msg_type == '-damage':
        #context.battle.apply_damage(msg_data)
        pass
    elif msg_type == '-heal':
        pass
    elif msg_type == '-sethp':
        pass
    elif msg_type == '-status':
        pass
    elif msg_type == '-curestatus':
        pass
    elif msg_type == '-cureteam':
        pass
    elif msg_type == '-boost':
        pass
    elif msg_type == '-unboost':
        pass
    elif msg_type == '-setboost':
        pass
    elif msg_type == '-swapboost':
        pass
    elif msg_type == '-invertboost':
        pass
    elif msg_type == '-clearboost':
        pass
    elif msg_type == '-clearallboost':
        pass
    elif msg_type == '-clearpositiveboost':
        pass
    elif msg_type == '-clearnegativeboost':
        pass
    elif msg_type == '-copyboost':
        pass
    elif msg_type == '-weather':
        pass
    elif msg_type == '-fieldstart':
        pass
    elif msg_type == '-fieldend':
        pass
    elif msg_type == '-sidestart':
        pass
    elif msg_type == '-sideend':
        pass
    elif msg_type == '-start':
        pass
    elif msg_type == '-end':
        pass
    elif msg_type == '-crit':
        pass
    elif msg_type == '-supereffective':
        pass
    elif msg_type == '-resisted':
        pass
    elif msg_type == '-immune':
        pass
    elif msg_type == '-item':
        pass
    elif msg_type == '-enditem':
        pass
    elif msg_type == '-ability':
        pass
    elif msg_type == '-endability':
        pass
    elif msg_type == '-transform':
        pass
    elif msg_type == '-mega':
        pass
    elif msg_type == '-primal':
        pass
    elif msg_type == '-burst':
        pass
    elif msg_type == '-zpower':
        pass
    elif msg_type == '-zbroken':
        pass
    elif msg_type == '-activate':
        pass
    elif msg_type == '-hint':
        pass
    elif msg_type == '-center':
        pass
    elif msg_type == '-message':
        pass
    elif msg_type == '-combine':
        pass
    elif msg_type == '-waiting':
        pass
    elif msg_type == '-prepare':
        pass
    elif msg_type == '-mustrecharge':
        pass
    elif msg_type == '-hitcount':
        pass
    elif msg_type == '-singlemove':
        pass
    elif msg_type == '-singleturn':
        pass
    logger.write(f'[battle state] {context.battle}\n')
