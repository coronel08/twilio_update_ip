import re
import requests
from flask import Flask, request,render_template, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import NUMBERS, TWILIO_SID, TWILIO_TOKEN


app = Flask(__name__)
client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route('/sms', methods=['POST'])
def sms():
    """ 
    If from_number is equal to PRIVATE_NUMBER, it sends the message to the number specified in the msg. 
    Else it forwards a message with the originating number and msg body to the PRIVATE_NUMBER 
    """
    from_number = request.form['From']
    to_number = request.form['To']
    msg_body = request.form['Body']
    print(from_number, to_number, '\n', msg_body)


class TextProxy():
    """ Create a text proxy per number/client instance """

    def __init__(self, twilio_number, personal_number):
        self.twilio_number = twilio_number
        self.personal_number = personal_number
        # figure out
        # from_number = request.form['From']
        # to_number = request.form['To']
        # msg_body = request.form['Body']
        # print(from_number, to_number, '\n', msg_body)

    def routing(self):
        if from_number == self.personal_number:
            pass
        elif to_number == self.twilio_number:
            pass
        else:
            pass

    def encode_message(self, msg, number):
        """ Encode message from twilio number to number passed in"""
        return f"{number}: {msg}"

    def decode_message(self, msg):
        """ If message came from PRIVATE NUMBER, take the phone number passed through the message and seperate it from the message body.  """
        pattern = re.compile('\+\d*')
        number = pattern.match(msg).group()
        body = msg[len(number) + 1:]
        return body, number

    def send_message(self, msg, number, from_=''):
        """ Sends message from TWILIO_NUMBER to number passed in """
        response = MessagingResponse()
        response.message(msg, to=number, from_=from_)
        return str(response)


if __name__ == '__main__':
    app.run()
