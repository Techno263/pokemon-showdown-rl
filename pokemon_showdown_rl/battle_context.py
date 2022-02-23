import json

from pokemon_showdown_rl.showdown.parse_msg import parse_player
from pokemon_showdown_rl.showdown.battle import Battle

class BattleContext:
    def __init__(self, username, logger):
        self.username = username
        self.request = None
        self.player_id = None
        self.battle = Battle()
        self.request_init = False

    def apply_request(self, msg_data):
        if len(msg_data) == 0:
            return
        self.request = json.dumps(msg_data)
        if not self.request_init:
            self.request_init = True
            player = self.battle.players[self.player_id]
            player.process_request

    def apply_player(self, msg_data):
        player_id, username, avatar, rating = parse_player(msg_data)
        if username == self.username:
            self.player_id = player_id
        self.battle.add_player(player, username, avatar, rating)
