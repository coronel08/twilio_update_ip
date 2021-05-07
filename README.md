# Twilio Scripts and Proxy NUmber 📱↔️👻↔️📱
A couple of python scripts to interact with Twilio. This was devised so that I dont have to get business calls clogging my personal phone. The text_proxy_server.py script will run a server that will receive text on a twilio phone number. Inbound text will be routed to a personal phone number and your reply back will be routed to look as if came from the twilio number. <br><br>

Use Cases:
* Temporary or International numbers 
* A burner phone number for drug transactions and darkweb at only $1 a month
* A seperate number from your personal phone number (my case)


<b>Example Convo</b>, note that you will need to use actual phone numbers in E.164 format such as +13231234567. Also when going from Personal # -> Twilio# your text back should start with the number of the person you want to text/customer:
<br>📱↔️👻↔️📱<br>
<b>Customer# -> Twilio#</b>: Hello I am looking for a quote on a new kitchen <br>
<b>Twilio# -> Personal</b>#: Customer#:"Hello I am looking for a quote on a new" <br>
<b>Personal# -> Twilio#</b>: Customer# Yes I can go ahead and schedule an estimate this week. <br><br>

You will need to have a twilio account, a phone number purchased, python, ngrok(a reverse proxy that creates a secure tunell from a public endpoint), and some elbow grease. See deployment section to see how to purchase a Twilio number and get going. <br><br>

---
## Table of Contents
* [Structure](#Structure) 
* [Getting Started](#getting-started)
  * [Deploy](#deploy)
* [Notes](#notes)
  * [Resources](#resources)
* [TO-DO](#todo)
<br><br>

---
## Structure
* config_sample.py : <b><i>rename file as config.py and replace the credentials with your information </b></i> to use, all the other scripts rely on the credentials from this
* test_sms.py : Testing out sending a text messages through twilio to myself, the first step in getting this going
* text_proxy_server.py : a server that will forward text back and forth between customers and my personal number so I dont have to give out my personal number. 
* update_ip.py : a script to update the ip address of the server in case it changes
* sms_conversation.py : A script to create conversations between two numbers, requires a server with twilio-cli installed source [Twilio Docs](https://www.twilio.com/docs/conversations/quickstart) 
<br><br>

---
## Getting Started

Sign up for a twilio account, [use my affiliate link to sign up and get $10](www.twilio.com/referral/T0noIv). Photo below shows how to [purchase a phone number](https://www.twilio.com/console/phone-numbers/search) in twilio
![](./pics/buy-number.gif)

Replace the items in config_sample.py with your information, the private number will be your personal phone number/cell phone <b> make sure to rename the file to config.py</b>. 
```
twilio_sid = 'XXXXXXXXXXXXX'
twilio_token = 'XXXXXXXXXXXX'
TWILIO_NUMBER = "+13236211111"
PRIVATE_NUMBER = "+13231113118"
```


### Deploy 
Create virtual environment, install dependencies, and Ngrok. Ngrok will expose localhost port 5000 to incoming requests, it will provide us with a html that we can use in Twilio. 
```
virtualenv venv
pip install -r requirements.txt
sudo snap install ngrok #install ngrok on linux, if not in linux google how to install ngrok
ngrok http 5000 #start ngrok to expose port 5000
```

Below is a photo of how your phone numbers webhook should look like for texting. [Click your number to check the webhooks](https://www.twilio.com/console/phone-numbers/incoming)
![](./pics/webhook-setup.png)

Now you can run the text_proxy_server.py


---
## Notes
Notes

[Messages api](https://www.twilio.com/docs/sms/api/message-resource#create-a-message-resource) show how to create, fetch, delete, or update a message


### Resources for Conversations
Creating [Conversation](https://www.twilio.com/docs/conversations/quickstart?code-sample=code-create-your-first-conversation&code-language=Node.js&code-sdk-version=3.x) and [Creating WhatsApp Conversations](https://www.twilio.com/docs/conversations/using-whatsapp-conversations)


Command to run in Twilio-CLI for section 
```
twilio token:chat --identity testPine --chat-service-sid ISe762ba9737c643c7993f602847ebe2d6 --profile lappy

```

Paste into ConversationApp.js in sandbox
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6InR3aWxpby1mcGE7dj0xIn0.eyJqdGkiOiJTSzA5YWM1NzVjYWFhOTM4MDhkYTMyZTg4YmI2ZmUwNzJjLTE2MjAyNTgzNDYiLCJncmFudHMiOnsiaWRlbnRpdHkiOiJ0ZXN0UGluZSIsImNoYXQiOnsic2VydmljZV9zaWQiOiJJU2U3NjJiYTk3MzdjNjQzYzc5OTNmNjAyODQ3ZWJlMmQ2In19LCJpYXQiOjE2MjAyNTgzNDYsImV4cCI6MTYyMDI2MTk0NiwiaXNzIjoiU0swOWFjNTc1Y2FhYTkzODA4ZGEzMmU4OGJiNmZlMDcyYyIsInN1YiI6IkFDMjhkMGM0MmQzMGY2YzJiYTE1YzA5NGQyZDZiYjMwMTUifQ.jhQPnYhIRs2cXDbcixBF0NeeImflx1VZa_msVSNFLcY
```

### Creating a phone number proxy
Resources:
* [Phone number proxy script flask](https://www.twilio.com/blog/2018/02/phone-number-forward-mask-python-flask.html) and [Github repo](https://github.com/npentrel/twilio-ghost)
* [Record phone calls flask](https://www.twilio.com/blog/transcribe-voice-message-twilio-python-flask)
---
## Todo
There is a lot that can be added to the functionality of these scripts such as automating responses or anything you can think of
* [ ] Add in browser calling [FLask Javascript in Browser Calling](https://www.twilio.com/blog/make-receive-phone-calls-browser-twilio-programmable-voice-python-javascript)
* [ ] Build a cahtbot with Whatsapp[Flask chatbot ](https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio)
* [ ] Upload to AWS
* [ ] Add video with text chat [React Video Chat Twilio](https://www.twilio.com/blog/open-source-video-chat-app-reactjs-conversations-api)
* [ ] Code out a only during work hours kind of thing 
* [ ] Automate Response for keywords
* [ ] Route several numbers, looki into using a dict for phone numbers.
* [ ] Setup cron job to run update ip script (don't need to do this now that i'm using aws)
* [x] Setup Twilio CLI on server to process text messages and conversations on server. [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart)
  * [x] Create a WhatsApp business account for 1(323)622-4366
    * [ ] [autopilot whatsapp](https://www.twilio.com/docs/autopilot/channels/whatsapp) and [WhatsApp Senders](https://www.twilio.com/console/sms/whatsapp/senders) and [autopilot all](https://www.twilio.com/docs/autopilot/channels) 
* [x] Create a FB business manager account [FB Business](https://business.facebook.com/overview)
  * [ ] Learn and use WHatsApp Business and learn [WhatsApp API](https://www.twilio.com/docs/whatsapp/api)
* [x] Update file names, clean up folder, update README.
* [x] Setup recording and voice transcription of incoming calls


* [] Email Support about Conversations
```
Rather than keeping the WhatsApp room separate from the chat or SMS rooms, Conversations brings it together, automatically proxying conversations between participants. Whether it’s a customer care scenario where agents and employees field inquiries over webchat, while consumers respond over SMS or WhatsApp, in-app chat, or a large online conversation paired with a video event (perhaps built within minutes with our Open Source ReactJS app), every participant can choose their preferred channel. 
```