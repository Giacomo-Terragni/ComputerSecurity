clients = {}


class Client:

    def __init__(self, id, password):
        self.id = id
        self.password = password

    def __repr__(self):
        return f'Client({self.id}, {self.password})'
