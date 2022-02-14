from dataclasses import dataclass
from pokemon_showdown_rl.showdown.stats import Stats

@dataclass
class StatsEntry:
    num: int
    name: str
    stats: Stats
