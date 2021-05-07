import re
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import PRIVATE_NUMBER, TWILIO_NUMBER, twilio_sid, twilio_token


app = Flask(__name__)
client = Client(twilio_sid, twilio_token)


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


if __name__ == '__main__':
    app.run()
