from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import os

# environment variables for the scripts
load_dotenv(find_dotenv())
account_sid = os.environ.get("twilio_sid")
auth_token = os.environ.get("twilio_token")
client = Client(account_sid, auth_token)
PRIVATE_NUMBER = os.environ.get("fidel_phone")
TWILIO_NUMBER = os.environ.get("twilio_phone")


def send_text(body='test from 424 twilio number'):
    """
    Sends a text message to me, if nothing is passed in function it will send test
    """
    message = client.messages.create(
        from_='+14243389831',
        to=TWILIO_NUMBER,
        body=body
    )
    print(message.sid, message.to, message.body)

send_text()