import os.path as path


dirname = path.dirname(__file__)
data_dir = path.join(dirname, 'data')

pokedex_filename = 'pokedex.json'
team_builder_filename = 'team_builder.json'
learnset_filename = 'learnset.json'
moves_filename = 'moves.json'
abilities_filename = 'abilities.json'
items_filename = 'items.json'
formats_data_filename = 'formats_data.json'
formats_filename = 'formats.json'
typechart_filename = 'typechart.json'

pokedex_path = path.join(data_dir, pokedex_filename)
team_builder_path = path.join(data_dir, team_builder_filename)
learnset_path = path.join(data_dir, learnset_filename)
moves_path = path.join(data_dir, moves_filename)
abilities_path = path.join(data_dir, abilities_filename)
items_path = path.join(data_dir, items_filename)
formats_data_path = path.join(data_dir, formats_data_filename)
formats_path = path.join(data_dir, formats_filename)
typechart_path = path.join(data_dir, typechart_filename)
