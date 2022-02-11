class Boost:
    def __init__(self):
        self.attack = 0
        self.defense = 0
        self.special_attack = 0
        self.special_defense = 0
        self.speed = 0
        self.evasion = 0
        self.accuracy = 0

    def boost(self, stat, amount):
        if stat == 'atk':
            self.attack = min(self.attack + amount, 6)
        elif stat == 'def':
            self.defense = min(self.defense + amount, 6)
        elif stat == 'spa':
            self.special_attack = min(self.special_attack + amount, 6)
        elif stat == 'spd':
            self.special_defense = min(self.special_defense + amount, 6)
        elif stat == 'spe':
            self.speed = min(self.speed + amount, 6)
        elif stat == 'evasion':
            self.evasion = min(self.evasion + amount, 6)
        elif stat == 'accuracy':
            self.accuracy = min(self.accuracy + amount, 6)

    def unboost(self, stat, amount):
        if stat == 'atk':
            self.attack = max(self.attack + amount, -6)
        elif stat == 'def':
            self.defense = max(self.defense + amount, -6)
        elif stat == 'spa':
            self.special_attack = max(self.special_attack + amount, -6)
        elif stat == 'spd':
            self.special_defense = max(self.special_defense + amount, -6)
        elif stat == 'spe':
            self.speed = max(self.speed + amount, -6)
        elif stat == 'evasion':
            self.evasion = max(self.evasion + amount, -6)
        elif stat == 'accuracy':
            self.accuracy = max(self.accuracy + amount, -6)

    def set_boost(self, stat, amount):
        if stat == 'atk':
            self.attack = amount
        elif stat == 'def':
            self.defense = amount
        elif stat == 'spa':
            self.special_attack = amount
        elif stat == 'spd':
            self.special_defense = amount
        elif stat == 'spe':
            self.speed = amount
        elif stat == 'evasion':
            self.evasion = amount
        elif stat == 'accuracy':
            self.accuracy = amount

    def swap(self, boost, stats):
        for stat in stats:
            if stat == 'atk':
                self.attack, boost.attack = boost.attack, self.attack
            elif stat == 'def':
                self.defense, boost.defense = boost.defense, self.defense
            elif stat == 'spa':
                self.special_attack, boost.special_attack = boost.special_attack, self.special_attack
            elif stat == 'spd':
                self.special_defense, boost.special_defense = boost.special_defense, self.special_defense
            elif stat == 'spe':
                self.speed, boost.speed = boost.speed, self.speed
            elif stat == 'evasion':
                self.evasion, boost.evasion = boost.evasion, self.evasion
            elif stat == 'accuracy':
                self.accuracy, boost.accuracy = boost.accuracy, self.accuracy

    def invert(self):
        self.attack = -self.attack
        self.defense = -self.defense
        self.special_attack = -self.special_attack
        self.special_defense = -self.special_defense
        self.speed = -self.speed
        self.evasion = -self.evasion
        self.accuracy = -self.accuracy
