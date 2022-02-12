import json

from pokemon_showdown_rl.showdown.parse_msg import parse_player
from pokemon_showdown_rl.showdown.battle import Battle

class BattleContext:
    def __init__(self, username, logger):
        self.username = username
        self.request = None
        self.player = None
        self.battle = Battle()

    def apply_request(self, msg_data):
        if len(msg_data) > 0:
            self.request = json.dumps(msg_data)

    def apply_player(self, msg_data):
        player, username, avatar, rating = parse_player(msg_data)
        if username == self.username:
            self.player = player
        self.battle.add_player(player, username, avatar, rating)
