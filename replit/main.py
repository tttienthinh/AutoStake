import pandas as pd
from datetime import datetime
from flask import Flask
from flask import request
import os


app = Flask('')
target_password = os.getenv("password")

def calcul_credit(ip):
    df_fees = pd.read_csv("data/fees.csv")
    df_pay = pd.read_csv("data/pay.csv")
    
    fees = df_fees.USDTfees[df_fees.ip == ip].sum()
    pay = df_pay.USDTpay[df_pay.ip == ip].sum()
    
    credits = 1 + pay - fees
    return float(credits)


@app.route('/')
def home():
    return "This Website support the <a href='https://tttienthinh.github.io/AutoStake/'>GitHub</a>"

# Startup
@app.route('/api/startup/', methods=['GET'])
def startup(): # ip version -> credit exec
    ip = request.args['ip']
    version = request.args['version']

    with open("data/startup.csv", "a+") as f:
        f.write(f"\n{ip},{datetime.now()},{version}")
        f.close()    

    credit = calcul_credit(ip)
    exec = "None"
    return {"credit": credit, "exec": exec}

# Log
@app.route('/api/log/', methods=['GET'])
def log(): # ip version log -> credit exec
    ip = request.args['ip']
    version = request.args['version']
    log = request.args['log']

    with open("data/log.csv", "a+") as f:
        f.write(f"\n{ip},{datetime.now()},{version},{log}")
        f.close()    

    exec = "None"
    return {"exec": exec}

# Fees
@app.route('/api/fees/', methods=['GET'])
def fees(): # ip token token_amount USDT_amount USDT_fees -> exec
    ip = request.args['ip']
    token = request.args['token']
    token_amount = request.args['token_amount']
    USDT_amount = request.args['USDT_amount']
    USDT_fees = request.args['USDT_fees']

    with open("data/fees.csv", "a+") as f:
        f.write(f"\n{ip},{datetime.now()},{token},{token_amount},{USDT_amount},{USDT_fees}")
        f.close()    

    exec = "None"
    return {"exec": exec}

# Pay
@app.route('/api/pay/', methods=['GET'])
def pay(): # ip email  USDT_pay pass -> credit
    ip = request.args['ip']
    email = request.args['email']
    USDT_pay = request.args['USDT_pay']
    password = request.args['password']

    if password == target_password:
    with open("data/pay.csv", "a+") as f:
        f.write(f"\n{ip},{datetime.now()},{email},{USDT_pay}")
        f.close()    

    credit = calcul_credit(ip)
    return {"credit": credit}


app.run(host='0.0.0.0', port=8080, debug=True)