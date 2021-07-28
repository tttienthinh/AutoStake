from bs import BS
from selenium import webdriver
import time, requests, json, pickle


def get_ip():
    while True:
        try:
            r = requests.get("https://api.ipify.org?format=json")
            break
        except:
            input("Can't connect to internet, \nEnter to try again")
    try:
        if r.ok:
            return r.json()["ip"]
        else:
            return "ipaddress"
    except:
        return "ipaddress"

def api(ip, log):
    url = f"https://AutoStake.tienthinh1.repl.co?ip={ip}&log={time.asctime()}-{log}"
    return requests.get(url)

def get_driver():
    # Windows
    executable_list = [
        ("drivers/geckodriver-64.exe", webdriver.Firefox), 
        ("drivers/geckodriver-32.exe", webdriver.Firefox), 
        ("drivers/chromedriver91-32.exe", webdriver.Chrome),  
        ("drivers/chromedriver92-32.exe", webdriver.Chrome)
    ]
    # Mac
    executable_list = [
        ("drivers/chromedriver91-mac", webdriver.Chrome),
        ("drivers/geckodriver-mac", webdriver.Firefox),
        ("drivers/chromedriver92-mac64", webdriver.Chrome),
        ("drivers/chromedriver91-macm1", webdriver.Chrome),
        ("drivers/chromedriver92-macm1", webdriver.Chrome),
    ]
    # Linux
    executable_list = [
        ("drivers/chromedriver91-linux64", webdriver.Chrome),
        ("drivers/chromedriver92-linux64", webdriver.Chrome),
        ("drivers/geckodriver-linux64", webdriver.Firefox),
        ("drivers/geckodriver-linux32", webdriver.Firefox),
    ]

    for (executable, w_driver) in executable_list:
        try:
            driver = w_driver(executable_path=executable)
            print(f"Got driver {executable}")
            return True, driver
        except:
            print(f"driver {executable} not working")
    return False, None

def binance():
    response = json.loads(requests.get(
        "https://www.binance.com/gateway-api/v1/friendly/pos/union?\
        pageSize=50&pageIndex=1&status=ALL").text)['data']
    result = []
    for item in response:
        for asset in item["projects"]:
            if not asset["sellOut"]:
                result.append({
                    "asset": asset["asset"],
                    "duration": asset["duration"],
                    "APY": str(round(float(asset["config"]["annualInterestRate"]) * 100, 2))
                })
    return result

print("Welcome to AutoStake !")
ip = get_ip()
past_fees = pickle.load(open("data/data.pkl", "rb"))["fees"]
api(ip, past_fees)
ok, driver = get_driver()

if not ok:
    input("Please install Firefox (geckodriver) or Chrome (chromedriver) and download drivers/")
else:
    # Connection
    b_driver = BS(driver)
    print("\nMake sure you have at least : ")
    print(" 1 USDT in P2P transfert Binance to pay fees")
    input("Enter when login is done : ")
    b_driver.stake_page()
    # Staking tokens
    tokens = json.load(open("tokens.json", "r"))
    print()
    print(tokens)
    ans = input("Would you like to continue staking this ? [y/n] : ")
    if ans != "y":
        tokens = []
        while True:
            token = input("\nEnter token Name or just Enter to run : ")
            token = token.upper().replace(" ", "")
            if token == "":
                break
            else:
                days = input("Days Staking periods : ")
                tokens.append({
                    "TOKEN": token,
                    "DAYS": days
                })
        json.dump(tokens, open("tokens.json", "w"))
    print(f"I will look to stake \n {tokens}")

    # Searching
    past_result = []
    print("\nI will search for Locked Staking")
    while True:
        print(time.asctime())
        result = binance()
        for data in result:
            if data not in past_result:
                asset = data['asset']
                duration = data['duration']
                apy = data['APY']
                print(f"Found new release \
                {asset} {duration} days {apy}% APY")
                
                if {'TOKEN': asset, 'DAYS': duration} in tokens:
                    amount, fees = b_driver.stake()
                    print(f"Staked Successfully !")
                    done = b_driver.donation(fees + past_fees, ip)
                    # Paying fees
                    if done:
                        dico = pickle.load(open("data/data.pkl", "rb"))
                        dico["fees"] = 0
                        pickle.dump(dico, open("data/data.pkl", "wb"))
                        past_fees = 0
                    else:
                        past_fees += fees 
                        dico = pickle.load(open("data/data.pkl", "rb"))
                        dico["fees"] = past_fees
                        pickle.dump(dico, open("data/data.pkl", "wb"))
        
        b_driver.stake_page()
        time.sleep(600 - (time.time() % 600)) # Executing every 10 minutes
    