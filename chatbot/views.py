import json
import re
from pprint import pprint

import requests
from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from vichychatbot import settings

# def post_facebook_message(fbid, received_message):
#     access_token = settings.FACEBOOK_VERIFY_TOKEN
#     post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % (access_token)
#
#     message_list = process(received_message)
#
#     for message in message_list:
#         response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": message}})
#         status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
#         print("Status:")
#         pprint(status.json())


# LOGIC_RESPONSES = {
#     'start':
#         'dict_message_gallerie'
#     # quick reply
#     ,
#     'Start Chatting': [
#         'Comment pouvons-nous vous aider {{user name noun}} ?', 'Vous avez un problème de peau ?',
#         'Quel est votre problème ? '
#     ],
#     'une': [
#         "Acné", "Tâche de soleil ou cicatrices d'acné", "Points noirs et petits boutons", "Pores dilatés",
#         "Boutons de régles"
#     ],
# }

dict_message_quickreply = {
    'text': "Bonjour et bienvenue sur la page officielle de La Roche Posay MAROC séléctionner une langue : ",
    "quick_replies": [
        {
            "content_type": "text",
            "title": "fr",
            "payload": "",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/French_language_%28text%29.png"
        }, {
            "content_type": "text",
            "title": "ar",
            "payload": "",
            "image_url": "http://www.collegevedas.louisgermain34.com/wp-content/uploads/2016/09/Langue-Arabe-3.png"
        }
    ]
}

LOGIC_RESPONSES = {

    'hello': dict_message_quickreply,
    'fr': {
        'text': "Comment peux-t-on t'aider ?",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "Infos produits",
                "payload": "",
            }, {
                "content_type": "text",
                "title": "Diagnostic de peau",
                "payload": "",
                "image_url": "",
            }
        ]
    },
    'Infos produits': {
        'text': "Sélectionner une gamme:",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "NORMADERM",
                "payload": "",
            }, {
                "content_type": "text",
                "title": "AQUALIA THERMAL",
                "payload": "",
                "image_url": "",
            }
        ]
    },
    'NORMADERM': {
        'text': "sélectionner un produit:",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "NORMADERM anti-acné",
                "payload": "",
            }, {
                "content_type": "text",
                "title": "NORMADERM GEL 200 ml",
                "payload": "",
                "image_url": "",
            }, {
                "content_type": "text",
                "title": "NORMADERM GEL 400 ml",
                "payload": "",
                "image_url": "",
            }, {
                "content_type": "text",
                "title": "NORMADERM HYALUSPOT",
                "payload": "",
                "image_url": "",
            }, {
                "content_type": "text",
                "title": "NORMADERM 3 EN 1",
                "payload": "",
                "image_url": "",
            },
        ]
    },
    'NORMADERM anti-acné': {
        'text': "Prix conseillé: 210 DHS \n http://bit.ly/2FYBBcC",

    }, 'NORMADERM GEL 200 ml': {
        'text': "Prix conseillé: 189 DHS \n http://bit.ly/2CnQ10K",

    }, 'NORMADERM GEL 400 ml': {
        'text': "Prix conseillé: 279 DHS \n http://bit.ly/2DUgerH",

    }, 'NORMADERM HYALUSPOT': {
        'text': "Prix conseillé: 175 DH \n http://bit.ly/2FvEpwI",

    }, 'NORMADERM 3 EN 1': {
        'text': "Prix conseillé: 199 DH \n http://bit.ly/2Omk9lf",

    },
    'AQUALIA THERMAL': {
        'text': "Sélectionner un produit:",
        "quick_replies": [
            {
                "content_type": "text",
                "title": "A.T. crème réhydratante légère",
                "payload": "",
                "image_url": "",
            }, {
                "content_type": "text",
                "title": "A.T. crème réhydratante riche",
                "payload": "",
                "image_url": "",
            },
        ]
    }, 'A.T. crème réhydrata...': {
        'text': "Prix conseillé: 214 DHS \n http://bit.ly/2OLHM2L",

    }, 'A.T. crème réhydratante riche': {
        'text': "Prix conseillé: 214 DHS \n http://bit.ly/2SXAMmi",

    },
}

url_buttons = {
    "type": "web_url",
    "url": "<URL_TO_OPEN_IN_WEBVIEW>",
    "title": "<BUTTON_TEXT>",
}

post_back_button = {
    "type": "postback",
    "title": "<BUTTON_TEXT>",
    "payload": "<STRING_SENT_TO_WEBHOOK>"  # communicate with webhook
}

dict_message_buttons = {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "button",
            "text": "Need further assistance? Talk to a representative",
            "buttons": [
                {
                    "type": "postback",
                    "title": "choice1",
                    "payload": "no payload"
                }, {
                    "type": "postback",
                    "title": "choice2",
                    "payload": "payload2"
                }, {
                    "type": "web_url",
                    "title": "url3",
                    "payload": "payload3"
                }
            ]
        }
    }
}

