from flask import Flask, request, make_response
from models.models import *

# This is the server
app = Flask(__name__)
FILENAME = "./logs/logs.txt"


# TODO: this is not being called when client is created, i thought it should ? and that it should say counter 0
def update_log(user_id, action, amount):
    with open(FILENAME, 'a+') as f:
        f.write(f'{user_id}  {action}  {amount}\n')
    f.close()


@app.route("/login-client", methods=["POST"])
def login_client():
    id = request.form["id"]
    password = request.form["password"]
    hash_id = hash(id)
    hash_password = hash(password)
    user = User(hash_id, hash_password)
    if hash_id not in users:
        try:
            save_user(user)
            update_log(id, "NEW LOG IN", user.counter)  # ??
        except Exception as ex:
            return make_response({"error": f"could not log in {str(ex)}"}, 400)
        print(users)
        return make_response({"result": "success"}, 200)
    else:
        for key in users:
            if users[key].password == hash_password:
                return make_response({"result": "success"}, 200)
        return make_response({"result": "fail"}, 400)


@app.route("/logout-client", methods=["DELETE"])
def logout_client():
    id = request.form["id"]
    try:
        delete_user(users[id])
    except Exception as ex:
        return make_response({"error": f"could not log out {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/increase-counter", methods=["POST"])
def increase_counter():
    id = request.form["id"]
    amount = int(request.form["amount"])
    try:
        #TODO: check that this type of amount input  is correct -> CHIARA
        users[id].counter += amount
        update_log(id, "INCREASE", users[id].counter)
    except Exception as ex:
        return make_response({"error": f"unable to increase counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/decrease-counter", methods=["POST"])
def decrease_counter():
    id = request.form["id"]
    amount = int(request.form["amount"])
    try:
        #TODO: check that this type of amount input  is correct -> CHIARA
        users[id].counter -= amount
        update_log(id, "DECREASE", users[id].counter)
    except Exception as ex:
        return make_response({"error": f"unable to decrease counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)