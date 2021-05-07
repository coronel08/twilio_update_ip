# twilio_update_ip
Python Script to update twilio inside, will add twilio script to get text messaging api going as well.

Replace the items in config_sample.py with your information to run the scripts
```
twilio_sid = 'XXXXXXXXXXXXX'
twilio_token = 'XXXXXXXXXXXX'
TWILIO_NUMBER = "+13236211111"
PRIVATE_NUMBER = "+13231113118"
```



[Messages api](https://www.twilio.com/docs/sms/api/message-resource#create-a-message-resource) show how to create, fetch, delete, or update a message


![](media.gif)

---
## Resources for Conversations
Creating [Conversation](https://www.twilio.com/docs/conversations/quickstart?code-sample=code-create-your-first-conversation&code-language=Node.js&code-sdk-version=3.x) and [Creating WhatsApp Conversations](https://www.twilio.com/docs/conversations/using-whatsapp-conversations)


Command to run in Twilio-CLI for section 
```
twilio token:chat --identity testPine --chat-service-sid ISe762ba9737c643c7993f602847ebe2d6 --profile lappy

```

Paste into ConversationApp.js in sandbox
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6InR3aWxpby1mcGE7dj0xIn0.eyJqdGkiOiJTSzA5YWM1NzVjYWFhOTM4MDhkYTMyZTg4YmI2ZmUwNzJjLTE2MjAyNTgzNDYiLCJncmFudHMiOnsiaWRlbnRpdHkiOiJ0ZXN0UGluZSIsImNoYXQiOnsic2VydmljZV9zaWQiOiJJU2U3NjJiYTk3MzdjNjQzYzc5OTNmNjAyODQ3ZWJlMmQ2In19LCJpYXQiOjE2MjAyNTgzNDYsImV4cCI6MTYyMDI2MTk0NiwiaXNzIjoiU0swOWFjNTc1Y2FhYTkzODA4ZGEzMmU4OGJiNmZlMDcyYyIsInN1YiI6IkFDMjhkMGM0MmQzMGY2YzJiYTE1YzA5NGQyZDZiYjMwMTUifQ.jhQPnYhIRs2cXDbcixBF0NeeImflx1VZa_msVSNFLcY
```

---
## Creating a phone number proxy
Resources:
* [Phone number proxy script](https://www.twilio.com/blog/2018/02/phone-number-forward-mask-python-flask.html)
* [Github phone number proxy](https://github.com/npentrel/twilio-ghost)

Script is named ----

---
### Notes
Notes


---
### Todo
* Setup cron job to run update ip script
* [x] Setup Twilio CLI on server to process text messages and conversations on server. [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart)
  * [x] Create a WhatsApp business account for 1(323)622-4366
    * [ ] [autopilot whatsapp](https://www.twilio.com/docs/autopilot/channels/whatsapp) and [WhatsApp Senders](https://www.twilio.com/console/sms/whatsapp/senders) and [autopilot all](https://www.twilio.com/docs/autopilot/channels) 
* [x] Create a FB business manager account [FB Business](https://business.facebook.com/overview)
  * [ ] Learn and use WHatsApp Business and learn [WhatsApp API](https://www.twilio.com/docs/whatsapp/api)
* [ ] Update file names, clean up folder, update README.
