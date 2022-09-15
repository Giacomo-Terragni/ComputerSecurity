from flask import Flask, request, make_response
from datetime import datetime

app = Flask(__name__)

fmt = '%Y-%m-%d %H:%M:%S'  # for datetime calculations


@app.route("/") # hello :)
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/create-customer", methods=["POST"])
def create_customer():
    from models.sql_model import save_new_customer

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone_number = request.form["phone_number"]
    street = request.form["street"]
    house_number = request.form["house_number"]
    city = request.form["city"]
    postcode = request.form["postcode"]

    try:
        save_new_customer(firstname, lastname, phone_number, street, house_number, city, postcode)
    except Exception as ex:
        return make_response({"error": f"could not create user {str(ex)}"}, 400)

    return make_response({"result": "success"}, 200)


@app.route("/create-order", methods=["POST"])
def create_order():
    from models.sql_model import save_new_order, save_new_orderline, find_single_customer, find_single_address, save_available_delivery
    import json

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    street = request.form["street"]
    house_number = request.form["house_number"]
    postcode = request.form["postcode"]
    pizzas = json.loads(request.form["pizzas"])
    drinks = json.loads(request.form["drinks"])
    deserts = json.loads(request.form["deserts"])
    discount = request.form["discount"]

    if len(pizzas) == 0:
        return make_response({"error": "order does not contain any pizzas"}, 400)

    address = find_single_address(street=street, house_number=house_number, postcode=postcode)
    if address is None:
        return make_response({"error": "address is not in the system"}, 400)

    customer = find_single_customer(firstname=firstname, lastname=lastname, address_id=address.id)
    if customer is None:
        return make_response({"error": "customer has not been created"}, 400)

    try:
        order = save_new_order(customer_id=customer.id, time=datetime.now().strftime(fmt), code=discount)
        for orderline in pizzas:
            save_new_orderline(order.id, "Pizza", orderline[0], orderline[1])

        for orderline in drinks:
            save_new_orderline(order.id, "Drink", orderline[0], orderline[1])

        for orderline in deserts:
            save_new_orderline(order.id, "Desert", orderline[0], orderline[1])

        save_available_delivery(order, address.postcode, order.datetime)

    except Exception as ex:
        return make_response({"error": f"could not create order {str(ex)}"}, 400)

    return make_response({"result": "success"}, 200)


@app.route("/cancel-order", methods=["DELETE"])
def cancel_order():
    from models.sql_model import delete_single_delivery, find_single_order

    order_id = request.form["order_id"]
    order = find_single_order(id=order_id)

    now = datetime.now().strftime(fmt)
    # calculate time difference in minutes
    d1 = datetime.strptime(str(order.datetime), fmt)
    d2 = datetime.strptime(now, fmt)
    diff = d2 - d1
    diff_minutes = diff.seconds / 60

    if diff_minutes < 5:
        try:
            delete_single_delivery(order_id=order.id)
        except Exception as ex:
            return make_response({"error": f"could not cancel order {str(ex)}"}, 400)

        return make_response({"result": "success"}, 200)
    else:
        return make_response({"error": f"order {order.id} cannot be canceled anymore"}, 400)


@app.route("/customer/<customer_id>")
def get_customer(customer_id: int):
    from models.sql_model import find_single_customer, find_single_address
    customer = find_single_customer(id=customer_id)
    address = find_single_address(id=customer.address_id)
    if customer:
        return make_response({"firstname": customer.firstname, "lastname": customer.lastname, "phone": customer.phone_number,
                              "street": address.street, "house_number": address.house_number, "city": address.city, "postcode": address.postcode}, 200)
    else:
        return make_response({"error": f"Customer with id {customer_id} does not exist"}, 400)


@app.route("/track-order/<order_id>")
def track_order(order_id: int):
    from models.sql_model import find_single_order, find_single_delivery

    order = find_single_order(id=order_id)
    if order:
        delivery = find_single_delivery(order_id=order.id)
        if delivery is None:
            return make_response({"status": "CANCELLED"}, 200)

        now = datetime.now().strftime(fmt)
        # calculate time difference in minutes
        d1 = datetime.strptime(str(delivery.estimated_time), fmt)
        d2 = datetime.strptime(now, fmt)
        diff = d2 - d1
        diff_minutes = diff.seconds / 60

        if diff.days >= 0 and diff_minutes > 0:
            return make_response({"status": "DELIVERED"}, 200)
        # calculate time difference in minutes
        d1 = datetime.strptime(str(order.datetime), fmt)
        d2 = datetime.strptime(now, fmt)
        diff = d2 - d1
        diff_minutes = diff.seconds / 60

        if diff_minutes < 5:
            return make_response({"status": "IN PROCESS", "estimated_time": delivery.estimated_time}, 200)
        else:
            return make_response({"status": "OUT FOR DELIVERY", "estimated_time": delivery.estimated_time}, 200)

    else:
        return make_response({"error": f"Order with id {order_id} does not exist"}, 400)
