#https://www.twilio.com/docs/conversations/quickstart

from twilio.rest import Client
from datetime import datetime
import os
# environment variables for the scripts
from config import twilio_sid, twilio_token, PRIVATE_NUMBER, TWILIO_NUMBER
# Depreceated storing variables in dotenv, using config file for env variables
"""  
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
twilio_sid = os.environ.get("twilio_sid")
twilio_token = os.environ.get("twilio_token")
PRIVATE_NUMBER = os.environ.get("fidel_phone")
TWILIO_NUMBER = os.environ.get("twilio_phone")
"""

client = Client(twilio_sid, twilio_token)


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
            messaging_binding_address=PRIVATE_NUMBER,
            messaging_binding_proxy_address=TWILIO_NUMBER
        )
    print(participant.sid)


def chat_in_conversation(conversation_sid):
    participant = client.conversations \
        .conversations(conversation_sid) \
        .participants \
        .create(identity='testPine')
    print(participant.sid)


# fetch_messages()
# start_conversation()
conversation_sid = 'CHa58ccfd9e9a148cd91b32b2989f97bf9'  # from start_conversation
conversation_service = 'ISe762ba9737c643c7993f602847ebe2d6'  # from fetch_conversation
# fetch_conversation(conversation_sid)
# from add_conversation and chat_in_conversation
participant_sid = 'MB980856734004444b81b3ea640953d9e4'
# add_conversation(conversation_sid)
chat_in_conversation(conversation_sid)
