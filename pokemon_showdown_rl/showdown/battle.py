from pokemon_showdown_rl.showdown.player import Player
from pokemon_showdown_rl.showdown.rule import Rule
from pokemon_showdown_rl.showdown.parse_msg import (
    parse_teamsize, parse_rule, parse_move, parse_switch, parse_drag,
    parse_detailschange, parse_replace, parse_swap, parse_faint,
    parse_formechange, parse_damage, parse_heal, parse_sethp, parse_status,
    parse_curestatus, parse_cureteam, parse_boost, parse_unboost,
    parse_setboost, parse_swapboost, parse_invertboost, parse_clearboost
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

    def process_request(self, request):
        player_id = request['side']['id']
        player = self.players[player_id]
        player.process_request(request)

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
        if max_hp != 0:
            assert pokemon.max_hp == max_hp
        # End testing code
        if current_hp == 0:
            player.set_hp(position, current_hp)
        else:
            player.set_hp_status(position, current_hp, status)

    def apply_heal(self, msg_data):
        (
            player, position, name, current_hp, max_hp, status
        ) = parse_heal(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        if max_hp != 0:
            assert pokemon.max_hp == max_hp
        # End testing code
        if current_hp == 0:
            player.set_hp(position, current_hp)
        else:
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
        player, position, name, status = parse_curestatus(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.cure_status(position, status)

    def apply_cureteam(self, msg_data):
        player, position, name = parse_cureteam(msg_data)
        player = self.players[player]
        player.cure_team()

    def apply_boost(self, msg_data):
        player, position, name, stat, amount = parse_boost(msg_data)
        player = self.players[player]
        player.boost(position, stat, amount)

    def apply_unboost(self, msg_data):
        player, position, name, stat, amount = parse_unboost(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.unboost(position, stat, amount)

    def apply_setboost(self, msg_data):
        player, position, name, stat, amount = parse_setboost(msg_data)
        player = self.players[player]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.set_boost(position, stat, amount)

    def apply_swapboost(self, msg_data):
        (
            source_player_id, source_position, source_name, target_player_id,
            target_position, target_name, stats
        ) = parse_swapboost(msg_data)
        source_player = self.players[source_player_id]
        target_player = self.players[target_player_id]
        source_pokemon = source_player.active[source_position]
        target_pokemon = target_player.active[target_position]
        assert source_pokemon.name == source_name
        assert target_pokemon.name == target_name
        source_pokemon.boost.swap(target_pokemon.boost, stats)

    def apply_invertboost(self, msg_data):
        player_id, position, name = parse_invertboost(msg_data)
        player = self.players[player_id]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.invert_boost(position)

    def apply_clearboost(self, msg_data):
        player_id, position, name = parse_clearboost(msg_data)
        player = self.players[player_id]
        # Begin testing code
        pokemon = player.active[position]
        assert pokemon.name == name
        # End testing code
        player.clear_boost(position)

    def apply_clearallboost(self):
        for player in self.players:
            player.clear_all_boost()

    def apply_clearpositiveboost(self, msg_data):
        pass
