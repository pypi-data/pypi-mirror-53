import requests


class Webhook:
    """This is a class to send messages via a Discord Webhook.
    """
    def __init__(self, url=None):
        """The constructor for Webhook class.

        Parameters:
            url (string): Slack App URL from Slack.

        Instance Attributes:
            url (string): Webhook URL from Slack
        """
        # Need to add verification of valid webhook
        if url is None:
            raise TypeError(
                "Missing required arguments: 'url' or 'channel_id' & 'token'"
            )

        self.url = url

    def message(self, content=None):
        """Generates the message JSON for the Slack Webhook.

        Parameters:
            content (string): Message content sent through Slack Webhook.

        Instance Attributes:
            content (string): Message content sent through Slack Webhook.
        """
        self.content = None if content is None else str(content)

    def execute(self):
        """Executes the Slack Webhook via a POST.

        Parameters:
            None

        Instance Attributes:
            url (string): Webhook URL from Slack
            content (string): Message ccontent sent through Slack webhook.
        """
        header = {"Content-Type": "application/json"}
        json_data = {}

        if self.content is not None:

            json_data["text"] = self.content

            return requests.post(self.url, headers=header, json=json_data)

        raise TypeError(
            "Missing required arguments: 'content'"
        )
