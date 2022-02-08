from pokemon_showdown_rl.util.logging import get_logger

# Stop state
# Closes the connection which then causes the client message loop to exit

async def handle(context, websocket, room_id, msg_type, msg_data):
    logger = get_logger(context.username)
    logger.write('Closing websocket\n')
    websocket.close()
