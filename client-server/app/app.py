from flask import Flask, request, make_response, jsonify
from models.models import *

# This is the server
app = Flask(__name__)
FILENAME = "./logs/logs.txt"
generate_key_files()
private_key = get_private_key()
public_key = get_public_key()


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
    id = decrypt_message(request.form["id"])
    password = decrypt_message(request.form["password"])
    # TODO: check for injections in id and password (Giaco)
    hash_id = hash(id)
    hash_password = hash(password)
    user = User(hash_id, hash_password)
    # user doesnt exist
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
                users[key].login_counter += 1
                update_log(id, "NEW LOG IN", users[key].counter)
                return make_response({"result": "success"}, 200)
        return make_response({"result": "fail"}, 400)


@app.route("/logout-client", methods=["DELETE"])
def logout_client():
    id = decrypt_message(request.form["id"])
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
    id = decrypt_message(request.form["id"])
    amount = decrypt_message(request.form["amount"])
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
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/decrease-counter", methods=["POST"])
def decrease_counter():
    id = request.form["id"]
    amount = request.form["amount"]
    # TODO: decrypt data using private key (Giaco)-->check
    id = decrypt_message(id)
    amount = decrypt_message(amount)
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
    print(users)
    return make_response({"result": "success"}, 200)


@app.route("/public-key", methods=["GET"])
def get_public_key():
    return public_key
