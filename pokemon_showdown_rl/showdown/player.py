import pokemon_showdown_rl.showdown.parse_util as parse_util

from pokemon_showdown_rl.showdown.team import Team
from pokemon_showdown_rl.showdown.parse_util import (
    parse_pokemon_ident, parse_details, parse_hp_status
)
from dataclasses import dataclass, field

@dataclass
class Player:
    username: str
    avatar: str
    rating: str
    team: Team = field(default_factory=Team)
    teamsize: int = field(init=False, default=0)
    active: dict = field(init=False, default_factory=dict)

    def initialize_from_request(self, request):
        side = request['side']
        assert side['name'] == self.username
        assert len(side['pokemon']) == self.teamsize
        for p in side['pokemon']:
            _, name = parse_pokemon_ident(p['ident'])
            species, shiny, gender, level = parse_details(p['details'])
            current_hp, max_hp, status = parse_hp_status(p['condition'])
            pokemon = self.team.add_pokemon(
                name, species, shiny, gender, level, current_hp, max_hp, status
            )
            pokemon.add_move()

    def process_request(self, request):
        side = request['side']
        assert side['name'] == self.username
        assert len(side['pokemon']) == self.teamsize
        for i, p in enumerate(side['pokemon']):
            _, name = parse_pokemon_ident(p['ident'])
            species, shiny, gender, level = parse_details(p['details'])
            pokemon = self.team.get_pokemon(
                name, species, shiny, gender, level
            )
            current_hp, max_hp, status = parse_hp_status(p['condition'])
            assert pokemon.current_hp == current_hp
            assert pokemon.status == status
            if current_hp != 0:
                assert pokemon.max_hp == max_hp
            stats = p['stats']
            if not pokemon.stats.initialized:
                pokemon.stats.initialize(
                    stats['atk'], stats['def'], stats['spa'], stats['spd'],
                    stats['spe']
                )
            else:
                assert pokemon.stats.attack == stats['atk']
                assert pokemon.stats.defense == stats['def']
                assert pokemon.stats.special_attack == stats['spa']
                assert pokemon.stats.special_defense == stats['spd']
                assert pokemon.stats.speed == stats['spe']
            if len(pokemon.moves) == 0:
                pokemon.initialize_moves(p['moves'])
            if p['active']:
                r_moves = request['active'][i]['moves']
                if len(r_moves == 0):
                    pokemon.initialize_moves(r_moves)
                else:
                    for m in r_moves:
                        move = pokemon.get_move(m['id'])
                        assert move.name == m['move']
                        assert move.move_id == m['id']
                        assert move.pp == m['pp']
                        assert move.max_pp == m['maxpp']
                        assert move.target == m['target']
                        assert move.disabled == m['disabled']
            

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

    def cure_status(self, position, status):
        pokemon = self.active[position]
        assert pokemon.status == status
        pokemon.status = ''

    def cure_team(self):
        self.team.cure_team()

    def boost(self, position, stat, amount):
        pokemon = self.active[position]
        pokemon.boost.boost(stat, amount)

    def unboost(self, position, stat, amount):
        pokemon = self.active[position]
        pokemon.boost.unboost(stat, amount)

    def set_boost(self, position, stat, amount):
        pokemon = self.active[position]
        pokemon.boost.set_boost(stat, amount)

    def invert_boost(self, position):
        pokemon = self.active[position]
        pokemon.boost.invert()

    def clear_boost(self, position):
        pokemon = self.active[position]
        pokemon.boost.clear_boost()

    def clear_all_boost(self):
        for pokemon in self.active.values():
            pokemon.boost.clear()

    def clear_positive_boost(self, position):
        pokemon = self.active[position]
        pokemon.boost.clear_positive()

    def clear_negative_boost(self, position):
        pokemon = self.active[position]
        pokemon.boost.clear_negative()

    def start_effect(self, position, effect):
        pokemon = self.active[position]
        # TODO: apply effect to pokemon

    def end_effect(self, position, effect):
        pokemon = self.active[position]
        # TODO: end effect on pokemon

    def update_item(self, position, item):
        pokemon = self.active[position]
        pokemon.item = item

    def remove_item(self, position, item):
        pokemon = self.active[position]
        if pokemon.item == item:
            pokemon.item = ''
        else:
            raise Exception('Tried to remove item that pokemon does not have')

    def set_ability(self, position, ability):
        pokemon = self.active[position]
        pokemon.ability = ability

    def transform(self, position, species):
        pokemon = self.active[position]
        # TODO: Get pokemon stats/info from species name and assigne it to
        # transform
        pokemon.transform = None

    def mega_evolve(self, position, mega_stone):
        pokemon = self.active[position]
        # TODO: swap pokemon to mega evolved form
        # self.active[position] = mega_pokemon

    def primal_reversion(self, position):
        pokemon = self.active[position]
        # TODO: swap to primal form
        # self.active[position] = primal_pokemon

    def ultra_burst(self, position, species, item):
        pokemon = self.active[position]
        # TODO: swap pokemon to ultra burst form
