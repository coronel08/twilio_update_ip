import re
import requests
from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import PRIVATE_NUMBER, TWILIO_NUMBER, twilio_sid, twilio_token, twilio_api, api_key, TWIML_APP_SID
# Browser Calling dependencies
from dotenv import load_dotenv
import os
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from pprint import pprint

# Setting variables for Browser Calling
load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']
twiml_app_sid = os.environ['TWIML_APP_SID']
twilio_number = os.environ['TWILIO_NUMBER']


app = Flask(__name__)
client = Client(twilio_sid, twilio_token)
auth_token = twilio_token


# Route and functions for text proxy, handling incoming text and outgoing text from a twilio number
@app.route('/sms', methods=['POST'])
def sms():
    """ 
    If from_number is equal to PRIVATE_NUMBER, it sends the message to the number specified in the msg. 
    Else it forwards a message with the originating number and msg body to the PRIVATE_NUMBER 
    """
    from_number = request.form['From']
    msg_body = request.form['Body']
    print(from_number, '\n', msg_body)

    if from_number == PRIVATE_NUMBER:
        msg, to_number = decode_message(msg_body)
        return send_message(msg, to_number)
    else:
        msg = encode_message(msg_body, from_number)
        return send_message(msg, PRIVATE_NUMBER)


def encode_message(msg, number):
    """If number is not from PRIVATE_NUMBER it creates a message with the originating number and the msg, then forwards it to the PRIVATE_NUMBER """
    return "{}: {}".format(number, msg)


def decode_message(msg):
    """ If message came from PRIVATE NUMBER, take the phone number passed through the message and seperate it from the message body.  """
    pattern = re.compile('\+\d*')
    number = pattern.match(msg).group()
    body = msg[len(number) + 1:]
    return body, number


def send_message(msg, number):
    """ Sends message from TWILIO_NUMBER to number passed in """
    response = MessagingResponse()
    response.message(msg, to=number, from_=TWILIO_NUMBER)
    return str(response)


# Route and functions for recording calls coming in
@app.route("/record", methods=['POST'])
def record():
    """ Record messages coming in """
    response = VoiceResponse()
    if 'RecordingSid' not in request.form:
        response.say("Hello, please leave your message ")
        # access thru twilio api https://www.twilio.com/docs/voice/api/recording-transcription
        response.record(transcribe=True)
    else:
        print("Hanging up")
        response.hangup()
    return str(response)


def message():
    transcription = client.transcriptions.list(limit=1)
    sid = transcription[0].sid
    t = client.transcriptions(sid).fetch()
    print(t.transcription_text)
    return str(sid)


# Route and functions for a chatbot
@app.route('/bot', methods=['POST'])
def bot():
    """ A chatbot feature that reads an incoming msg and finds a keyword, if keyword cat or quote, then it replies back"""
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = ("Error loading API")
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        msg.media('https://cataas.com/cat')
        responded = True
    elif not responded:
        msg.body('Send a quotes or cats in body, sorry')
    return str(resp)


# Route and functions for browser dialing
@app.route('/', methods=['GET'])
def home():
    """ serving the UI """
    return render_template(
        'home.html',
        title='In browser calls',
    )


@app.route('/token', methods=['GET'])
def get_token():
    """ Generating and returning access tokens to the client using config.py credentials """
    identity = TWILIO_NUMBER
    outgoing_application_sid = TWIML_APP_SID
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(
        account_sid, api_key, api_key_secret, identity=identity
    )

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True,
    )
    access_token.add_grant(voice_grant)

    response = jsonify(
        {'token': access_token.to_jwt().decode(), 'identity': identity})

    return response


@app.route('/handle_calls', methods=['POST'])
def call():
    """ Instructions for making and receiving calls """
    pprint(request.form)

    response = VoiceResponse()
    dial = Dial(callerId=TWILIO_NUMBER)

    if 'To' in request.form and request.form['To'] != TWILIO_NUMBER:
        print('outbound call')
        dial.number(request.form['To'])
        return str(response.append(dial))
    return ''


if __name__ == '__main__':
    app.run()
