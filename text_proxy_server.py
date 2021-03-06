import re
import requests
import os
from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import NUMBERS, TWILIO_SID, TWILIO_TOKEN, TWILIO_API, API_KEY, TWIML_APP_SID
from pyngrok import ngrok


app = Flask(__name__)
client = Client(TWILIO_SID, TWILIO_TOKEN)



'''
name_list = ["Fidel","Karina"]
number_list = [323,714]
text = "Mom text to someone out"

for i, j in enumerate(name_list):
    if j in text:
        print(f"{i}:{j} in text, return number {number_list[i]}")
    else:
        pass



#added twilio#, make a dict with two values zipped.
twilio_list = [987,876]
test = dict(zip(name_list,zip(number_list, twilio_list)))

'''


# Route and functions for text proxy, handling incoming text and outgoing text from a twilio number
@app.route('/sms', methods=['POST'])
def sms():
    """ 
    If from_number is equal to PRIVATE_NUMBER, it sends the message to the number specified in the msg. 
    Else it forwards a message with the originating number and msg body to the PRIVATE_NUMBER 
    """
    from_number = request.form['From']
    to_number = request.form['To']
    msg_body = request.form['Body']
    print(from_number, '\n', msg_body)

    if from_number == NUMBERS['PRIVATE_NUMBER']:
        # Text from my phone come out as 323 num
        msg, to_number = decode_message(msg_body)
        return send_message(msg, to_number)
    elif from_number == NUMBERS['MOM']:
        # Text from moms phone comes out as 424 num
        msg, to_number = decode_message(msg_body)
        return send_message(msg, to_number, from_=NUMBERS['SECOND_NUMBER'])
    elif to_number == NUMBERS['SECOND_NUMBER']:
        # Text coming to Twilio Second Number, # forwards to Mom
        msg = encode_message(msg_body, from_number)
        return send_message(msg, NUMBERS['MOM'], from_=NUMBERS['SECOND_NUMBER'])
    else:
        # Else forward all text to 323 numbers route.
        msg = encode_message(msg_body, from_number)
        return send_message(msg, NUMBERS['PRIVATE_NUMBER'])


def get_key(val, dict_name):
    """ 
    Function to return the key from a value in the dictionary
    https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    """
    for key, value in dict_name.items():
        if val == value:
            return key


def encode_message(msg, number):
    """If number is not from PRIVATE_NUMBER it creates a message with the originating number and the msg, then forwards it to the PRIVATE_NUMBER """
    return "{}: {}".format(number, msg)


def decode_message(msg):
    """ If message came from PRIVATE NUMBER, take the phone number passed through the message and seperate it from the message body.  """
    pattern = re.compile('\+\d*')
    number = pattern.match(msg).group()
    body = msg[len(number) + 1:]
    return body, number


def send_message(msg, number, from_=NUMBERS['TWILIO_NUMBER']):
    """ Sends message from TWILIO_NUMBER to number passed in """
    response = MessagingResponse()
    response.message(msg, to=number, from_=from_)
    return str(response)

# https://www.twilio.com/blog/automating-ngrok-python-twilio-applications-pyngrok
def start_ngrok():
    url = ngrok.connect(5000).public_url
    print('* Tunnel URL:', url + '/sms')

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


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()
    app.run()
