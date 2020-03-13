import json

import requests

from chatbot.facebook_settings import MESSAGES_URL, PAGE_ACCESS_TOKEN, HEADER


class GraphApi:
    @staticmethod
    def call_send_api(request_body):
        url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
        data = json.dumps(request_body)
        status = requests.post(url, headers=HEADER, data=data)
        return status

    def call_fba_events_api(self, sender_psid, event_name):
        pass
