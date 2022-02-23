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
    boost: Boost = field(init=False, default_factory=Boost)
    stats: Stats = field(init=False, default_factory=Stats)
    moves: list[Move] = field(init=False, default_factory=list)
    item: str = field(init=False, default_factory=str)
    ability: str = field(init=False, default=None)
    transform: Pokemon = field(init=False, default=None)


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

    def add_move(self, name)

    def get_move(self, move_id):
        for m in self.moves:
            if m.move_id == move_id:
                return m
        return None
