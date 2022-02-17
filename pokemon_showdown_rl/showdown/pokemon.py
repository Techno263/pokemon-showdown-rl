from pokemon_showdown_rl.showdown.boost import Boost
from pokemon_showdown_rl.showdown.move import Move
from pokemon_showdown_rl.showdown.stats import Stats
from dataclasses import dataclass, field

@dataclass
class Pokemon:
    name: str
    species: str
    shiny: bool
    gender: str
    level: int
    current_hp: int
    max_hp: int
    status: str
    boost: Boost = field(init=False, default=Boost())
    stats: Stats = field(init=False, default=Stats())
    moves: list[Move] = field(init=False, default_factory=list)
    item: str = None

    '''
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
    '''

    def initialize_moves(self, moves):
        if len(moves) == 0:
            moves = [
                Move(
                    m['move'], m['id'], m['pp'], m['maxpp'], m['target'],
                    m['disabled']
                )
                for m in moves
            ]
        else:
            raise Exception('Moves already initialized')

    def get_move(self, move_id):
        for m in self.moves:
            if m.move_id == move_id:
                return m
        return None
