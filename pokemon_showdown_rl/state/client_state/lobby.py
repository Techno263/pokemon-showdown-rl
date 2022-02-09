import asyncio
from pokemon_showdown_rl.showdown.parse_msg import parse_pm

# Lobby state
# Client is in this state after successful login
# Client is ready to begin battles

name = 'lobby'

async def handle(context, websocket, msg_type, msg_data):
    if msg_type == 'pm':
        _, challenger, _, _, msg = parse_pm(msg_data)
        # check if pm is a challenge
        if msg.startswith('/challenge '):
            challenge_msg, _ = msg.split('|', 1)
            _, battle_format = challenge_msg.split(' ')
            if context.challenge_callback == None:
                # if no callback, reject challenge
                await websocket.send(f'|/reject {challenger}')
            elif asyncio.iscoroutinefunction(context.challenge_callback):
                await context.challenge_callback(
                    websocket, challenger, battle_format
                )
            else:
                context.challenge_callback(
                    websocket, challenger, battle_format
                )
