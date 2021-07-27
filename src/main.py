print("hello World 0.0.1")

from bs import BS
from selenium import webdriver
import time, requests, json

with open("data/data.txt", "r+") as f:
    print(f.read())
    f.close()

# webdriver.Firefox(executable_path="drivers/geckodriver-64.exe")
# webdriver.Chrome(executable_path="drivers/chromedriver92-32.exe")
with open("data/data.txt", "a+") as f:
    f.write(f"{input()}\n")
    f.close()
