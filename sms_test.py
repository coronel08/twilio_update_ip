from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import os

# environment variables for the scripts
load_dotenv(find_dotenv())
account_sid = os.environ.get("twilio_sid")
auth_token = os.environ.get("twilio_token")
client = Client(account_sid, auth_token)
fidel_phone = '+13236333898'
twilio_phone = '+13236224366'


def send_text(body='test'):
    """ 
    Sends a text message to me, if nothing is passed in function it will send test
    """
    message = client.messages.create(
        to=fidel_phone,
        from_=twilio_phone,
        body=body
    )
    print(message.sid, message.to, message.body)


def fetch_messages():
    """ 
    Fetches the last 30 text messages, before 2021
    """
    # can add filter like from_= , to= , date_sent=datetime(2021,1,1,0,0,0) , date_sent_after=datetime()
    messages = client.messages.list(
        date_sent_before=datetime(2021, 1, 1, 0, 0, 0), limit=30)
    for record in messages:
        print(record.sid, '\n', record.to, record.body, '\n')
    # Fetch messages by id
    # message = client.messages('MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX').fetch()


def start_conversation():
    """ Create a conversation and return conversation_sid """
    conversation = client.conversations \
        .conversations  \
        .create(friendly_name='My First Conversation')
    print(conversation.sid)


def fetch_conversation(conversation_sid):
    """ Fetch the conversation using sid and return conversation_service """
    conversation = client.conversations \
        .conversations(conversation_sid) \
        .fetch()
    print(conversation.chat_service_sid)


def add_conversation(conversation_sid):
    participant = client.conversations \
        .conversations(conversation_sid) \
        .participants \
        .create(
            messaging_binding_address=fidel_phone,
            messaging_binding_proxy_address=twilio_phone
        )
    print(participant.sid)


# send_text("This is a test run")
# fetch_messages()


# start_conversation()
# from start conversation
conversation_sid = 'CHa58ccfd9e9a148cd91b32b2989f97bf9'
# from fetch conversation
conversation_service = 'ISe762ba9737c643c7993f602847ebe2d6'
# fetch_conversation(conversation_sid)
participant_sid = 'MB980856734004444b81b3ea640953d9e4'
add_conversation(conversation_sid)
