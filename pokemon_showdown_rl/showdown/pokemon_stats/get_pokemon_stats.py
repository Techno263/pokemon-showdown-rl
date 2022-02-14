import pandas as pd
import requests


from bs4 import BeautifulSoup


stat_urls = [
    {
        'gens': [1],
        'url': r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_I)'
    },
    {
        'gens': [2, 3, 4, 5],
        'url': r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_II-V)'
    },
    {
        'gens': [6],
        'url': r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VI)'
    },
    {
        'gens': [7],
        'url': r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VII)'
    },
    {
        'gens': [8],
        'url': r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VIII-present)'
    }
]


def pokemon_table_find(tag):
    return tag.name == 'th' and 'Pokémon' == tag.text.strip()


def parse_stats_table(url):
    # Make request
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Find table header with text 'Pokémon'breakpoint()
    poke_headers = soup.find_all(pokemon_table_find)
    assert len(poke_headers) == 1
    header = poke_headers[0]
    # Get table
    table = header.find_parent('table')
    table = str(table).strip()
    # Convert to pandas
    pokemon_stats_df = pd.read_html(table, flavor='bs4')[0]
    pokemon_stats_df.drop(
        ['Unnamed: 1', 'Total', 'Average'],
        axis=1,
        errors='ignore',
        inplace=True
    )
    pokemon_stats_df.rename(
        columns={
            '#': 'num',
            'Pokémon': 'name',
            'HP': 'hp',
            'Attack': 'atk',
            'Defense': 'def',
            'Special': 'spc',
            'Sp. Attack': 'spa',
            'Sp. Defense': 'spd',
            'Speed': 'spe'
        },
        inplace=True
    )
    return pokemon_stats_df


def get_stats():
    for url_data in stat_urls:
        url = url_data['url']
        gens = url_data['gens']
        df = parse_stats_table(url)
        min_gen = min(gens)
        max_gen = max(gens)
        if min_gen == max_gen:
            ouput_name = f'stats_gen_{min_gen}.json'
        else:
            ouput_name = f'stats_gen_{min_gen}-{max_gen}.json'
        json_stats = df.to_json(ouput_name, orient='index')


def main():
    get_stats()


if __name__ == '__main__':
    main()
