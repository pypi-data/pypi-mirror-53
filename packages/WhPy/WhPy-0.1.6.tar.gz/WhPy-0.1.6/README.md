# WhPy - Webhook Python

[![PyPI](https://img.shields.io/pypi/v/WhPy)](https://pypi.org/project/WhPy/)
[![PyPI - License](https://img.shields.io/pypi/l/WhPy)](https://pypi.org/project/WhPy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/WhPy)](https://pypi.org/project/WhPy/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/WhPy)](https://pypi.org/project/WhPy/)

Webhook Python is a Python 3 module for interacting with various chat applications via established webhooks.

## Installation

> pip install WhPy

## SHA256 CHECKSUMS

``` text
61e9e7c854a1f903b4805304e0c9522d5eebf8973fe0c19631b01e84937d9e70  WhPy/discord.py
2004c330f131d71e4f3556f2ce3b737208403789a8e30314d67c702805b43def  WhPy/__init__.py
0f0724f3bf27c1ef85faffd75cf8bfe75bc6931ecd00aa8ca568a6761e3112d3  WhPy/slack.py
```

## Code Examples

Hello, World!

``` python 3
from WhPy import discord

# Discord Webhook URL
webhook_url = "https://discordapp.com/api/webhooks/1234/567890"

# Creates Discord Instance
hook = discord.Webhook(url=webhook_url)

# Sets Message Content
hook.message(content="Hello, World!")

# Executes the Webhook
hook.execute()
```

Hello, World! from user `MichaelCduBois`

``` python 3
from WhPy import discord

# Discord Webhook Parameters
webhook_channel_id = "1234"
webhook_token = "567890"

# Creates Discord Instance
hook = discord.Webhook(channel_id=webhook_channel_id, token=webhook_token)

# Sets Message Content as MichaelCduBois
hook.message(content="Hello, World!", username="MichaelCduBois")

#Executes the Webhook
hook.execute()
```

Hello, World! Text-to-Speech Message

``` python 3
from WhPy import discord

# Discord Webhook URL
webhook_url = "https://discordapp.com/api/webhooks/1234/567890"

# Creats Discord Instance
hook = discord.webhook(url=webhook_url)

# Sets Message content as a Text-to-Speech Message
hook.message(content="Hello, World!", tts=True)

# Executes the Webhook
hook.execute()
```

Return message confirmation as JSON Object

``` python 3
from WhPy import discord

# Discord Webhook URL
webhook_url = "https://discordapp.com/api/webhooks/1234/567890"

# Creats Discord Instance
hook = discord.webhook(url=webhook_url)

# Sets Message Content
hook.message(content="Hello, World!")

# Executes the Webhook
hook.execute(wait=True)
```
