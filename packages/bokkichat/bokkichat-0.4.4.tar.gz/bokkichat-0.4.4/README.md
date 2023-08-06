# bokkichat
|master|develop|
|:----:|:-----:|
|[![build status](https://gitlab.namibsun.net/namibsun/python/bokkichat/badges/master/build.svg)](https://gitlab.namibsun.net/namibsun/python/bokkichat/commits/master)|[![build status](https://gitlab.namibsun.net/namibsun/python/bokkichat/badges/develop/build.svg)](https://gitlab.namibsun.net/namibsun/python/bokkichat/commits/develop)|

![Logo](resources/logo/logo-readme.png)

Bokkichat is a python library that offers unified interfaces for interacting
with different chat services.

As an example, it could be used to write a bot for both Whatsapp and Telegram
without many service-specific alterations.

A project that extends this idea is
[kudubot](http://gitlab.namibsun.net/namibsun/python/kudubot).

# Implemented Connection Types

Currently the following connection types are supported out of the box:

* CLI
* Telegram (Bot)

# Installation

Installing bokkichat is as simple as running ```pip install bokkichat```, or
```python setup.py install``` when installing from source.

# Usage

First, you'll need to initialize the correct Settings object, which can then be
used to initialize the Connection.

```python
from bokkichat.settings.impl.TelegramBotSettings import TelegramBotSettings
from bokkichat.connection.impl.TelegramBotConnection import TelegramBotConnection

settings = TelegramBotSettings("APIKEY")
connection = TelegramBotConnection(settings)
```

Afterwards, you can send, receive and loop using the Connection object.

Some examples:

```python
# Sending a message
from bokkichat.settings.impl.TelegramBotSettings import TelegramBotSettings
from bokkichat.connection.impl.TelegramBotConnection import TelegramBotConnection
from bokkichat.entities.message.TextMessage import TextMessage
from bokkichat.entities.Address import Address

settings = TelegramBotSettings("APIKEY")
connection = TelegramBotConnection(settings)

receiver = Address("12345678")
msg = TextMessage(connection.address, receiver, "BODY", "TITLE")

connection.send(msg)
```

```python
# Echo every received message
from bokkichat.settings.impl.TelegramBotSettings import TelegramBotSettings
from bokkichat.connection.impl.TelegramBotConnection import TelegramBotConnection
from bokkichat.connection.Connection import Connection
from bokkichat.entities.message.Message import Message

settings = TelegramBotSettings("APIKEY")
connection = TelegramBotConnection(settings)


def echo(con: Connection, msg: Message):
    reply = msg.make_reply()
    con.send(reply)

connection.loop(echo)
```

# Implementing your own connection type

If the connection type you want to use is not implemented by bokkichat itself,
you can always implement it yourself. To do so, you will need to implement two
classes.

First off, you'll need to implement a subclass of the ```Settings``` class
and implement its abstract methods. Take a look at the implementation of 
various Settings classes
[here](bokkichat/settings/impl)
for some inspiration.

The Settings class defines the authentication information required for the
bot to function.

Afterwards, a subclass of the ```Connection``` class must be implemented.
Again, implement the abstract methods and let yourself be inspired by
[previous implementations](bokkichat/connection/impl)

The Connection class defines how to communicate with the service itself.

These two classes define everything that's needed for a bokkichat connection.

## Further Information

* [Changelog](CHANGELOG)
* [License (GPLv3)](LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namibsun/python/bokkichat)
* [Github](https://github.com/namboy94/bokkichat)
* [Progstats](https://progstats.namibsun.net/projects/bokkichat)
* [PyPi](https://pypi.org/project/bokkichat)
