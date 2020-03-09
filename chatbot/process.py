import json
import os
from pprint import pprint
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

length_limit = 640  # to be used to double-check in individual scraping functions
headline_limit = 5


def fox_news():
    url = "https://www.foxnews.com"
    res = requests.get(url)

    try:
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        headline_list = soup.select(".primary a")
        headline_list.pop(0)  # hacky fix to get rid of headlineless first item

        message_list = ["Fox News:"]
        for headline in headline_list[:headline_limit]:
            current_message = headline.getText() + "\n" + headline.get("href")
            if len(current_message) < length_limit:
                message_list.append(current_message)

        return message_list

    except Exception as exc:
        return ["There was a problem: %s" % (exc)]


def tech_news():
    url = "https://www.reuters.com/news/archive/technologyNews"
    res = requests.get(url)

    try:
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        headline_list = soup.select("div[class='story-content'] a")

        message_list = ["Technology news:"]
        for headline in headline_list[:headline_limit]:
            current_message = headline.getText().strip() + "\n" + urljoin(url, headline.get("href"))
            if len(current_message) < length_limit:
                message_list.append(current_message)

        return message_list

    except Exception as exc:
        return ["There was a problem: %s" % (exc)]


def wotd():
    url = "https://www.merriam-webster.com/word-of-the-day"
    res = requests.get(url)

    try:
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.select("title")[0].getText()
        definition_list = soup.select("div[class='wod-definition-container'] p")

        message_list = ["Word of the Day:"]
        message_list.append(title)
        for definition in definition_list:
            current_message = definition.getText().strip()
            if len(current_message) < length_limit:
                message_list.append(current_message)

        return message_list

    except Exception as exc:
        return ["There was a problem: %s" % (exc)]


'''
def reddit_python():
    url = "https://www.reddit.com/r/Python/"
    res = requests.get(url)
    try:
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        headline_list = soup.select()
'''



def process(my_command):
    command_to_info = {
        "fox news": {
            "function": fox_news,
            "description": "general news on foxnews.com"
        },
        "tech news": {
            "function": tech_news,
            "description": "technology news on reuters.com"
        },
        "wotd": {
            "function": wotd,
            "description": "word of the day on merriam-webster.com"
        },
    }

    if my_command in command_to_info:
        return command_to_info[my_command]["function"]()
    else:
        help_message = "Command not recognized. Type:"
        for command in command_to_info:
            help_message += "\n- '%s' for %s" % (command, command_to_info[command]["description"])

        return [help_message[i: i + length_limit] for i in range(0, len(help_message), length_limit)]


import sys

if __name__ == "__main__":
    args = sys.argvl
    if len(args) == 2:
        access_token = os.environ["FB_MESS_ACCESS_TOKEN"]
        post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % (access_token)
        fbid = os.environ["FB_MESS_ID"]

        message_list = process(args[1])

        for message in message_list:
            response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": message}})
            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
            print("Status:")
            pprint(status.json())


# Bonjour et bienvenue sur la page officielle de VICHY MAROC :)
# sélectionner une langue :
#
#
# def process(id, text):
#
