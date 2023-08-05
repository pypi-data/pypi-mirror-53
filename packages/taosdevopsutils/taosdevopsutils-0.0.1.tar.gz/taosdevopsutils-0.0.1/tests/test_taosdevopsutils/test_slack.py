from unittest import TestCase
from taosdevopsutils.slack import Slack
import slack
import requests


class TestSlackClass:
    def test_slack_posts_http_when_given_webhook(self, mocker):
        slack_mock = mocker.patch.object(slack.WebClient, "chat_postMessage")
        requests_mock = mocker.patch.object(requests, "post")
        slack_client = Slack()
        slack_client.post_slack_message("https://slack/webhook/somehook", "SomeMessage")
        assert not slack_mock.called
        assert requests_mock.called

    def test_slack_posts_message_when_given_user_id(self, mocker):
        slack_mock = mocker.patch.object(slack.WebClient, "chat_postMessage")
        requests_mock = mocker.patch.object(requests, "post")
        slack_client = Slack()
        slack_client.post_slack_message("U123456", "SomeMessage")
        assert slack_mock.called
        assert not requests_mock.called
