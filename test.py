import asyncio
from pokemon_showdown_rl.client import Client
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

def main():
    asyncio.run(run_battle())

if __name__ == '__main__':
    main()
