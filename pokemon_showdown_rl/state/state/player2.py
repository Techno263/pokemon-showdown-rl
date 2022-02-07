from pokemon_showdown_rl.state.state import turn

async def handle(context, websocket, room_id, msg_type, msg_data):
    if msg_type == 'player':
        player, username, avatar, rating = msg_data.split('|')
        avatar = int(avatar)
        rating = int(rating) if len(rating) > 0 else None
        assert player == 'p2'
        if username == context.username:
            context.player = player
        context.update_state(turn)
