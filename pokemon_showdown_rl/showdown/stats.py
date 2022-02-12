from dataclasses import dataclass

@dataclass
class Stats:
    attack: int = 0
    defense: int = 0
    special_attack: int = 0
    special_defense: int = 0
    speed: int = 0
    initialized: bool = False

    def initialize(
        self, attack, defense, special_attack, special_defense, speed
    ):
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.initialized = True
