import json

from PyInquirer import prompt
import requests
from models.sql_model import show_menu, show_order

BASE_URL = "http://localhost:5000"

main_list = {
    "type": "list",
    "name": "choice",
    "message": "What do you want to do?",
    "choices": ["Create a customer", "Create an order", "Get a customer", "Track order",
                "Cancel order", "Quit"],
}

item_list = {
    "type": "list",
    "name": "choice",
    "message": "Add item to order",
    "choices": ["Pizza", "Drink", "Desert", "Discount code", "Ready"],
}

order_questions = [
    {"type": "input", "message": "First name", "name": "firstname"},
    {"type": "input", "message": "Last name", "name": "lastname"},
    {"type": "input", "message": "Street", "name": "street"},
    {"type": "input", "message": "House number", "name": "house_number"},
    {"type": "input", "message": "Post code", "name": "postcode"}
]

customer_questions = [
    {"type": "input", "message": "First name", "name": "firstname"},
    {"type": "input", "message": "Last name", "name": "lastname"},
    {"type": "input", "message": "Phone number", "name": "phone_number"},
    {"type": "input", "message": "Street", "name": "street"},
    {"type": "input", "message": "House number", "name": "house_number"},
    {"type": "input", "message": "City", "name": "city"},
    {"type": "input", "message": "Post code", "name": "postcode"}
]

customer_id_questions = [
    {"type": "input", "message": "Enter the id", "name": "customer_id"}
]

pizza_questions = [
    {"type": "input", "message": "Enter the pizza id", "name": "pizza_id"},
    {"type": "input", "message": "Quantity", "name": "quantity"}
]

drink_questions = [
    {"type": "input", "message": "Enter the drink id", "name": "drink_id"},
    {"type": "input", "message": "Quantity", "name": "quantity"}
]

desert_questions = [
    {"type": "input", "message": "Enter the desert id", "name": "desert_id"},
    {"type": "input", "message": "Quantity", "name": "quantity"}
]

order_id_questions = [
    {"type": "input", "message": "Enter the id", "name": "order_id"}
]

discount_questions = [
    {"type": "input", "message": "Enter the code", "name": "discount_code"}
]


def customer(firstname, lastname, phone_number, street, house_number, city, postcode):
    response = requests.post(BASE_URL + "/create-customer", data={"firstname": firstname, "lastname": lastname, "phone_number": phone_number,
                                                                  "street": street, "house_number": house_number, "city": city, "postcode": postcode})
    print(response.json())


def order(firstname, lastname, street, house_number, postcode, pizzas, drinks, deserts, discount_code):
    response = requests.post(BASE_URL + "/create-order", data={"firstname": firstname, "lastname": lastname, "street": street, "house_number": house_number,
                                                               "postcode": postcode, "pizzas": json.dumps(pizzas), "drinks": json.dumps(drinks), "deserts": json.dumps(deserts),
                                                               "discount": discount_code})
    print(response.json())


def get_customer(customer_id):
    response = requests.get(BASE_URL + "/customer/" + customer_id)
    print(response.json())


def track_order(order_id):
    response = requests.get(BASE_URL + "/track-order/" + order_id)
    print(response.json())


def cancel_order(order_id):
    response = requests.delete(BASE_URL + "/cancel-order", data={"order_id": order_id})
    print(response.json())


if __name__ == "__main__":
    show_menu()
    while True:
        answers = prompt(main_list)
        answer = answers["choice"]
        if answer == "Create a customer":
            customer_answers = prompt(customer_questions)
            customer(**customer_answers)

        if answer == "Create an order":
            order_answers = prompt(order_questions)
            pizzas = []
            drinks = []
            deserts = []
            discount = ""
            while True:
                items = prompt(item_list)
                item = items["choice"]
                if item == "Pizza":
                    pizza_ans = prompt(pizza_questions)
                    pizzas.append((int(pizza_ans["pizza_id"]), int(pizza_ans["quantity"])))
                if item == "Drink":
                    drink_ans = prompt(drink_questions)
                    drinks.append((int(drink_ans["drink_id"]), int(drink_ans["quantity"])))
                if item == "Desert":
                    desert_ans = prompt(desert_questions)
                    deserts.append((int(desert_ans["desert_id"]), int(desert_ans["quantity"])))
                if item == "Discount code":
                    discount_ans = prompt(discount_questions)
                    discount = discount_ans["discount_code"]
                if item == "Ready":
                    break

            order(order_answers["firstname"], order_answers["lastname"], order_answers["street"],
                  order_answers["house_number"], order_answers["postcode"], pizzas, drinks, deserts, discount)
            show_order()

        if answer == "Get a customer":
            get_customer_answers = prompt(customer_id_questions)
            get_customer(**get_customer_answers)

        if answer == "Track order":
            order_id_answers = prompt(order_id_questions)
            track_order(**order_id_answers)

        if answer == "Cancel order":
            order_id_answers = prompt(order_id_questions)
            cancel_order(**order_id_answers)

        if answer == "Quit":
            break
