import asyncio
import pokemon_showdown_rl.showdown.pokemon_data_v2.get_pokemon_data as get_pokemon_data


def main():
    asyncio.run(get_pokemon_data.data_exists())


if __name__ == '__main__':
    main()
