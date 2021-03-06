from pokemon_showdown_rl.state.state import request

# Join battle state
# Waits to receive a join message where the player is the battler
# Moves to request state

async def handle(context, websocket, room_id, msg_type, msg_data):
    if (
        (msg_type == 'j' or msg_type == 'join' or msg_type == 'J')
        and msg_data[1:] == context.username
        and msg_data[0] == '☆'
    ):
        context.room_id = room_id
        context.update_state(request)
