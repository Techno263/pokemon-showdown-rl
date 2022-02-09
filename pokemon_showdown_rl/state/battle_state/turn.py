import json
from pokemon_showdown_rl.showdown.parse_msg import parse_player
from pokemon_showdown_rl.state.battle_state import action

name = 'turn'

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'request' and len(msg_data) > 0:
        context.request = json.dumps(msg_data)
    elif msg_type == 'player':
        player, username, _, _ = parse_player(msg_data)
        if username == context.username:
            context.player = player
    elif msg_type == 'turn':
        await websocket.send(f'{room_id}|/choose default')
