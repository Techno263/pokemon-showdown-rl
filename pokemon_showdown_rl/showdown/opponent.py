

class Opponent:

    def __init__(self):
        self.pokemon = None
        self.team = []

    def switch(self, pokemon):
        for i, p in enumerate(self.team):
            if p.species == pokemon.species:
                self.team[i] = pokemon
