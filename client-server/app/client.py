import base64

import requests
import json
import time
import sys
import argparse
from gui import visual
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

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


def check_connection(ip, port):
    if ip == "127.0.0.1" and port == "5000":
        return True
    else:
        return False


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
        ip = data["server"]["ip"]

        if ip == "":
            sys.exit("Error: empty ip.")

    except KeyError:
        sys.exit("Error: ip not in json file.")

    try:
        port = data["server"]["port"]

        if port == "":
            sys.exit("Error: empty port.")

    except KeyError:
        sys.exit("Error: port not in json file.")

    try:
        user_id = data["id"]

        if user_id == "":
            sys.exit("Error: empty user id.")

        if len(user_id) > 100:
            sys.exit("Error: user id too long (maximum 100 characters).")

    except KeyError:
        sys.exit("Error: user id not in json file.")

    try:
        password = data["password"]

        if password == "":
            sys.exit("Error: empty password.")

        if len(password) > 100:
            sys.exit("Error: password too long (maximum 100 characters).")

    except KeyError:
        sys.exit("Error: password not in json file.")

    try:
        delay = data["actions"]["delay"]

        if delay == "":
            sys.exit("Error: empty delay.")

        delay = int(delay)

        if delay <= 0:
            sys.exit("Error: negative or 0 delay.")

        if delay >= 86401:
            sys.exit("Error: delay should be at most 86400 seconds (1 day).")

    except KeyError:
        sys.exit("Error: delay not in json file.")
    except ValueError:
        sys.exit("Error: delay is not an integer.")

    try:
        ip = data["server"]["ip"]
        port = data["server"]["port"]
        if not check_connection(ip, port):
            sys.exit("Error: Input file does not contain right IP and port.")
        BASE_URL = 'http://' + ip + ':' + port
        print('URL:', BASE_URL)

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
