import hashlib
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

    def __repr__(self):
        return f'Client({self.id}, {self.password}, {self.counter})'


def save_user(client: User):
    users[client.id] = client


# TODO: debugging in future
def delete_user(user: User):
    users.pop(user.id)

def hash(input: str):
    hashed_input = hashlib.sha256(input.encode('utf-8')).hexdigest()
    return hashed_input
