from flask import Flask, request, make_response
from models.models import *

# This is the server
app = Flask(__name__)

fmt = '%Y-%m-%d %H:%M:%S'  # for datetime calculations


# TODO: check id is valid (string)
@app.route("/login-client", methods=["POST"])
def login_client():
    id = request.form["id"]
    password = request.form["password"]
    actions = Actions() #TODO come back to this based on response from email, most likely we will delete it
    user = User(id, password, actions)

    if id not in users:
        try:
            save_user(user)
        except Exception as ex:
            return make_response({"error": f"could not log in {str(ex)}"}, 400)
        print(users)
        return make_response({"result": "success"}, 200)
    else:
        # TODO: check password if it is the same then handle same user in different devices, if it is not then error
        return make_response({"result": "fail"}, 400)


# TODO: log in file counter of the client logging out
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
        #TODO: check that this type of amount input  is correct
        users[id].counter += amount
    except Exception as ex:
        return make_response({"error": f"unable to increase counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/decrease-counter", methods=["POST"])
def decrease_counter():
    id = request.form["id"]
    amount = int(request.form["amount"])
    try:
        #TODO: check that this type of amount input  is correct
        users[id].counter -= amount
    except Exception as ex:
        return make_response({"error": f"unable to decrease counter {str(ex)}"}, 400)
    print(users)
    return make_response({"result": "success"}, 200)