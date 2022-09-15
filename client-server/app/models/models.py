import socket

clients = {}
delay = 0


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5050


class Actions:
    def __init__(self):
        self.delay = delay
        self.steps = []

    def add_action(self, action: str):
        self.steps.append(action)

    def remove_action(self, action: str):
        self.steps.remove(action)


class Client:

    def __init__(self, id: str, password: str, actions: Actions):
        self.id = id
        self.password = password
        self.counter = 0
        self.server = Server()
        self.actions = actions

    def __repr__(self):
        return f'Client({self.id}, {self.password})'

    def increase_counter(self, amount: int):
        self.counter += amount

    def decrease_counter(self, amount: int):
        self.counter += amount


def save_client(client: Client):
    # TODO: check if client is already logged, in case
    clients[client.id] = client


def get_client(id: int):
    return clients[id]


# TODO: check pop works fine
def delete_client(client: Client):
    clients.pop(client.id)

# TODO: hash id
