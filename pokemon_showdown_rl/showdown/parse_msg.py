from pokemon_showdown_rl.showdown.parse_util import parse_user, parse_pokemon

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
    player, position, name = parse_pokemon(pokemon)
    species, *details = details.split(', ') 
    shiny = False
    gender = ''
    level = 100
    for detail in details:
        if detail == 'shiny':
            shiny = True
        elif detail == 'M':
            gender = 'M'
        elif detail == 'F':
            gender = 'F'
        elif detail[0] == 'L':
            level = int(detail[1:])
    current_hp, max_hp = map(int, hp.split)
    return (
        player, position, name, species, shiny, gender, level,
        current_hp, max_hp, status
    )
