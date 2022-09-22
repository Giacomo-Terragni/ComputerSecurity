import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

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


# TODO: method to generate private key (Giaco)--> check
def generate_key_files():
    # generating public/private
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    # Storing private Keys
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as f:
        f.write(pem)
    # storing public
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(pem)


def get_public_key():
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def get_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


