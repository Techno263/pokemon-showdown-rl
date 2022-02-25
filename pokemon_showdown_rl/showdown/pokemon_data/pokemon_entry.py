from dataclasses import dataclass

@dataclass
class PokemonEntry:
    name: str
    num: int
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    weight: float
    height: float
    types: list[str]
    abilities: list[str]
    learnset: list[str]
    evos: list[str]
    alts: list[str]

    @staticmethod
    def from_json(json_data):
        return PokemonEntry(
            json_data['name'], json_data['dex_num'], json_data['hp'],
            json_data['atk'], json_data['def'], json_data['spa'],
            json_data['spd'], json_data['spe'], json_data['weight'],
            json_data['height'], json_data['types'], json_data['abilities'],
            json_data['learnset'], json_data['evos'], json_data['alts']
        )
