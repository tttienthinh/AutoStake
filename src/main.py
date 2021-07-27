from bs import BS
from selenium import webdriver
import time, requests, json




b_driver = BS(
    webdriver.Firefox(executable_path="/home/tttienthinh/Documents/Programmation/Bash/StartupApp/driver/geckodriver"),
)


print("Hello World")
time.sleep(5)