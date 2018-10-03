# CS Pound Discord Bot

[![Build Status](https://travis-ci.com/haruyuki/CS-Pound.svg?branch=master)](https://travis-ci.com/haruyuki/CS-Pound)
[![Coverage Status](https://coveralls.io/repos/github/haruyuki/CS-Pound/badge.svg?branch=master)](https://coveralls.io/github/haruyuki/CS-Pound?branch=master)
[![Requirements Status](https://requires.io/github/haruyuki/CS-Pound/requirements.svg?branch=master)](https://requires.io/github/haruyuki/CS-Pound/requirements/?branch=master)
[![Discord.py Rewrite](https://img.shields.io/badge/discord.py-rewrite-orange.svg)](https://github.com/Rapptz/discord.py)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/haruyuki/CS-Pound.svg)](https://github.com/haruyuki/CS-Pound/blob/master/LICENSE)
[![Discord Server](https://img.shields.io/discord/409642350600781824.svg?logo=discord)](https://invite.gg/cspound)

A Discord bot for the online virtual pet adopting website. With the bot you can view pet information and pound opening times straight in Discord without needing to access the website.

### Features

| Command       | Description                                                               | Example                                                                       |
|-------------  |-------------------------------------------------------------------------  |---------------------------------------------------------------------------    |
| ,autoremind   | Setup an autoreminder for when the pound opens                            | ,autoremind 5m                                                                |
| ,giveaway     | Create a giveaway                                                         | ,giveaway 10m 5w 10 pets from my non-existent group.                          |
| ,help         | Displays the help message of all or a specific command.                   | ,help autoremind                                                              |
| ,image        | Displays the pet as you would see it in "My Pets" group                   | ,image http://www.chickensmoothie.com/viewpet.php?id=54685939                 |
| ,oekaki       | Displays Oekaki drawing from the link                                     | ,oekaki http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993     |
| ,pet          | Displays information about the pet from the link                          | ,pet http://www.chickensmoothie.com/viewpet.php?id=54685939                   |
| ,remindme     | Pings you after specified amount of time. Maximum reminding time is 24h   | ,remindme 1h6m23s<br>,remindme 12m<br>,remindme 1h10s                         |
| ,statistics   | Displays CS Pound bot statistics                                          | ,statistics                                                                   |
| ,support      | PM's you the link to the CS Pound Development Server                      | ,support                                                                      |
| ,time         | Tells you how long before the pound opens                                 | ,time                                                                         |

### Prerequisites

* Python 3.6 and above.
* Install all Python requirements using: `pip install -r requirements.txt`.
* A [Discord](https://discordapp.com) account.
* Though not required, a [Chicken Smoothie](https://www.chickensmoothie.com) account is highly recommended.
* The [Verdana](https://docs.microsoft.com/en-us/typography/font-list/verdana) font family.

### Installation
Please refer to the wiki for [Server](https://github.com/Tesshin/CS-Pound/wiki/Server-Installation) or [User](https://github.com/Tesshin/CS-Pound/wiki/User-Installation) installation

### Running

To start the bot run the following command:
```bash
python cs-pound.py
```

## Built With

* [Python](https://www.python.org/downloads/release/python-370/) 3.7.0
* [Discord.py](https://pypi.org/project/discord.py/) 1.0.0a
* [lxml](https://pypi.org/project/lxml/) 4.2.3
* [Pillow](https://pypi.org/project/Pillow/) 5.2.0
* [psutil](https://pypi.org/project/psutil/) 5.4.6
* [uvloop](https://pypi.org/project/uvloop/) 0.11.0

## Authors

* [**@haruyuki**](https://github.com/haruyuki)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgements

* [Chicken Smoothie](http://www.chickensmoothie.com)
* [discord.py](https://github.com/Rapptz/discord.py)
* [DigitalOcean](https://www.digitalocean.com)
* [BlobGivingBot](https://github.com/BlobEmoji/blobgivingbot)
* [GiveawayBot](https://github.com/jagrosh/GiveawayBot)
