import time
import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime
from email.message import EmailMessage


# Setting the Maximum and Minimum wanted rates to inform.
MAX_RATE = 3.7
MIN_RATE = 3.5

# Setting the address of the recipient
RECIPENT = "kfirim1@gmail.com"


# This method receives the rate value, the address of the recipient, and the index wether there was a rise or drop
# then sends the email.
def email_send(rate,emailaddress, index):
    EMAIL_ADDRESS = 'malkanbot@gmail.com'
    EMAIL_PASSWORD = 'ela10raanana'
    msgcontent = "Hello, the current dollar rate is: " + rate +" Shekels.\n"
    msg = EmailMessage()
    msg.set_content(msgcontent)
    msg['Subject'] = index+'the Dollar-Shekel rate is '+rate
    msg['From'] = "malkanbot@gmail.com"
    msg['To'] = emailaddress
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

# Pulling the rate value from the web.
def get_Rate():
    page = requests.get("https://fx-rate.net/USD/ILS/")
    print(page.status_code)
    while page.status_code!=200:
        page = requests.get("https://fx-rate.net/USD/ILS/")
    soup = BeautifulSoup(page.content, 'html.parser')
    today = soup.find(id="pair_today")
    pair_today = today.find_all(class_="left_block")
    coin = pair_today[0]
    exact = coin.find(class_="tpl_box").get_text()
    exact = exact.split(" ")
    rate = exact[4]
    print(rate)
    return rate

prev_rate=0
# This loop is running twice a day, receiving the current rate and comparing it's value to the Maximum rate and
# the Minimum rate that we settled.
while True:
    rate = get_Rate()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    if (float(prev_rate)!=0):
        if (float(prev_rate)>=MAX_RATE and float(rate)>=MAX_RATE):
            continue
        elif (float(prev_rate) <= MIN_RATE and float(rate) <= MIN_RATE):
            continue

    if (float(rate)>=MAX_RATE):
        email_send(rate,"amit.malkan@gmail.com","Exchange rise! ")
    if (float(rate)<=MIN_RATE):
        email_send(rate, RECIPENT, "Exchange drop! ")

    prev_rate=rate
    time.sleep(43200)
