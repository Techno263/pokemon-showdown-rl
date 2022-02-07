class Move:

    def __init__(self, name, identifier, pp, max_pp, target, disabled):
        self.name = name
        self.identifier = identifier
        self.pp = pp
        self.max_pp = max_pp
        self.target = target
        self.disabled = disabled

    @property
    def percentage_pp(self):
        return self.pp / self.max_pp

    @staticmethod
    def from_request(request_move):
        name = request_move['move']
        identifier = request_move['id']
        pp = request_move['pp'] if 'pp' in request_move else None
        max_pp = request_move['maxpp'] if 'maxpp' in request_move else None
        target = request_move['target'] if 'target' in request_move else None
        disabled = request_move['disabled'] if 'disabled' in request_move else None
        return Move(name, identifier, pp, max_pp, target, disabled)
