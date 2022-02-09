import asyncio

class ClientContext:
    def __init__(self, username, state, logger, challenge_callback=None):
        self.username = username
        self.state = None
        self.logger = logger
        self.challenge_callback = challenge_callback
        self.challstr = None
        self.in_lobby_event = asyncio.Event()
        self.update_state(state)

    def update_state(self, next_state):
        self.logger.info(f'CUPT | {next_state.name}')
        self.state = next_state
