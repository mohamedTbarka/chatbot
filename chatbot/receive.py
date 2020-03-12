# Handles messages events
import json

import requests

from vichychatbot.settings import PAGE_ACCESS_TOKEN


def handle_message(sender_psid, received_message):
    # check if the message contains text
    if 'text' in received_message:
        print('-------txt--------')
        # create the payload ofr a basic text message
        response = {
            "text": "You sent the message :" + received_message['text'] + ". Now send me an image !"
        }
    elif 'attachments' in received_message:
        # Gets the URL of the message attachment
        url = received_message['attachments'][0]['payload']['url']
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": url,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Yes!",
                                "payload": "yes",
                            },
                            {
                                "type": "postback",
                                "title": "No!",
                                "payload": "no",
                            }
                        ],
                    }]
                }
            }
        }
    call_send_api(sender_psid, response)

    # Handles messaging_postbacks events


def handle_postback(sender_psid, received_postback):
    payload = received_postback['payload']
    # Set the response based on the postback payload
    if payload == 'yes':
        response = {"text": "Thanks!"}
    elif payload == 'no':
        response = {"text": "Ooops, try sending another image."}
    call_send_api(sender_psid, response)


# Sends response messages via the Send API
def call_send_api(sender_psid, response):
    # construct the message body
    request_body = {
        "recipient": {
            "id": sender_psid
        },
        "message": response
    }

    uri = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % PAGE_ACCESS_TOKEN

    status = requests.post(uri, headers={'Content-Type': 'application/json'}, data=json.dumps(request_body))

    if status.ok:
        print('message sent !')
    else:
        print('unable to send message !')
