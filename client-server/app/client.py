import base64

import requests
import json
import time
import sys
import argparse
from gui import visual
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from models.models import *

# This class should not use models so that client-server structure is separated
from cryptography.hazmat.primitives.serialization import load_pem_public_key

BASE_URL = ""


def encrypt_message(message):
    public_key = get_public_key()
    message = str.encode(message)
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message


def login_client(id, password):
    encrypted_id = encrypt_message(id)
    encrypted_password = encrypt_message(password)
    response = requests.post(BASE_URL + "/login-client", data={"id": base64.b64encode(encrypted_id), "password": base64.b64encode(encrypted_password)})
    print(response.json())
    return response.json()


def logout_client(id):
    encrypted_id = encrypt_message(id)
    response = requests.delete(BASE_URL + "/logout-client", data={"id": base64.b64encode(encrypted_id)})
    print(response.json())
    return response


def increase_counter(id, amount):
    encrypted_id = encrypt_message(id)
    encrypted_amount = encrypt_message(amount)
    response = requests.post(BASE_URL + "/increase-counter", data={"id": base64.b64encode(encrypted_id), "amount": base64.b64encode(encrypted_amount)})
    print(response.json())
    return response


def decrease_counter(id, amount):
    encrypted_id = encrypt_message(id)
    encrypted_amount = encrypt_message(amount)
    response = requests.post(BASE_URL + "/decrease-counter", data={"id": base64.b64encode(encrypted_id), "amount": base64.b64encode(encrypted_amount)})
    print(response.json())
    return response


def get_public_key():
    response = requests.get(BASE_URL + "/public-key")
    return load_pem_public_key(response.content)


def initialize_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    return vars(parser.parse_args())


# python client.py --file data.json
if __name__ == "__main__":
    # source: https://www.geeksforgeeks.org/read-json-file-using-python/
    # Opening JSON file
    visual.setup_gui()

    try:
        args = initialize_argparse()
        path = visual.filenames.pop()
        file = open(path)
        data = json.load(file)
    except Exception:
        sys.exit("Error: Invalid JSON file provided.")

    try:
        BASE_URL = 'http://' + data["server"]["ip"] + ':' + data["server"]["port"]
        print('URL:', BASE_URL)
        user_id = data["id"]
        password = data["password"]
        delay = int(data["actions"]["delay"])
    except KeyError:
        sys.exit("Error: Input file does not contain right input format.")

    result = login_client(user_id, password)
    if result['result'] == 'fail':
        sys.exit('Error: Invalid combination of password and user ID.')

    # loop throw actions
    for step in data["actions"]["steps"]:
        if "INCREASE" in step:
            new_casted_amount = step.replace("INCREASE ", "")
            increase_counter(user_id, new_casted_amount)

        if "DECREASE" in step:
            new_casted_amount = step.replace("DECREASE ", "")
            decrease_counter(user_id, new_casted_amount)

        time.sleep(delay)
    logout_client(user_id)
    file.close()
