from dataclasses import dataclass
from Enum import Flag

class MoveFlags(Flag):
    pass


class MoveTarget(str, Flag):
    

@dataclass
class Move():
