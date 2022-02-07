from pokemon_showdown_rl.util.logging import get_logger
from pokemon_showdown_rl.showdown.battle import Battle

class StateContext:

    def __init__(self, username, opponent, challenger, team, battle_format):
        self.username = username
        self.opponent = opponent
        self.challenger = challenger
        self.team = team
        self.battle_format = battle_format
        self.state = None
        self.challstr = None
        self.room_id = None
        self.team_state = None
        self.action = None
        self.actions = None
        self.battle = Battle()
        
    def update_state(self, next_state):
        logger = get_logger(self.username)
        logger.write(f'[update state] {self.username}: {next_state.__name__}\n')
        self.state = next_state

    @property
    def full_name(self):
        return f'{self.username}{self.username_postfix}'
