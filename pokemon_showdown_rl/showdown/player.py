from pokemon_showdown_rl.showdown.team import Team


class Player:
    def __init__(self, username, avatar, rating, team=[]):
        self.username = username
        self.avatar = avatar
        self.rating = rating
        self.teamsize = 0
        self.team = Team(team)
        self.active = {}

    def switch(
        self, position, name, species, shiny, gender, level, hp,
        max_hp, status
    ):
        pokemon = self.team.get_pokemon(name, species, shiny, gender, level)
        if pokemon == None:
            pokemon = self.team.add_pokemon(
                name, species, shiny, gender, level, hp, max_hp, status
            )
        assert pokemon.max_hp == max_hp, f'pokemon.max_hp = {pokemon.max_hp}, max_hp = {max_hp}'
        pokemon.hp = hp
        pokemon.status = status
        self.active[position] = pokemon

    def set_hp_status(self, position, hp, status):
        pokemon = self.active[position]
        pokemon.hp = hp
        pokemon.status = status

    def set_hp(self, position, hp):
        pokemon = self.active[position]
        pokemon.hp = hp

    def set_status(self, position, status):
        pokemon = self.active[position]
        pokemon.status = status
