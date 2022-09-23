import base64

from flask import Flask, request, make_response
from models.models import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# This is the server
app = Flask(__name__)
FILENAME = "./logs/logs.txt"
private_key = get_private_key()
public_key = get_public_key(private_key)


def decrypt_message(message):
    decrypted_message = private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode("utf-8")


def update_log(user_id, action, counter):
    with open(FILENAME, 'a+') as f:
        f.write(f'ID: {user_id} | {action} | COUNTER: {counter}\n')
    f.close()


@app.route("/login-client", methods=["POST"])
def login_client():
    id = decrypt_message(base64.b64decode(request.form["id"]))
    password = decrypt_message(base64.b64decode(request.form["password"]))
    hash_id = hash(id)
    hash_password = hash(password)
    user = User(hash_id, hash_password)
    # user doesnt exist
    if hash_id not in users:
        try:
            save_user(user)
            update_log(id, "NEW LOG IN", user.counter)
        except Exception as ex:
            return make_response({"error": f"could not log in {str(ex)}"}, 400)
        return make_response({"result": "success"}, 200)
    else:
        for key in users:
            if users[key].password == hash_password:
                users[key].login_counter += 1
                update_log(id, "NEW LOG IN", users[key].counter)
                return make_response({"result": "success"}, 200)
        return make_response({"result": "fail"}, 400)


@app.route("/logout-client", methods=["DELETE"])
def logout_client():
    id = decrypt_message(base64.b64decode(request.form["id"]))
    try:
        if users[hash(id)].login_counter > 1:
            users[hash(id)].login_counter -= 1
        else:
            delete_user(users[hash(id)])
    except Exception as ex:
        return make_response({"error": f"could not log out {str(ex)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/increase-counter", methods=["POST"])
def increase_counter():
    id = decrypt_message(base64.b64decode(request.form["id"]))
    amount = decrypt_message(base64.b64decode(request.form["amount"]))
    try:
        amount = int(amount)
    except ValueError:
        return make_response({"error": f"amount provided is not an integer"}, 400)

    if amount < 0:
        return make_response({"error": f"amount provided is negative"}, 400)

    try:
        users[hash(id)].counter += amount
        update_log(id, f"INCREASE {amount}", users[hash(id)].counter)
    except Exception as ex:
        return make_response({"error": f"unable to increase counter {str(ex)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/decrease-counter", methods=["POST"])
def decrease_counter():
    id = decrypt_message(base64.b64decode(request.form["id"]))
    amount = decrypt_message(base64.b64decode(request.form["amount"]))
    try:
        amount = int(amount)
    except ValueError:
        return make_response({"error": f"amount provided is not an integer"}, 400)

    if amount < 0:
        return make_response({"error": f"amount provided is negative"}, 400)

    try:
        if (users[hash(id)].counter - amount) < 0:
            return make_response({"error": f"counter cannot be negative"}, 400)

        users[hash(id)].counter -= amount
        update_log(id, f"DECREASE {amount}", users[hash(id)].counter)
    except Exception as ex:
        return make_response({"error": f"unable to decrease counter {str(ex)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/public-key", methods=["GET"])
def get_public_key():
    return make_response(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
