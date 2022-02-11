import websockets
import logging
from pokemon_showdown_rl.websocket_wrapper import WebsocketWrapper
from pokemon_showdown_rl.room import Room
from pokemon_showdown_rl.client_context import ClientContext
from pokemon_showdown_rl.state.client_state import challstr

def _setup_client_logging(username):
    logger = logging.getLogger(f'{username}.client')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f'logs/{username}.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s | %(message)s'
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

class Client:
    def __init__(self, username, challenge_callback=None):
        self.username = username
        self.rooms = {}
        self.websocket = None
        self.websocket_wrapper = None
        self.logger = _setup_client_logging(self.username)
        self.context = ClientContext(
            self.username, challstr, self.logger, challenge_callback
        )

    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        else:
            room = Room(room_id, self.username, self.logger)
            self.rooms[room_id] = room
            return room

    async def parse_websocket_message(self, message):
        messages = message.split('\n')
        if messages[0][0] == '>':
            room_id = messages[0][1:]
            messages = messages[1:]
        else:
            room_id = None
        for msg in messages:
            #self.logger.info(f'recv | {room_id} - {msg}')
            if len(msg) == 0:
                continue
            if msg[0] == '|':
                msg = msg[1:]
                index = msg.find('|')
                if index >= 0:
                    msg_type = msg[:index]
                    msg_data = msg[index + 1:]
                else:
                    msg_type = msg
                    msg_data = ''
                msg_data, *tags_msgs = msg_data.split('|[')
                tags = {}
                for tag_msg in tags_msgs:
                    tag_type, tag_data = tag_msg.split(']')
                    tag_data = tag_data.lstrip()
                    tags[tag_type] = tag_data
                if room_id == None:
                    # message from lobby or global
                    self.logger.info(f'RECV | lobby | {msg_type} | {msg_data}')
                    await self.handle_msg(msg_type, msg_data, tags)
                else:
                    # message from non-lobby and non-global room
                    self.logger.info(f'RECV | {room_id} | {msg_type} | {msg_data}')
                    room = self.get_room(room_id)
                    await room.handle_msg(self.websocket_wrapper, msg_type, msg_data, tags)

    async def handle_msg(self, msg_type, msg_data, tags):
        await self.context.state.handle(
            self.context, self.websocket_wrapper, msg_type, msg_data, tags
        )

    async def run(self, url):
        self.websocket = await websockets.connect(url)
        self.websocket_wrapper = WebsocketWrapper(self.websocket, self.logger)
        async for message in self.websocket:
            try:
                await self.parse_websocket_message(message)
            except websockets.ConnectionClosed:
                break
        self.websocket = None

    async def wait_for_lobby(self):
        await self.context.in_lobby_event.wait()

    async def challenge(self, team, opponent, battle_format):
        await self.websocket_wrapper.send(f'|/utm {team}')
        await self.websocket_wrapper.send(f'|/challenge {opponent}, {battle_format}')

    async def accept_challenge(self, team, opponent, battle_format):
        while True:
            challenge = self.context.get()
            if (
                challenge.challenger == opponent
                and challenge.battle_format == battle_format
            ):
                await self.websocket_wrapper.send(f'|/utm {team}')
                await self.websocket_wrapper.send(f'|/accept {opponent}')
                return
