import hashlib

users = {}
delay = 0


class User:

    def __init__(self, id: str, password: str):
        self.id = id
        self.password = password
        self.counter = 0
        self.login_counter = 1

    def __repr__(self):
        return f'Client({self.id}, {self.password}, {self.counter})'


def save_user(client: User):
    users[client.id] = client


def delete_user(user: User):
    users.pop(user.id)


# TODO: add salt, pepper and private keys and public key
# TODO: how to compare 2 hashs id of the same user
def hash(input: str):
    hashed_input = hashlib.sha256(input.encode('utf-8')).hexdigest()
    return hashed_input
