import json
import re
from pokemon_showdown_rl.state.state import turn, user
from pokemon_showdown_rl.showdown.pokemon import Pokemon
from pokemon_showdown_rl.showdown.move import Move
from pokemon_showdown_rl.util.logging import get_logger

async def handle(context, websocket, room_id, msg_type, msg_data):
    logger = get_logger(context.username)
    if msg_type == 'request' and len(msg_data) > 0:
        request = json.loads(msg_data)
        logger.write(f'[request] {sorted(request.keys())}\n')
        username = request['side']['name']
        player_id = request['side']['id']
        context.player_id = player_id
        context.team_state = [Pokemon.from_request(p) for p in request['side']['pokemon']]
        if 'active' in request:
            context.action = 'active'
            request_active = request['active'][0]
            context.moves = [Move.from_request(m) for m in request_active['moves']]
            trapped = (
                request_active['trapped']
                if 'trapped' in request_active
                else False
            )
        elif 'forceSwitch' in request:
            context.action = 'forceSwitch'
            force_switch = request['forceSwitch']
        elif 'wait' in request:
            context.action = 'wait'
            wait = request['wait']
        context.update_state(turn)
