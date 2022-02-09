from pokemon_showdown_rl.state.battle_state import turn

name = 'action'

async def handle(context, websocket, room_id, msg_type, msg_data):
    context.update_state(turn)
