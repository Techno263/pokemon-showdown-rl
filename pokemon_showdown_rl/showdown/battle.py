from pokemon_showdown_rl.showdown.player import Player
from pokemon_showdown_rl.showdown.rule import Rule
from pokemon_showdown_rl.showdown.parse_msg import (
    parse_teamsize, parse_rule, parse_move, parse_switch, parse_drag,
    parse_detailschange, parse_replace, parse_swap, parse_faint,
    parse_formechange, parse_damage, parse_heal, parse_sethp, parse_status
)

class Battle:
    def __init__(self):
        self.title = ''
        self.gametype = ''
        self.gen = 0
        self.tier = ''
        self.rules = []
        self.players = {}

    def add_player(self, player, username, avatar, rating):
        self.players[player] = Player(username, avatar, rating)

    def apply_title(self, msg_data):
        self.title = msg_data

    def apply_gametype(self, msg_data):
        self.gametype == msg_data

    def apply_teamsize(self, msg_data):
        player, teamsize = parse_teamsize(msg_data)
        player = self.players[player]
        player.teamsize = teamsize

    def apply_gen(self, msg_data):
        self.gen = int(msg_data)

    def apply_tier(self, msg_data):
        self.tier = msg_data

    def apply_rule(self, msg_data):
        rule, description = parse_rule(msg_data)
        rule = Rule(rule, description)
        self.rules.append(rule)

    def apply_move(self, msg_data):
        (
            player, position, name, move, target_player, target_position,
            target_name, tags
        ) = parse_move(msg_data)
        player = self.players[player]
        # TODO: Update pokemon state with the knowledge of this move

    def apply_switch(self, msg_data):
        (
            player, position, name, species, shiny, gender, level,
            current_hp, max_hp, status
        ) = parse_switch(msg_data)
        player = self.players[player]
        player.switch(
            position, name, species, shiny, gender, level, current_hp, max_hp,
            status
        )

    def apply_drag(self, msg_data):
        (
            player, position, name, species, shiny, gender, level,
            current_hp, max_hp, status
        ) = parse_drag(msg_data)
        player = self.players[player]
        player.switch(
            position, name, species, shiny, gender, level, current_hp, max_hp,
            status
        )

    def apply_detailschange(self, msg_data):
        (
            player, position, name, species, shiny, gender, level, current_hp,
            max_hp, status
        ) = parse_detailschange(msg_data)
        # TODO: Update pokemon state with new details

    def apply_replace(self, msg_data):
        (
            player, position, name, species, shiny, gender, level, current_hp,
            max_hp, status
        ) = parse_replace(msg_data)
        # TODO: Update pokemon state with replacement

    def apply_swap(self, msg_data):
        player, position, name, swap_position = parse_swap(msg_data)

    def apply_faint(self, msg_data):
        player, position, name = parse_faint(msg_data)

    def apply_formechange(self, msg_data):
        (
            player, position, name, species, current_hp, max_hp, status
        ) = parse_formechange(msg_data)
        # TODO: Figure out correct behavior of formechange

    def apply_damage(self, msg_data):
        (
            player, position, name, current_hp, max_hp, status
        ) = parse_damage(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        assert pokemon.max_hp == max_hp
        # End testing code
        player.set_hp_status(position, current_hp, status)

    def apply_heal(self, msg_data):
        (
            player, position, name, current_hp, max_hp, status
        ) = parse_heal(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        assert pokemon.max_hp == max_hp
        # End testing code
        player.set_hp_status(position, current_hp, status)

    def apply_sethp(self, msg_data):
        player, position, name, hp = parse_sethp(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.set_hp(position, hp)

    def apply_status(self, msg_data):
        player, position, name, status = parse_status(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.set_status(position, status)

    def apply_curestatus(self, msg_data):