# carousele

dict_message_gallerie = {
    # "text": joke_text,
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [
                {
                    "title": "Welcome!",
                    "image_url": "https://image.shutterstock.com/image-vector/vector-modern-phone-icon-bubble-600w-280094294.jpg",
                    "subtitle": "We have the right hat for everyone.",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://petersfancybrownhats.com/view?item=103",
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://petersfancybrownhats.com",
                            "title": "View Website"
                        }, {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                },
                {
                    "title": "Welcome!",
                    "image_url": "https://image.shutterstock.com/image-vector/vector-modern-phone-icon-bubble-600w-280094294.jpg",
                    "subtitle": "We have the right hat for everyone.",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://petersfancybrownhats.com/view?item=103",
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://petersfancybrownhats.com",
                            "title": "View Website"
                        }, {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                },
                {
                    "title": "Welcome!",
                    "image_url": "https://image.shutterstock.com/image-vector/vector-modern-phone-icon-bubble-600w-280094294.jpg",
                    "subtitle": "We have the right hat for everyone.",
                    "default_action": {
                        "type": "web_url",
                        "url": "https://petersfancybrownhats.com/view?item=103",
                        "webview_height_ratio": "tall",
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://petersfancybrownhats.com",
                            "title": "View Website"
                        }, {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }
            ]
        }
    }
}

# image
dict_message_image = {
    "attachment": {
        "type": "image",
        "payload": {
            "is_reusable": "true",
            "url": "https://image.shutterstock.com/image-vector/vector-modern-phone-icon-bubble-600w-280094294.jpg"
        }
    }
}


def post_facebook_message(fbid, recevied_message, request):
    access_token = settings.FACEBOOK_VERIFY_TOKEN
    post_message_url = "https://graph.facebook.com/v4.0/me/messages?access_token=%s" % access_token  # endpoint

    print('--------------received messages-------------------')
    print(recevied_message)
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    print('-----------tokens----------')
    print(tokens)
    msg = None

    # for token in tokens:
    if recevied_message in LOGIC_RESPONSES:
        # request.session['token'] = token
        # msg = random.choice(LOGIC_RESPONSES[token])  # logic to define access to dictionnary
        msg = LOGIC_RESPONSES[recevied_message]


    else:
        msg = "J'ai pas compris , veuillez entrer un choix valide !! "
        msg = {
            'text': "J'ai pas compris , veuillez entrer un choix valide !! ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Infos produits",
                    "payload": "",
                }, {
                    "content_type": "text",
                    "title": "Diagnostic de peau",
                    "payload": "",
                    "image_url": "",
                }
            ]
        }

    print('-----------message----------')
    print(msg)

    # response_msg1 = json.dumps({'recipient': {'id': fbid}, 'message': dict_message})

    msg = json.dumps({'recipient': {'id': fbid}, 'message': msg})
    status = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=msg)
    pprint(status.json())
    return status.json()

    # response_msg = json.dumps({'recipient': {'id': fbid}, 'message': dict_message_quickreply})
    # fbbotw.post_text_message(fbid=user_fbid, message=response_msg)

    # status = requests.post(
    #     post_message_url,
    #     headers={'Content-Type': 'application/json'},
    #     data=response_msg)
    #
    # # response_msg1 = json.dumps({'recipient': {'id': fbid}, 'message': dict_message})
    # # status = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=response_msg1)
    # pprint(status.json())
    # return status.json()


# Create your views here.
class Bot(generic.View):
    def get(self, request, *args, **kwargs):
        verify_token = settings.FACEBOOK_VERIFY_TOKEN
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token.')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        incomming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incomming_message['entry']:
            for message in entry['messaging']:
                print(message)
                if 'message' in message:
                    print("Message:")
                    pprint(message)
                    if 'text' in message['message']:
                        quick_replies = [
                            {
                                "content_type": "text",
                                "title": "Yes!",
                                "payload": "SEND_FORECAST"
                            },
                            {
                                "content_type": "text",
                                "title": "Nope",
                                "payload": "USER_SAY_NOT"
                            }
                        ]
                        # fbbotw.post_text_w_quickreplies(fbid=message['sender']['id'],
                        #                                 message=message['message']['text'], quick_replies=quick_replies)
                        #
                        # response = fbbotw.post_image_w_quickreplies(
                        #     fbid=message['sender']['id'],
                        #     image_url='https://i.ibb.co/p2XSb77/vf-peau-normal.png',
                        #     quick_replies=quick_replies
                        # )

                        # fbbotw.post_text_message(fbid=message['sender']['id'], message=message['message']['text'])
                        post_facebook_message(message['sender']['id'], message['message']['text'], request)

        return HttpResponse()
