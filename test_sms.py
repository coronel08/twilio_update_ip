from twilio.rest import Client
from datetime import datetime
import os
# environment variables for the scripts
from config import twilio_sid, twilio_token, PRIVATE_NUMBER
TWILIO_NUMBER = '+14243389831'

client = Client(twilio_sid, twilio_token)


def send_text(body='test from 424 twilio number'):
    """
    Sends a text message to me, if nothing is passed in function it will send test
    """
    message = client.messages.create(
        from_='+14243389831',
        to=PRIVATE_NUMBER,
        body=body
    )
    print(message.sid, message.to, message.body)


send_text()
