from flask import Flask, request, make_response
from datetime import datetime
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
        return make_response({"result": "success"}, 200)
    else:
        # TODO: check password
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

# @app.route("/customer/<customer_id>")
# def get_customer(customer_id: int):
#     customer = find_single_customer(id=customer_id)
#     address = find_single_address(id=customer.address_id)
#     if customer:
#         return make_response({"firstname": customer.firstname, "lastname": customer.lastname, "phone": customer.phone_number,
#                               "street": address.street, "house_number": address.house_number, "city": address.city, "postcode": address.postcode}, 200)
#     else:
#         return make_response({"error": f"Customer with id {customer_id} does not exist"}, 400)
