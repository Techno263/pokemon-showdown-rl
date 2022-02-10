def parse_user(user):
    rank = user[0]
    username = user[1:]
    return rank, username

def parse_pokemon(pokemon):
    position, name = pokemon.split(': ', 1)
    player = position[:2]
    position = position[2]
    return player, position, name

def parse_details(details):
    species, *details = details.split(', ')
    shiny = False
    gender = ''
    level = 100
    for detail in details[1:]:
        if detail == 'shiny':
            shiny = True
        elif detail == 'M':
            gender = 'M'
        elif detail == 'F':
            gender = 'F'
        elif detail[0] == 'L':
            level = int(detail[1:])
    return species, shiny, gender, level

def parse_hp_status(hp_status):
    hp_status = hp_status.split(' ', 1)
    if len(hp_status) == 1:
        hp = hp_status[0]
        status = ''
    else:
        hp, status = hp_status
    if hp == '0':
        current_hp = 0
        max_hp = 0
    else:
        current_hp, max_hp = map(int, hp.split('/'))
    return current_hp, max_hp, status

'''
def parse_damage(damage):
    pokemon, hp_status = damage.split('|')
    player, pos, name = parse_pokemon(pokemon)
    current_hp, max_hp, status = parse_hp_status(hp_status)
    return player, pos, name, current_hp, max_hp, status
'''
