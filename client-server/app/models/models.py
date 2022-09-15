import socket

users = {}
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


class User:

    def __init__(self, id: str, password: str, actions: Actions):
        self.id = id # TODO: maybe this could also be name or contain letters
        self.password = password
        self.counter = 0
        self.actions = actions #TODO: probably delete this

    def __repr__(self):
        return f'Client({self.id}, {self.password}, {self.counter})'



def save_user(client: User):
    # TODO: check if client is already logged, in case
    users[client.id] = client


# TODO: check pop works fine
def delete_user(user: User):
    users.pop(user.id)

# TODO: hash id and password
