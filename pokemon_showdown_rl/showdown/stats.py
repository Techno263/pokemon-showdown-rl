from dataclasses import dataclass

@dataclass
class Stats:
    attack: int = None
    defense: int = None
    special_attack: int = None
    special_defense: int = None
    speed: int = None

    def is_initialized(self):
        return (
            self.attack == None
            or self.defense == None
            or self.special_attack == None
            or self.special_defense == None
            or self.speed == None
        )
