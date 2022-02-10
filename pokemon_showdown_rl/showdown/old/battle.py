import re
from dataclasses import dataclass
from pokemon_showdown_rl.showdown.gender import Gender
from pokemon_showdown_rl.showdown.parse_util import (
    parse_switch, parse_damage
)

level_regex = re.compile(r'L[1-9][0-9]?')

@dataclass
class Pokemon:
    pass

class BattleSide:
    def __init__(self):
        self.current = None
        self.team = {}

    def __str__(self):
        return (
            f'current: {self.current}, team: ['
            + ', '.join(str(p) for p in self.team.values())
            + ']'
        )

    @property
    def current_pokemon(self):
        return self.team[self.current]

class Battle:
    def __init__(self):
        self.p1 = BattleSide()
        self.p2 = BattleSide()

    def __str__(self):
        return f'p1: {{{self.p1}}}, p2:{{{self.p2}}}'

    def apply_switch(self, switch):
        (
            player, pos, name, species, shiny, gender, level, current_hp,
            max_hp, status
        ) = parse_switch(switch)
        if player == 'p1':
            battle_side = self.p1
        elif player == 'p2':
            battle_side = self.p2
        else:
            raise Exception(f'Invalid player: {player}')
        if species in battle_side.team:
            pokemon = battle_side[species]
            assert pokemon['name'] == name
            assert pokemon['species'] == species
            assert pokemon['shiny'] == shiny
            assert pokemon['gender'] == gender
            assert pokemon['level'] == level
            assert pokemon['current_hp'] == current_hp
            assert pokemon['max_hp'] == max_hp
            assert pokemon['status'] == status
        else:
            battle_side.team[species] = {
                'name': name,
                'species': species,
                'shiny': shiny,
                'gender': gender,
                'level': level,
                'current_hp': current_hp,
                'max_hp': max_hp,
                'status': status
            }
        battle_side.current = species

    def apply_drag(self, drag):
        self.apply_switch(drag)

    def apply_damage(self, damage):
        player, pos, name, current_hp, max_hp, status = parse_damage(damage)
        if player == 'p1':
            battle_side = self.p1
        elif player == 'p2':
            battle_side = self.p2
        else:
            raise Exception(f'Invalid player: {player}')
        pokemon = battle_side.current_pokemon
        assert pokemon.name == name
        assert pokemon.max_hp == max_hp or max_hp == 0
        pokemon.current_hp = current_hp
        pokemon.status = status
