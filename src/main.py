from bs import BS
from selenium import webdriver
import time, requests, json, pickle

version = "1.0.0"

def get_driver(OS="Windows"):
    if OS=="Windows":
        # Windows
        executable_list = [
            ("drivers/geckodriver-64.exe", webdriver.Firefox), 
            ("drivers/geckodriver-32.exe", webdriver.Firefox), 
            ("drivers/chromedriver91-32.exe", webdriver.Chrome),  
            ("drivers/chromedriver92-32.exe", webdriver.Chrome)
        ]
    elif OS=="Mac":
        # Mac
        executable_list = [
            ("drivers/chromedriver91-mac", webdriver.Chrome),
            ("drivers/geckodriver-mac", webdriver.Firefox),
            ("drivers/chromedriver92-mac64", webdriver.Chrome),
            ("drivers/chromedriver91-macm1", webdriver.Chrome),
            ("drivers/chromedriver92-macm1", webdriver.Chrome),
        ]
    else:
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

def log(message):
    print("====================")
    print(message)
    print("====================")

log(f"Welcome to AutoStake {version} --- https://tttienthinh.github.io/AutoStake/")
OS = input("Which OS are you using [Windows/Mac/Linux] ? :")
ok, driver = get_driver(OS)
ip = "main"

if not ok:
    input("Please install Firefox (geckodriver) or Chrome (chromedriver) and download drivers/")
else:
    # Connection
    b_driver = BS(driver)
    input("Enter when login is done : ")

    ans = input("Would you like to make a donation ? [y/n] : ")
    if ans.upper() == "Y":
        # Donation
        try:
            b_driver.donation(0, ip, "tranthuongtienthinh@gmail.com")
        except:
            pass
        input(f"Click Enter when is done : ")
    # Staking tokens
    b_driver.stake_page()
    tokens = json.load(open("data/tokens.json", "r"))
    log(tokens)
    ans = input("Would you like to continue staking this ? [y/n] : ")
    if ans.upper() != "Y":
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
        json.dump(tokens, open("data/tokens.json", "w"))
    log(f"I will look to stake every 10 minutes, don't close the console \n {tokens}")

    # Searching
    past_result = []
    while True:
        print(time.asctime())
        result = binance()
        new_result = []
        for data in result:
            new_result.append(data)
            if data not in past_result:
                asset = data['asset']
                duration = data['duration']
                apy = data['APY']
                print(f"Found new release     {asset} {duration} days {apy}% APY")
                
                if {'TOKEN': asset, 'DAYS': duration} in tokens:
                    lock_amount, amount, fees = b_driver.stake(asset, duration)
                    log(f"Staked Successfully {lock_amount} {asset}!")
        past_result = new_result
        b_driver.stake_page()
        time.sleep(600 - (time.time() % 600)) # Executing every 10 minutes
        