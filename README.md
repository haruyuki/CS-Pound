# CS Pound Discord Bot

[![Discord.py](https://img.shields.io/badge/discord.py-rewrite-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python 3.7](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/haruyuki/CS-Pound.svg)](https://github.com/haruyuki/CS-Pound/blob/master/LICENSE)

A Discord bot for the virtual pet adoption website [Chicken Smoothie](https://www.chickensmoothie.com). With this bot you can view information on pets and pound opening times straight from Discord without accessing the website.

## Features

| Command       | Description                                                                        | Example                                                                       |
|-------------  |----------------------------------------------------------------------------------  |---------------------------------------------------------------------------    |
| ,autoremind   | Setup an autoremind for when the pound opens                                       | ,autoremind 5m                                                                |
| ,cs           | Given an amount of C$, returns the equivalent amount in FR gems and treasure       | ,cs 100                                                                       |
| ,gems         | Given an amount of FR gems, returns the equivalent amount in treasure and C$       | ,gems 623<br>,fr 1                                                            |
| ,giveaway     | Create a giveaway                                                                  | ,giveaway 10m 5w 10 pets from my non-existent group.                          |
| ,help         | Displays the help message of all or a specific command.                            | ,help<br>,help autoremind                                                     |
| ,identify     | Tells you the archive page where a pet or item is located                          | ,identify <https://www.chickensmoothie.com/viewpet.php?id=109085729>          |
| ,image        | Displays the pet as you would see it in "My Pets" group                            | ,image <http://www.chickensmoothie.com/viewpet.php?id=54685939>               |
| ,invite       | Sends you a link to where you can invite CS Pound to your Discord server           | ,invite                                                                       |
| ,news         | Allows you to show or opt in to announcements on the Chicken Smoothie              | ,news on<br>,news off<br>,news latest                                         |
| ,pet          | Displays information about the pet from the link                                   | ,pet <http://www.chickensmoothie.com/viewpet.php?id=54685939>                 |
| ,poundpets    | Searches through the pound account for rare pets and display them all in an image  | ,poundpets<br>,poundpets get                                                  |
| ,remindme     | Pings you after specified amount of time. Maximum reminding time is 24h            | ,remindme 1h6m23s<br>,remindme 12m<br>,remindme 1h10s                         |
| ,statistics   | Displays CS Pound bot statistics                                                   | ,statistics                                                                   |
| ,support      | PM's you the link to the CS Pound Development Server                               | ,support                                                                      |
| ,time         | Tells you how long before the pound opens                                          | ,time                                                                         |
| ,treasure     | Given an amount of FR treasure, returns the equivalent amount in gems and C$       | ,treasure 752642<br>,tr 6463                                                  |

## Usage
I would prefer if you don't your run own instance of my bot, but rather use the already existing instance. Head to <https://haruyuki.moe/CS-Pound/> and click the button on the top right (or below the title if you're on mobile), to invite the bot to your server.

## Contributors

* [**@ev-ev**](https://github.com/ev-ev) -> Edited README.md
* [**@Zenrac**](https://github.com/Zenrac) -> Code optimisations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

All pet rarity images are property of [Chicken Smoothie](https://www.chickensmoothie.com).

## Development Status
[![Build Status](https://app.travis-ci.com/haruyuki/CS-Pound.svg?branch=master)](https://app.travis-ci.com/haruyuki/CS-Pound)
[![Coverage Status](https://img.shields.io/codecov/c/github/haruyuki/CS-Pound.svg)](https://codecov.io/gh/haruyuki/CS-Pound)
