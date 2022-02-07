import re
from enum import IntEnum

level_regex = re.compile(r'L[1-9][0-9]?')

class Gender(IntEnum):
    Unknown = 0
    Male = 1
    Female = 2

class Pokemon:
    def __init__(
        self,
        identifier,
        name,
        species,
        shiny,
        gender,
        level,
        current_hp,
        max_hp,
        status,
        active,
        attack,
        defense,
        special_attack,
        special_defense,
        speed,
        moves,
        base_ability,
        item,
        pokeball,
        ability
    ):
        self.identifier = identifier
        self.name = name
        self.species = species
        self.shiny = shiny
        self.gender = gender
        self.level = level
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.status = status
        self.active = active
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.moves = moves
        self.base_ability = base_ability
        self.item = item
        self.pokeball = pokeball
        self.ability = ability

    @property
    def hp_percentage(self):
        if self.current_hp == 0:
            return 0
        return self.current_hp / self.max_hp

    @staticmethod
    def from_request(request_pokemon):
        identifier = request_pokemon['ident']
        _, name = identifier.split(':')
        name = name.strip()
        details = [s.strip() for s in request_pokemon['details'].split(',')]
        species = details[0]
        shiny = False
        gender = Gender.Unknown
        level = 100
        for detail in details[1:]:
            if detail == 'shiny':
                shiny = True
            elif detail == 'M':
                gender = Gender.Male
            elif detail == 'F':
                gender = Gender.Female
            elif level_regex.match(detail) != None:
                level = int(detail[1:])
        if request_pokemon['condition'] == '0 fnt':
            pass
        hp_status = request_pokemon['condition'].split(' ', 1)
        if len(hp_status) == 1:
            hp = hp_status[0]
            status = ''
        else:
            hp, status = hp_status
        if hp == '0':
            current_hp = 0
            max_hp = 0
        else:
            current_hp, max_hp = map(int, hp.split('/'))
        active = request_pokemon['active']
        pokemon_stats = request_pokemon['stats']
        attack = pokemon_stats['atk']
        defense = pokemon_stats['def']
        special_attack = pokemon_stats['spa']
        special_defense = pokemon_stats['spd']
        speed = pokemon_stats['spe']
        moves = request_pokemon['moves']
        base_ability = request_pokemon['baseAbility']
        item = request_pokemon['item']
        pokeball = request_pokemon['pokeball']
        ability = request_pokemon['ability'] if 'ability' in request_pokemon else None
        return Pokemon(
            identifier, name, species, shiny, gender, level, current_hp,
            max_hp, status, active, attack, defense, special_attack,
            special_defense, speed, moves, base_ability, item, pokeball,
            ability
        )

    @staticmethod
    def from_switch(switch):
        identifier, details, hp = switch.split('|')
        pos, name = identifier.split(':')
        name = name.strip()
        details = [s.strip() for s in details.split(',')]
        species = details[0]
        shiny = False
        gender = Gender.Unknown
        level = 100
        for detail in details[1:]:
            if detail == 'shiny':
                shiny = True
            elif detail == 'M':
                gender = Gender.Male
            elif detail == 'F':
                gender = Gender.Female
            elif level_regex.match(detail) != None:
                level = int(detail[1:])
        current_hp, max_hp = map(int, hp.split('/'))
        return Pokemon(
            identifier, name, species, shiny, gender, level, current_hp,
            max_hp, None, None, None, None, None, None, None, None, None,
            None, None, None
        )
