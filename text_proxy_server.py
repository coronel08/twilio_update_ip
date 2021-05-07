import re
from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import PRIVATE_NUMBER, TWILIO_NUMBER


def encode_message(msg, number):
    return "{}: {}".format(number, msg)


def decode_message(msg):
    """ Format the number to  E.164 format and return body """
    pattern = re.compile('\+\d*')
    number = pattern.match(msg).group()
    body = msg[len(number) + 1:]
    return body, number


def send_message(msg, number):
    response = MessagingResponse()
    response.message(msg, to=number, from_=TWILIO_NUMBER)
    return str(response)


app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    """ if From number is equal to private number send to  """
    from_number = request.form['From']
    msg_body = request.form['Body']
    print(from_number, '\n', msg_body)

    if from_number == PRIVATE_NUMBER:
        msg, to_number = decode_message(msg_body)
        return send_message(msg, to_number)
    else:
        msg = encode_message(msg_body, from_number)
        return send_message(msg, PRIVATE_NUMBER)


if __name__ == '__main__':
    app.run()
