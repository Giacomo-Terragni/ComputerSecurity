import json
from models.models import *

from PyInquirer import prompt
import requests

BASE_URL = "http://localhost:5000"

choices_list = {
    "type": "list",
    "name": "choice",
    "message": "What would you like to do?",
    "choices": ["Increase", "Decrease", "Log out"],
}

final_list = {
    "type": "list",
    "name": "choice",
    "message": "What would you like to do?",
    "choices": ["Log in again", "Quit"],
}

login_questions = [
    {"type": "input", "message": "ID", "name": "id"},
    {"type": "input", "message": "Password", "name": "password"}
]

amount_questions = [
    {"type": "input", "message": "Amount", "name": "amount"}
]


def login_client(id, password, server, actions):
    response = requests.post(BASE_URL + "/login-client", data={"id": id, "password": password,
                                                               "server": json.dumps(server),
                                                               "actions": json.dumps(actions)})
    print(response.json())
    return response.json()

def logout_client(id):
    response = requests.delete(BASE_URL + "/logout-client", data={"id": id})
    print(response.json())
    return response


if __name__ == "__main__":
    while True:
        login_answers = prompt(login_questions)
        login_response = login_client(**login_answers)
        if "result" not in login_response:
            continue
        client_id = login_answers["id"]
        client = get_client(client_id)
        while True:
            choices_answers = prompt(choices_list)
            choice = choices_answers["choice"]
            if choice == "Increase":
                amount_answers = prompt(amount_questions)  # this is the amount asked in prompt
                # TODO: check amount is convertible to integer
                client.increase_counter(int(amount_answers["amount"]))
            if choice == "Decrease":
                amount_answers = prompt(amount_questions)  # this is the amount asked in prompt
                # TODO: check amount is convertible to integer
                client.decrease_counter(int(amount_answers["amount"]))
            if choice == "Log out":
                logout_response = logout_client(client_id)
                break
        final_answers = prompt(final_list)
        answer = final_answers["choice"]
        if answer == "Quit":
            break
