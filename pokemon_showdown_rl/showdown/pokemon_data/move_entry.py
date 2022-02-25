from dataclasses import dataclass
from enum import Enum
from pokemon_showdown_rl.showdown.pokemon_data.pokemon_type import PokemonType

class MoveCategory(str, Enum):
    PHYSICAL = 'Physical'
    SPECIAL = 'Special'
    STATUS = 'Non-Damaging'
    NON_DAMAGING = STATUS


@dataclass
class MoveEntry:
    name: str
    category: MoveCategory
    power: int
    accuracy: int
    priority: int
    pp: int
    move_type: PokemonType
    pokemon: list[str]

    @staticmethod
    def from_json(json_data):
        return MoveEntry(
            json_data['name'], MoveCategory(json_data['category']),
            json_data['power'], json_data['accuracy'], json_data['priority'],
            json_data['pp'], PokemonType(json_data['type']), json_data['pokemon']
        )
