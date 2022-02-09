from pokemon_showdown_rl.showdown.parse_util import parse_user

def parse_pm(msg_data):
    sender, receiver, msg = msg_data.split('|', 2)
    sender_rank, sender_name = parse_user(sender)
    reciever_rank, receiver_name = parse_user(receiver)
    return sender_rank, sender_name, reciever_rank, receiver_name, msg

def parse_player(msg_data):
    player, username, avatar, rating = msg_data.split('|', 3)
    return player, username, avatar, rating

def parse_move(msg_data):
    pokemon, move, target = msg_data.split('|', 2)

def parse_switch(msg_data):
    pokemon, details, hp_status = msg_data.split('|', 2)
    hp, status = hp_status.split(' ', 1)
    pokemon_position, pokemon_name = pokemon.split(': ', 1)
    
