from pokemon_showdown_rl.showdown.player import Player
from pokemon_showdown_rl.showdown.parse_msg import parse_switch

class Battle:
    def __init__(self):
        self.players = {}

    def get_player(self, player):
        if player in self.players:
            return self.players[player]
        else:
            p = Player()
            self.players[player] = p
            return p

    def apply_switch(self, msg_data):
        (
            player, position, name, species, shiny, gender, level,
            current_hp, max_hp, status
        ) = parse_switch(msg_data)
        player = self.get_player(player)
        player.switch(
            position, name, species, shiny, gender, level, current_hp, max_hp, status
        )
