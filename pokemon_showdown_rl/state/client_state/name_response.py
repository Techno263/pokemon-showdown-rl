from pokemon_showdown_rl.state.client_state import lobby, name_taken
from pokemon_showdown_rl.showdown.parse_util import parse_user

name = 'name_response'

async def handle(context, websocket, msg_type, msg_data, tags):
    if msg_type == 'nametaken':
        context.update_state(name_taken)
    elif msg_type == 'updateuser':
        user, named, _, _ = msg_type.split('|', maxsplit=3)
        _, username = parse_user(user)
        if (username == context.username) and named == '1':
            context.update_state(lobby)
