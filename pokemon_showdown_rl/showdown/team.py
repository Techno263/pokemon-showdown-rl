from pokemon_showdown_rl.showdown.pokemon import Pokemon
from dataclasses import dataclass, field

@dataclass
class Team:
    team: list[Pokemon] = field(default_factory=list)

    '''
    def __init__(self, team=[]):
        self.team = team
    '''

    def get_pokemon(self, name, species, shiny, gender, level):
        for pokemon in self.team:
            if (
                pokemon.name == name and pokemon.species == species
                and pokemon.shiny == shiny and pokemon.gender == gender
                and pokemon.level == level
            ):
                return pokemon
        return None

    def add_pokemon(
        self, name, species, shiny, gender, level, current_hp, max_hp, status
    ):
        pokemon = Pokemon(
            name, species, shiny, gender, level, current_hp, max_hp, status
        )
        self.team.append(pokemon)
        return pokemon

    def cure_team(self):
        for p in self.team:
            if p.status != '':
                p.status = ''
