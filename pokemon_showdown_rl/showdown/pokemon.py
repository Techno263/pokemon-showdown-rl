from pokemon_showdown_rl.showdown.boost import Boost

class Pokemon:
    def __init__(self, name, species, shiny, gender, level, current_hp, max_hp, status):
        self.name = name
        self.species = species
        self.shiny = shiny
        self.gender = gender
        self.level = level
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.status = status
        self.boost = Boost()
