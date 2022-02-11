from pokemon_showdown_rl.showdown.parse_util import (
    parse_user, parse_pokemon, parse_hp_status, parse_details
)

def parse_pm(msg_data):
    sender, receiver, msg = msg_data.split('|', 2)
    sender_rank, sender_name = parse_user(sender)
    reciever_rank, receiver_name = parse_user(receiver)
    return sender_rank, sender_name, reciever_rank, receiver_name, msg

def parse_player(msg_data):
    player, username, avatar, rating = msg_data.split('|', 3)
    return player, username, avatar, rating

def parse_teamsize(msg_data):
    player, teamsize = msg_data.split('|', 1)
    return player, teamsize

def parse_rule(msg_data):
    rule, description = msg_data.split(': ', 1)
    return rule, description

def parse_move(msg_data):
    pokemon, move, target = msg_data.split('|', 2)
    split_index = target.find('|')
    if split_index >= 0:
        tags = target[split_index+1:]
        target = target[:split_index]
    else:
        tags = ''
    player, position, name = parse_pokemon(pokemon)
    target_player, target_position, target_name = parse_pokemon(target)
    return (
        player, position, name, move, target_player, target_position,
        target_name, tags
    )

def parse_switch(msg_data):
    pokemon, details, hp_status = msg_data.split('|', 2)
    player, position, name = parse_pokemon(pokemon)
    species, shiny, gender, level = parse_details(details)
    current_hp, max_hp, status = parse_hp_status(hp_status)
    return (
        player, position, name, species, shiny, gender, level, current_hp,
        max_hp, status
    )

def parse_drag(msg_data):
    return parse_switch(msg_data)

def parse_detailschange(msg_data):
    return parse_switch(msg_data)

def parse_replace(msg_data):
    return parse_switch(msg_data)

def parse_swap(msg_data):
    pokemon, swap_position = msg_data.split('|', 1)
    player, position, name = parse_pokemon(pokemon)
    swap_position = int(swap_position)
    return player, position, name, swap_position

def parse_faint(msg_data):
    player, position, name = parse_pokemon(msg_data)
    return player, position, name

def parse_formechange(msg_data):
    pokemon, species, hp_status = msg_data.split('|', 2)
    player, position, name = parse_pokemon(pokemon)
    current_hp, max_hp, status = parse_hp_status(hp_status)
    return player, position, name, species, current_hp, max_hp, status

def parse_damage(msg_data):
    pokemon, hp_status = msg_data.split('|', 1)
    player, position, name = parse_pokemon(pokemon)
    current_hp, max_hp, status = parse_hp_status(hp_status)
    return player, position, name, current_hp, max_hp, status

def parse_heal(msg_data):
    return parse_damage(msg_data)

def parse_sethp(msg_data):
    pokemon, hp = msg_data.split('|', 1)
    player, position, name = parse_pokemon(pokemon)
    hp = int(hp)
    return player, position, name, hp

def parse_status(msg_data):
    pokemon, status = msg_data.split('|', 1)
    player, position, name = parse_pokemon(pokemon)
    return player, position, name, status

def parse_curestatus(msg_data):
    pokemon, status = msg_data.split('|', 1)
    player, position, name = parse_pokemon(pokemon)
    return player, position, name, status

def parse_cureteam(msg_data):
    player, position, name = parse_pokemon(msg_data)
    return player, position, name

def parse_boost(msg_data):
    pokemon, stat, amount = msg_data.split('|', 2)
    player, position, name = parse_pokemon(pokemon)
    amount = int(amount)
    return player, position, name, stat, amount

def parse_unboost(msg_data):
    return parse_boost(msg_data)

def parse_setboost(msg_data):
    return parse_boost(msg_data)

def parse_swapboost(msg_data):
    source, target_stats = msg_data.split('|', 1)
    source_player, source_position, source_name = parse_pokemon(source)
    if target_stats.find('|') >= 0:
        target, stats = target_stats.split('|', 1)
        stats = stats.split(', ')
    else:
        target = target_stats
        stats = ['atk', 'def', 'spa', 'spd', 'spe', 'evasion', 'accuracy']
    target_player, target_position, target_name = parse_pokemon(target)
    return (
        source_player, source_position, source_name, target_player,
        target_position, target_name, stats
    )

def parse_invertboost(msg_data):
    player_id, position, name = parse_pokemon(msg_data)
    return player_id, position, name

def parse_clearboost(msg_data):
    player_id, position, name = parse_pokemon(msg_data)
    return player_id, position, name

def parse_clearpositiveboost(msg_data):
    target, pokemon, effect = msg_data.split('|')
