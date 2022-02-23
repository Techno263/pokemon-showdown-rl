from dataclasses import dataclass

@dataclass
class Move:
    name: str
    move_id: str
    pp: int
    max_pp: int
    target: str
    disabled: bool
