# static genQuickReply(text, quickReplies) {
#     let response = {
#       text: text,
#       quick_replies: []
#     };
#
#     for (let quickReply of quickReplies) {
#       response["quick_replies"].push({
#         content_type: "text",
#         title: quickReply["title"],
#         payload: quickReply["payload"]
#       });
#     }
#
#     return response;
#   }
import json


def gen_quick_reply(text, quickreplies):
    response = {
        "text": text,
        "quick_replies": []
    }
    for quickreplie in quickreplies:
        response['quick_replies'].append(
            {
                "content_type": "text",
                "title": quickreplie["title"],
                "payload": quickreplie["payload"]
            }
        )
    return response


def gen_generic_template(image_url, title, subtitle, buttons):
    response = {
        "attachment": {
            type: "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": title,
                        "subtitle": subtitle,
                        "image_url": image_url,
                        "buttons": buttons
                    }
                ]
            }
        }
    }

    return response


def gen_image_template(image_url, title, subtitle=''):
    response = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": title,
                        "subtitle": subtitle,
                        "image_url": image_url
                    }
                ]
            }
        }
    }

    return response


def gen_button_template(title, buttons):
    response = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": title,
                "buttons": buttons
            }
        }
    }
    return response


def gen_text(text):
    response = {
        "text": text
    }
    return response


def gen_text_with_persona(text, persona_id):
    response = {
        "text": text,
        "persona_id": persona_id
    }

    return response


def gen_post_back_button(title, payload):
    response = {
        "type": "postback",
        "title": title,
        "payload": payload
    }
    return response


def gen_web_url_button(title, url):
    response = {
        "type": "web_url",
        "title": title,
        "url": url,
        "messenger_extensions": True
    }
    return response


def gen_nux_message(user):
    json_data = open('/chatbot/en_US.json')
    locale = json.load(json_data)
    welcome = gen_text(locale['get_started']['welcome'])
    guide = gen_text(locale['get_started']['guidance'])
    curation = gen_quick_reply(locale['get_started']['help'], [
        {
            "title": locale['menu']['suggestion'],
            "payload": "CURATION"
        },
        {
            "title": locale['menu']['help'],
            "payload": "CARE_HELP"
        }
    ])
    json_data.close()
    return [welcome, guide, curation]
