from pokemon_showdown_rl.showdown.pokemon import Pokemon

class Player:
    def __init__(self, team=[]):
        self.team = team
        self.actives = {}

    def switch(
        self, position, name, species, shiny, gender, level, current_hp,
        max_hp, status
    ):
        self.actives[position] = Pokemon(
            name, species, shiny, gender, level, current_hp, max_hp, status
        )
