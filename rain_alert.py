import os
import smtplib
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = os.environ.get("TWILIO_SID")  # add your twilio SID
auth_token = os.environ.get("AUTH_TOKEN")  # twilio auth_token
API_KEY = os.environ.get("OWM_API_KEY")  # open weather map API
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
MY_EMAIL = os.environ.get("EMAIL")  # your email
PASSWORD = os.environ.get("PASS")  # your email password
parameters = {
    "lat": -75.347841,  # a latitude of your address
    "lon": 12.253123,  # a longitude of your address
    "exclude": "daily,current",
    "appid": API_KEY,
}
response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False
for hourly_data in weather_slice:
    condition_code = hourly_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
client = Client(account_sid, auth_token, http_client=proxy_client)
if will_rain:
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="therecivermail@gmail.com",
                            msg="Subject: Weather forcast \n\n You might want to bring an "
                                "umbrella, or wear warm cloth, "
                                "it seems like it would rain")
    message = client.messages \
        .create(
        body="You might want to bring an umbrella, or wear warm cloth, it seems like it would rain (or at least)be cold",
        from_='+00000000',  # your twilio number
        to='+00000000'  # your number
    )
    print(message.status)
elif not will_rain:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="therecivermail@gmail.com", msg="Subject: Weather forcaset "
                                                                                            "\n\n You might want to"
                                                                                            " dress lighter")
    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    message = client.messages \
        .create(
        body="You might want to dress lighter",
        from_='+00000',  # Your twilio number
        to='+0000000'  # Your number
    )
    print(message.status)



