import websockets
from pokemon_showdown_rl.state.state import start
from pokemon_showdown_rl.state.state_context import StateContext
from pokemon_showdown_rl.util.logging import get_logger

class Client:
    def __init__(self, username, opponent, challenger, team, battle_format):
        self.context = StateContext(
            username, opponent, challenger, team, battle_format
        )

    async def parse_websocket_message(self, message):
        messages = message.split('\n')
        if messages[0][0] == '>':
            room_id = messages[0][1:]
            messages = messages[1:]
        else:
            room_id = None
        logger = get_logger(self.context.username)
        for msg in messages:
            logger.write(f'[{room_id}] ({len(msg):03d}): {msg}\n')
            if len(msg) == 0:
                continue
            if msg[0] == '|':
                msg = msg[1:]
                try:
                    index = msg.index('|')
                    msg_type = msg[:index]
                    msg_data = msg[index + 1:]
                except:
                    msg_type = msg
                    msg_data = ''
                await self.context.state.handle(
                    self.context, self.websocket, room_id, msg_type, msg_data
                )

    async def run(self, url):
        self.websocket = await websockets.connect(url)
        self.context.update_state(start)
        async for message in self.websocket:
            await self.parse_websocket_message(message)
