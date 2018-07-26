# CS Pound Discord Bot

<a href="https://github.com/Rapptz/discord.py" alt="Discord.py Rewrite"><img src="https://img.shields.io/badge/discord.py-rewrite-orange.svg" /></a>
<a href="https://www.python.org/" alt="Python 3.6"><img src="https://img.shields.io/badge/python-3.6-blue.svg" /></a>
<a href="https://gitlab.com/Rowlie/cs-pound/blob/master/LICENSE" alt="MIT License"><img src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>

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

### Prerequitites

* Python 3.6 and above.
* Install all requirements using : `pip install -r requirements.txt`.
* A [Discord](https://discordapp.com) account.
* Though not required, a [Chicken Smoothie](https://www.chickensmoothie.com) account is essential as it's the purpose of the bot.
* The [Verdana](https://docs.microsoft.com/en-us/typography/font-list/verdana) font family.

### Installation
Create a text file called `tokens.txt` and paste in the bot token in the first line.

### Running

To start the bot run the following command:
```bash
python cs-pound.py
```

## Built With

* Python 3.6.6
* Discord.py 1.0.0a
* lxml 4.2.3
* Pillow 5.2.0
* psutil 5.4.6
* uvloop 0.11.0

## Authors

* **Oliver Lin** - [@Tesshin](https://github.com/Tesshin)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgements

* [Chicken Smoothie](http://www.chickensmoothie.com)
* [discord.py](https://github.com/Rapptz/discord.py)
* [DigitalOcean](https://www.digitalocean.com)
* [BlobGivingBot](https://github.com/BlobEmoji/blobgivingbot)
