import socket

users = {}
delay = 0


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5050


class Actions:
    def __init__(self, delay):
        self.delay = delay
        self.steps = []

    def add_action(self, action: str):
        self.steps.append(action)

    def remove_action(self, action: str):
        self.steps.remove(action)


class User:

    def __init__(self, id: str, password: str):
        self.id = id
        self.password = password
        self.counter = 0
        # self.actions = actions #TODO: probably delete this: ELENA

    def __repr__(self):
        return f'Client({self.id}, {self.password}, {self.counter})'



def save_user(client: User):
    users[client.id] = client


# TODO: debugging in future
def delete_user(user: User):
    users.pop(user.id)

# TODO: hash id slides and password -> GIACOMO, ELENA
