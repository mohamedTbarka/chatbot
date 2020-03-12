# Handles messages events
import json

import i18n
import requests

import chatbot
from chatbot import survey, order, response
from chatbot.care import Care
from chatbot.response import gen_nux_message
from vichychatbot.settings import PAGE_ACCESS_TOKEN

i18n.load_path.append('/chatbot/locales')


class Receive:

    def __init__(self, user, webhookevent):
        self.user = user
        self.webhookEvent = webhookevent

    def handle_message(self):
        event = self.webhookEvent
        try:
            if 'message' in event:
                message = event['message']
                if 'quick_reply' in message:
                    responses = self.handle_quick_reply
                elif 'attachments' in message:
                    responses = self.handle_attachment_message()
                elif 'text' in message:
                    responses = self.handle_text_message()
            elif 'postback' in event:
                responses = self.handle_postback()
            elif 'referral' in event:
                responses = self.handle_referral()
        except Exception as e:
            print('%s (%s)' % (e.message, type(e)))
            responses = {
                "text": "An error has occured: %s. We have been notified and will fix the issue shortly!" % type(e)
            }
        if isinstance(responses, list):
            delay = 0
            for response in responses:
                self.send_message(response, delay * 2000)
                ++delay
        else:
            self.send_message(responses)

    def handle_text_message(self):
        print("Received text: %s for %s" % (self.webhookEvent['message']['text'], self.user['psid']))
        greeting = self.first_entity(self.webhookEvent['message']['nlp'])
        message = self.webhookEvent['message']['text'].strip().lower()
        if greeting and greeting['confidence'] > 0.0 or 'start over' in message:
            res = gen_nux_message(self.user)
        elif message.isdigit():
            res = order.handle_payload('ORDER_NUMBER')
        elif '#' in message:
            res = survey.handle_payload('CSAT_SUGGESTION')
        elif i18n.t("care.help").lower() in message:
            care = Care(self.user, self.webhookEvent)
            res = care.handle_payload('CARE_HELP')
        else:
            res = [
                chatbot.response.gen_text(
                    i18n.t("fallback.any", kwargs={"message": self.webhookEvent['message']['text']})
                ),
                chatbot.response.gen_text(i18n.t("get_started.guidance")),
                chatbot.response.gen_quick_reply(i18n.t("get_started.help"), [
                    {
                        "title": i18n.t("menu.suggestion"),
                        "payload": "CURATION"
                    },
                    {
                        "title": i18n.t("menu.help"),
                        "payload": "CARE_HELP"
                    }
                ])
            ]
        return res

    def handle_attachment_message(self):
        attachment = self.webhookEvent['message']['attachments'][0]
        print("Received attachment: %s for %s" % (attachment, self.user['psi']))
        res = chatbot.response.gen_quick_reply(i18n.t("fallback.attachment"), [
            {
                "title": i18n.t("menu.help"),
                "payload": "CARE_HELP"
            },
            {
                "title": i18n.t("menu.start_over"),
                "payload": "GET_STARTED"
            }
        ])

        return res

    def handle_quick_reply(self):
        payload = self.webhookEvent['message']['quick_reply']['payload']
        return self.hadle_payload(payload)

    def handle_postback(self):
        postback = self.webhookEven['postback']
        # Check for the special Get Started with referral
        if 'referral' in postback and postback['referral']['type'] == "OPEN_THREAD":
            payload = postback['payload']['ref']
        else :
            payload = postback['payload']
        return self.handle_payload(payload.upper())

    def


    def first_entity(self, nlp, name):
        return nlp and nlp['entities'] and nlp['entities']['name'] and nlp['entities']['name'][0]


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
