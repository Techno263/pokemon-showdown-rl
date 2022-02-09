from pokemon_showdown_rl.state.client_state import lobby
from pokemon_showdown_rl.showdown.messages.personal_message import PersonalMessage

async def handle(context, websocket, msg_type, msg_data):
    c = context.challenger_state
    await self.websocket_wrapper.send(f'|/utm {c.team}')
    await self.websocket_wrapper.send(f'|/challenge {c.opponent}, {c.battle_format}')
    if msg_type == 'pm':
        pm = PersonalMessage.from_msg(msg_data)

