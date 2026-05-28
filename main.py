import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = os.environ.get("MY_LAT")
MY_LONG = os.environ.get("MY_LONG")

def is_iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 < iss_latitude < MY_LAT+5 and MY_LONG-5 < iss_longitude < MY_LONG+5:
        return True
    else:
        return False

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour

    if sunset <= current_hour <= sunrise:
        return True
    else:
        return False

def send_email():
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
    SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
    RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
    

    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=f"Subject: ISS\n\nLook up")

while True:
    time.sleep(360)
    if is_iss_above() and is_dark():
        send_email()
