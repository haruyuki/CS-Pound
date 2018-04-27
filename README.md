# CS Pound Discord Bot

A Discord bot for the online virtual pet adopting website. With the bot you can view pet information and pound opening times straight in Discord without needing to access the website.

### Features

| Command | Description | Usage | Example |
|-------------|-------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------|
| ,image | Displays only the pet image from the given link | ,image <Pet Link> | ,image [http://www.chickensmoothie.com/viewpet.php?id=54685939](http://www.chickensmoothie.com/viewpet.php?id=54685939) |
| ,oekaki | Displays Oekaki drawing from the link | ,oekaki <Oekaki Link> | ,oekaki [http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993](http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993) |
| ,pet | Displays information about the pet from the link | ,pet <Pet Link> | ,pet [http://www.chickensmoothie.com/viewpet.php?id=54685939](http://www.chickensmoothie.com/viewpet.php?id=54685939) |
| ,pet2 | Displays a image of the pet and it's information | ,pet2 <Pet Link> | ,pet2 [http://www.chickensmoothie.com/viewpet.php?id=54685939](http://www.chickensmoothie.com/viewpet.php?id=54685939) |
| ,time | Tells you how long before the pound opens | ,time | ,time |
| ,remindme | Pings you after specified amount of time. Maximum reminding time is 24h | ,remindme <#h#m#s> | ,remindme 1h6m23s<br>,remindme 12m<br>,remindme 1h10s |
| ,help | Displays the help message of all or a specific command. | ,help [Command] | ,help remindme |
| ,support | PM's you the link to the CS Pound Development Server | ,support | ,support |
| ,statistics | Displays CS Pound bot statistics | ,statistics | ,statistics |

### Prerequitites

Though only tested on Python 3.5.2 and 3.6.5, it should work with any version of Python 3.

The libraries Discord.py, lxml, Pillow, psutil, PyImgur and Requests are required to run the Python script. These can be installed through Python PIP by running:
```
pip3 install discord lxml.html pillow psutil pyimgur requests
```

A Discord and Imgur account is also required.

### Running

To start the bot run the following command:
```
python3 cs-pound.py
```

## Built With

* Python 3.6.5
* Discord.py 0.16.12

## Authors

* **Oliver Lin** - [Chao](http://27.253.115.239:3000/chao)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* [Chicken Smoothie](http://www.chickensmoothie.com)
* [discord.py](https://github.com/Rapptz/discord.py)
* [DigitalOcean](https://www.digitalocean.com)