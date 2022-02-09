class WebsocketWrapper:
    def __init__(self, websocket, logger):
        self.websocket = websocket
        self.logger = logger

    async def send(self, message):
        self.logger.info(f'SEND | {message}')
        await self.websocket.send(message)

    async def close(self, code=1000, reason=''):
        self.logger.info('closing websocket')
        await self.websocket.close(code=code, reason=reason)
