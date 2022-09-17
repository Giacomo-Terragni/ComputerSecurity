import json
from models.models import *


import requests
import json
import time

# This class should not use models so that client-server structure is separated

BASE_URL = "http://localhost:5000"
# ip = localhost
# port = 5000

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


def login_client(id, password):
    response = requests.post(BASE_URL + "/login-client", data={"id": id, "password": password})
    print(response.json())
    return response.json()


def logout_client(id):
    response = requests.delete(BASE_URL + "/logout-client", data={"id": id})
    print(response.json())
    return response


def increase_counter(id, amount):
    response = requests.post(BASE_URL + "/increase-counter", data={"id": id, "amount": amount})
    print(response.json())
    return response


def decrease_counter(id, amount):
    response = requests.post(BASE_URL + "/decrease-counter", data={"id": id, "amount": amount})
    print(response.json())
    return response


def get_client(user_id):
    response = requests.get(BASE_URL + "/user/" + user_id)
    return response.json()


def update_log(fname, user_id, action, amount):
    with open(fname, 'a+') as f:
        f.write(f'{user_id}  {action}  {amount}\n')
    f.close()



#TODO> send email -> ERIC
def run_gui():
    while True:
        login_answers = prompt(login_questions)
        login_response = login_client(**login_answers)
        if "result" not in login_response:
            continue
        user_id = login_answers["id"]
        while True:
            choices_answers = prompt(choices_list)
            choice = choices_answers["choice"]
            if choice == "Increase":
                amount_answers = prompt(amount_questions)  # this is the amount asked in prompt
                # TODO: check amount is convertible to integer
                increase_counter(user_id, int(amount_answers["amount"]))
                # TODO: update json with new action
            if choice == "Decrease":
                amount_answers = prompt(amount_questions)  # this is the amount asked in prompt
                # TODO: check amount is convertible to integer
                decrease_counter(user_id, int(amount_answers["amount"]))
                # TODO: update json with new action
            if choice == "Log out":
                logout_response = logout_client(user_id)
                break
        final_answers = prompt(final_list)
        answer = final_answers["choice"]
        if answer == "Quit":
            break


# TODO: handle exceptions -> Meli
# TODO: output txt file with counters of all clients -> ERIC

if __name__ == "__main__":
    # source: https://www.geeksforgeeks.org/read-json-file-using-python/
    # Opening JSON file
    f = open('data.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    BASE_URL = 'http://' + data["server"]["ip"] + ':' + data["server"]["port"]
    user_id = data["id"]
    password = data["password"]

    logfile = "./logs/server " + data["server"]["ip"] + " " + data["server"]["port"] + " log.txt"

    login_client(user_id, password)
    delay = int(data["actions"]["delay"])

    # loop throw actions
    for step in data["actions"]["steps"]:
        if "INCREASE" in step:
            new_casted_amount = step.replace("INCREASE ", "")
            increase_counter(user_id, int(new_casted_amount))
            # TODO: update log file: ERIC (DONE?)
            client = get_client(user_id)
            try:
                update_log(logfile, user_id, "INCREASE", client["counter"])
            except KeyError:
                print("Failed updating the log file")

        if "DECREASE" in step:
            new_casted_amount = step.replace("DECREASE ", "")
            decrease_counter(user_id, int(new_casted_amount))
            client = get_client(user_id)
            try:
                update_log(logfile, user_id, "DECREASE", client["counter"])
            except KeyError:
                print("Failed updating the log file")

        time.sleep(delay)

    f.close()
