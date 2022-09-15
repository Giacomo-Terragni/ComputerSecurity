from flask import Flask, request, make_response
from models.models import *

app = Flask(__name__)

fmt = '%Y-%m-%d %H:%M:%S'  # for datetime calculations


# TODO: check id is valid (string)
@app.route("/login-client", methods=["POST"])
def login_client():
    id = request.form["id"]
    password = request.form["password"]
    actions = Actions()
    client = Client(id, password, actions)

    if id not in clients:
        try:
            save_client(client)
        except Exception as ex:
            return make_response({"error": f"could not log in {str(ex)}"}, 400)
        print(clients)
        return make_response({"result": "success"}, 200)
    else:
        # TODO: check password if it is the same then handle same user in different devices, if it is not then error
        return



# TODO: log in file counter of the client logging out
@app.route("/logout-client", methods=["DELETE"])
def logout_client():
    id = request.form["id"]
    try:
        delete_client(clients[id])
    except Exception as ex:
        return make_response({"error": f"could not log out {str(ex)}"}, 400)
    return make_response({"result": "success"}, 200)