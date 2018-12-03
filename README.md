# CS Pound Discord Bot

[![Discord.py Rewrite](https://img.shields.io/badge/discord.py-rewrite-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/haruyuki/CS-Pound.svg)](https://github.com/haruyuki/CS-Pound/blob/master/LICENSE)
[![Discord Server](https://img.shields.io/discord/409642350600781824.svg?logo=discord)](https://invite.gg/cspound)

A Discord bot for the virtual pet adoption website [Chicken Smoothie](https://www.chickensmoothie.com). With this bot you can view information on pets and pound opening times straight from Discord without accessing the website.

## Features

| Command       | Description                                                               | Example                                                                       |
|-------------  |-------------------------------------------------------------------------  |---------------------------------------------------------------------------    |
| ,autoremind   | Setup an autoreminder for when the pound opens                            | ,autoremind 5m                                                                |
| ,giveaway     | Create a giveaway                                                         | ,giveaway 10m 5w 10 pets from my non-existent group.                          |
| ,help         | Displays the help message of all or a specific command.                   | ,help autoremind    OR  ,help                                                 |
| ,image        | Displays the pet as you would see it in "My Pets" group                   | ,image <http://www.chickensmoothie.com/viewpet.php?id=54685939>               |
| ,oekaki       | Displays Oekaki drawing from the link                                     | ,oekaki <http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993>   |
| ,pet          | Displays information about the pet from the link                          | ,pet <http://www.chickensmoothie.com/viewpet.php?id=54685939>                 |
| ,remindme     | Pings you after specified amount of time. Maximum reminding time is 24h   | ,remindme 1h6m23s<br>,remindme 12m<br>,remindme 1h10s                         |
| ,statistics   | Displays CS Pound bot statistics                                          | ,statistics                                                                   |
| ,support      | PM's you the link to the CS Pound Development Server                      | ,support                                                                      |
| ,time         | Tells you how long before the pound opens                                 | ,time                                                                         |

## Prerequisites

* Python 3.6 and above.
* A [Discord](https://discordapp.com) account.
* Though not required, a [Chicken Smoothie](https://www.chickensmoothie.com) account is highly recommended.
* The [Verdana](https://docs.microsoft.com/en-us/typography/font-list/verdana) font family.

## Installation
* Install all Python requirements using: `pip install -r requirements.txt`.
* Set environment variables as used in constants.py

## Running

To start the bot run the following command:
```bash
python3 cs_pound.py
```

## Contributors

* [**@ev-ev**](https://github.com/ev-ev) -> Edited README.md
* [**@Zenrac**](https://github.com/Zenrac) -> Code optimisations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Development Status
[![Build Status](https://img.shields.io/travis/com/haruyuki/CS-Pound.svg)](https://travis-ci.com/haruyuki/CS-Pound)
[![Coverage Status](https://img.shields.io/codecov/c/github/haruyuki/CS-Pound.svg)](https://codecov.io/gh/haruyuki/CS-Pound)
[![Requirements Status](https://img.shields.io/requires/github/haruyuki/CS-Pound.svg)](https://requires.io/github/haruyuki/CS-Pound/requirements/?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b67c35ebe69c4f308c521d3e9bf397a4)](https://www.codacy.com/app/haruyuki/CS-Pound)
[![Maintainability](https://api.codeclimate.com/v1/badges/e1711e225711d4f33ec7/maintainability)](https://codeclimate.com/github/haruyuki/CS-Pound/maintainability)