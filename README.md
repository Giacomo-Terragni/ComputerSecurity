# Computer Security
Giacomo Terragni, Eric Banzuzi, Rosamelia Carioni, Chiara Paglioni, Elena Perego

## UML Diagram

![alt text](resources/ComputerSecurity.png)

## Requirements
Python 3 with these packages:
- requests
- flask
- cryptography

## 1. Flask
Make sure your terminal is at the same location as **app.py**. 
Initialize a server by typing:
`flask run`

You should be able to see the following in your  terminal:

![alt text](resources/flask.jpg)
<img src="resources/flask.jpg" width=800 height=100>

## 2. Clients
Open a new terminal in the same location as **client.py** and start the program by typing:

`python client.py`

The following window will open up:

![alt text](resources/gui.png)

Upload the *.json* file that you want to read by pressing the **Open File** button. 
Make sure the file is in the following format:

```
{"id": "100",
"password": "eleele",
"server":
{
  "ip": "127.0.0.1",
  "port": "5000"
},
"actions": {
  "delay": "4",
  "steps": [
    "INCREASE 2000",
    "DECREASE 100",
    "DECREASE 100",
    "DECREASE 100",
    "DECREASE 100"
  ]
}
}
```

## 3. Responses
If everything went well, you should see this in the terminal where the client was read:

![alt text](resources/success.jpg)

The errors for each action are handled separately.
If the client has an invalid value for the amount of **INCREASE** or **DECREASE** inside the actions,
the user will see the errors in the terminal as output. For example, for this client:

![alt text](resources/json.jpg)

You should see the following output:

![alt text](resources/error.jpg)

## 4. Log file
All outputs from the actions executed on the clients counter are stored in a log file in *app/logs/logs.txt*. 
If you wish to store the data in a different file, change the value of variable **FILENAME** in app.py to the new file's name.

The file information is in the following format:
```
ID: 100 | NEW LOG IN | COUNTER: 0
ID: 100 | INCREASE 10 | COUNTER: 10
ID: 100 | DECREASE 1 | COUNTER: 9
```
