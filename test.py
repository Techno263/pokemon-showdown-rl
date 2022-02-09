import asyncio
from pokemon_showdown_rl.client_v2 import Client
import random
import string

def get_random_username(length):
    valid_chars = (
        string.ascii_lowercase + string.digits
    )
    name_list = [
        valid_chars[random.randrange(len(valid_chars))]
        for _ in range(length)
    ]
    return ''.join(name_list)

async def run_battle():
    bot_name = get_random_username(16)
    client1_name = bot_name + '_1'
    client2_name = bot_name + '_2'
    client1 = Client(client1_name, client2_name, True, 'null', 'gen1randombattle')
    client2 = Client(client2_name, client1_name, False, 'null', 'gen1randombattle')
    url = r'ws://localhost:8000/showdown/websocket'
    await asyncio.gather(
        client1.run(url),
        client2.run(url)
    )

def challenge_callback(team, opponent, battle_format):
    _battle_format = battle_format
    async def callback(websocket, challenger, battle_format):
        if opponent == challenger and _battle_format == battle_format:
            await websocket.send(f'|/utm {team}')
            await websocket.send(f'|/accept {opponent}')
        else:
            await websocket.send(f'|/reject {opponent}')
    return callback

async def run_battle2():
    bot_name = get_random_username(16)
    client1_name = bot_name + '_1'
    client2_name = bot_name + '_2'
    battle_format = 'gen1randombattle'
    url = r'ws://localhost:8000/showdown/websocket'

    client1 = Client(client1_name)
    client2 = Client(client2_name, challenge_callback('null', client1_name, battle_format))

    async def lobby_handler():
        await asyncio.gather(
            client1.wait_for_lobby(), client2.wait_for_lobby()
        )
        await client1.challenge('null', client2_name, battle_format)
    await asyncio.gather(
        asyncio.gather(client1.run(url), client2.run(url)),
        lobby_handler()
    )

def main():
    asyncio.run(run_battle2())

if __name__ == '__main__':
    main()
