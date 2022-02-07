import json
from pokemon_showdown_rl.state.state import player2

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'request' and len(msg_data) > 0:
        context.request = json.loads(msg_data)
        context.update_state(player2)
