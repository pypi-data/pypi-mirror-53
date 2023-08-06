import requests


class Webhook:
    """This is a class to send messages via a Discord Webhook.

    Attributes:
        discord_endpoint (string): Discord's Webhook API Endpoint
    """
    global discord_endpoint
    discord_endpoint = "https://discordapp.com/api/webhooks"

    def __init__(self, url=None, channel_id=None, token=None):
        """The constructor for Webhook class.

        Parameters:
            url (string): Webhook URL from Discord.
            channel_id (string): Webhook channel_id taken from Webhook URL.
            token (string): webhook token taken from Webhook URL.

            *REQUIRES* url or channel_id and token to be set.

        Instance Attributes:
            embeds (list): Embed objects to be included in Discord message.
            channel_id (string): Channel ID of the Discord Webhook.
            token (string): Token of the Discord Webhook.
        """
        # Sets embeds to use with embeds() call
        self.embeds = []

        # Ensures variables are not None
        if not url and not all([channel_id, token]):

            raise TypeError(
                "Missing required arguments: 'url' or 'channel_id' & 'token'"
            )

        # Use channel_id and token over URL
        if all([channel_id, token]):

            url = None

            self.channel_id = str(channel_id)
            self.token = str(token)

        # Use URL if populated
        if url is not None:

            self.channel_id = url.split("/")[5]
            self.token = url.split("/")[6]

        # Validates Webhook Authorization
        response = requests.get(
            f"{ discord_endpoint }/{ self.channel_id }/{ self.token }"
        )

        if response.status_code != 200:

            message = response.json()["message"]

            raise ValueError(f"Webhook authorization error: { message }")

    def message(self, content=None, username=None, avatar_url=None, tts=False):
        """Generates the message JSON for the Discord Webhook.

        Parameters:
            content (string): Message content sent through Discord Webhook.
            username (string): Username to override the Discord Webhook name.
            avatar_url (string): URL to override the Discord Webhook Avatar.
            tts (boolean): True/False execution of Text-to-Speech message.

        Instance Attributes:
            content (string): Message content sent through Discord Webhook.
            username (string): Username to override the Discord Webhook name.
            avatar_url (string): URL to override the Discord Webhook Avatar.
            tts (boolean): True/False execution of Text-to-Speech message.
        """
        self.content = None if content is None else str(content)
        self.username = None if username is None else str(username)
        self.avatar_url = None if avatar_url is None else str(avatar_url)
        self.tts = True if tts is True else False

    def embed(self, title=None, description=None, url=None, color=None):
        """Adds a Discord embed object to the message.

        Parameters:
            title (string): Text set as the embed object title.
            description (string): Text set as the embed object description.
            url (string): URL the embed object links too.
            color (int - hex): Specifies color to send along embed object.

        Instance Attributes:
            embeds (list): Embed objects to be included in Discord message.
        """
        json = {}

        json["title"] = None if title is None else str(title)
        json["description"] = None if description is None else str(description)
        json["url"] = None if url is None else str(url)
        json["color"] = None if color is None else int(color, 16)

        self.embeds.append(json)

    def execute(self, wait=False):
        """Executes the Discord Webhook via a POST.

        Parameters:
            wait (boolean): .

        Returns:
            requests.post object.

        Instance Attributes:
            channel_id (string): Channel ID of the Discord Webhook.
            token (string): Token of the Discord Webhook.
            content (string): Message content sent through Discord Webhook.
            username (string): Username to override the Discord Webhook name.
            avatar_url (string): URL to override the Discord Webhook Avatar.
            tts (boolean): True/False execution of Text-to-Speech message.
            embeds (list): Embed objects to be included in Discord message.
        """
        # Call Parameters
        url = f"{ discord_endpoint }/{ self.channel_id }/{ self.token }"
        header = {"Content-Type": "application/json"}

        json_data = {}

        # Checks to see if message() has been called
        try:

            json_data["content"] = self.content
            json_data["username"] = self.username
            json_data["avatar_url"] = self.avatar_url
            json_data["tts"] = self.tts

        except AttributeError:

            self.message()

        # If self.content and self.embeds not set
        if all((self.content is None, len(self.embeds) == 0)):

            raise TypeError(
                "Missing required arguments: 'content' or 'embeds'"
            )

        if len(self.embeds) > 0:

            json_data["embeds"] = self.embeds

        url = f"{ url }?wait=true" if wait is True else url

        return requests.post(url, headers=header, json=json_data)

    def clear(self):
        """Clears all Instance Attributes.

        Parameters:
            None

        Instance Attributes:
            embeds (list): Embed objects to be included in Discord message.
        """
        # Resets self.embends
        self.embeds = []

        # Sets message to None
        self.message()
