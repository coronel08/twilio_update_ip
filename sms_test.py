from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import os

# environment variables for the scripts
load_dotenv(find_dotenv())
account_sid = os.environ.get("twilio_sid")
auth_token = os.environ.get("twilio_token")
client = Client(account_sid, auth_token)


def send_text(body='test'):
    """ 
    Sends a text message to me, if nothing is passed in function it will send test
    """
    message = client.messages.create(
        to='+13236333898',
        from_='+13236224366',
        body= body
    )
    print(message.sid, message.to, message.body)


def fetch_messages():
    """ 
    Fetches the last 30 text messages, before 2021
    """
    # can add filter like from_= , to= , date_sent=datetime(2021,1,1,0,0,0) , date_sent_after=datetime()
    messages = client.messages.list(date_sent_before=datetime(2021, 1, 1, 0, 0, 0),limit=30)
    for record in messages:
        print(record.sid, '\n', record.to, record.body, '\n')
    # Fetch messages by id
    # message = client.messages('MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX').fetch()


def start_conversation():
    conversation = client.conversations \
        .conversations  \
        .create(friendly_name='My First Conversation')
    print(conversation.sid)



# send_text("THis is a test run")
# fetch_messages()