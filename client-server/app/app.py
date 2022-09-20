from flask import Flask, request, make_response
from models.models import *

# This is the server
app = Flask(__name__)

fmt = '%Y-%m-%d %H:%M:%S'  # for datetime calculations


@app.route("/login-client", methods=["POST"])
def login_client():
    id = request.form["id"]
    password = request.form["password"]
    actions = request.form["actions"]
    actions = Actions
    user = User(id, password, actions)

    if id not in users:
        try:
            save_user(user)
        except Exception as ex:
            return make_response({"error": f"could not log in {str(ex)}"}, 400)
        print(users)
        return make_response({"result": "success"}, 200)
    else:
        # TODO: check password -> GIACO,  ELE
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
        # check whether amount is integer
        if amount.isinteger():
            users[id].counter += amount
        else:
            return make_response({"error": f"amount not int"}, 400)
    except Exception as ex:
        return make_response({"error": f"unable to increase counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/decrease-counter", methods=["POST"])
def decrease_counter():
    id = request.form["id"]
    amount = int(request.form["amount"])
    try:
        users[id].counter -= amount
        # check whether amount is integer
        if amount.isinteger():
            users[id].counter -= amount
        else:
            return make_response({"error": f"amount not int"}, 400)
    except Exception as ex:
        return make_response({"error": f"unable to decrease counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)
