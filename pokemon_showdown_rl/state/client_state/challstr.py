from pokemon_showdown_rl.state.client_state import join_lobby

# Challstr state
# Inital state for client
# waits for challstr and initiates autojoin

name = 'challstr'

async def handle(context, websocket, msg_type, msg_data):
    if msg_type == 'challstr':
        context.challstr = msg_data
        await websocket.send('|/autojoin')
        context.update_state(join_lobby)
