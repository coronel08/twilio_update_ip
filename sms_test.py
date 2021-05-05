from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
account_sid = os.environ.get("twilio_sid")
auth_token = os.environ.get("twilio_token")

client = Client(account_sid, auth_token)

message = client.messages.create(
    to='+13236333898',
    from_='+13236224366',
    body='WTF is up Twilio/Python'
)

print(message.sid)