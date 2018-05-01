# CS Pound Discord Bot

A Discord bot for the online virtual pet adopting website. With the bot you can view pet information and pound opening times straight in Discord without needing to access the website.

### Features

| Command       | Description                                                               | Example                                                                       |
|-------------  |-------------------------------------------------------------------------  |---------------------------------------------------------------------------    |
| ,image        | Displays only the pet image from the given link                           | ,image http://www.chickensmoothie.com/viewpet.php?id=54685939                 |
| ,oekaki       | Displays Oekaki drawing from the link                                     | ,oekaki http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993     |
| ,pet          | Displays information about the pet from the link                          | ,pet http://www.chickensmoothie.com/viewpet.php?id=54685939                   |
| ,pet2         | Displays a image of the pet and it's information                          | ,pet2 http://www.chickensmoothie.com/viewpet.php?id=54685939                  |
| ,time         | Tells you how long before the pound opens                                 | ,time                                                                         |
| ,remindme     | Pings you after specified amount of time. Maximum reminding time is 24h   | ,remindme 1h6m23s<br>,remindme 12m<br>,remindme 1h10s                         |
| ,help         | Displays the help message of all or a specific command.                   | ,help remindme                                                                |
| ,support      | PM's you the link to the CS Pound Development Server                      | ,support                                                                      |
| ,statistics   | Displays CS Pound bot statistics                                          | ,statistics                                                                   |

### Prerequitites

Though only tested on Python 3.5.2 and 3.6.5, it should work with any version of Python 3.

The libraries [discord.py](https://github.com/Rapptz/discord.py), [lxml](http://lxml.de), [Pillow](http://python-pillow.org), [psutil](https://github.com/giampaolo/psutil), [PyImgur](https://github.com/Damgaard/PyImgur) and [Requests](http://docs.python-requests.org/en/master/) are required to run the Python script. These can be installed through Python PIP by running:
```
pip3 install discord lxml.html pillow psutil pyimgur requests
```

A [Discord](https://discordapp.com) and [Imgur](https://imgur.com) account is also required.

### Running

To start the bot run the following command:
```python
python3 cs-pound.py
```

## Built With

* Python 3.6.5
* Discord.py 0.16.12
* lxml 4.2.1
* Pillow 5.1.0
* psutil 5.4.5
* PyImgur 0.6.0
* Requests 2.18.4

## Authors

* **Oliver Lin** - [Chao](http://27.253.115.239:3000/chao)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgements

* [Chicken Smoothie](http://www.chickensmoothie.com)
* [discord.py](https://github.com/Rapptz/discord.py)
* [DigitalOcean](https://www.digitalocean.com)