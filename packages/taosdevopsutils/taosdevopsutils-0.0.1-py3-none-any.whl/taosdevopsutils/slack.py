import slack
import os
from taosdevopsutils import config
import requests


class Slack:
    def __init__(self, token=config.SLACK_API_TOKEN):
        self.client = slack.WebClient(token=token)

    def _handle_webhook(self, target: str, message: str):
        return requests.post(
            target, data=message, headers={"Content-Type": "application/json"}
        )

    def _handle_direct_message(self, target: str, message: str):
        return self.client.chat_postMessage(channel=target, text=message, as_user=True)

    def post_slack_message(self, target: str, message: str):
        if target.startswith("https://"):
            return self._handle_webhook(target, message)
        return self._handle_direct_message(target, message)
