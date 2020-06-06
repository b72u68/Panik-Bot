# Panik-Bot
A crappy Discord bot downloading memes from Reddit and sending them on Discord.\
(update) now can also send jokes.

### Instructions

- Python3 is required for discord.py library
- Required Python libs: praw, configparser, discord. Run `pip install -r requirements.txt` to install libraries
- Create Reddit app and edit keys in `reddit_conf.ini` in `.config` directory
- Create Discord Bot and edit token in `discord_conf.ini` in `.config` directory

### Usage

- Run the bot LOCALLY. This bot cannot be hosted on server
- Type `!help` or `!` to read the bot commands

### To-do List

- [ ] Subreddit filter (avoid NSFW subreddits)
- [x] Make the bot run on a hosted server
- [x] Make a list of subreddits with good memes (or jokes)
- [x] Find a better way to keep track of downloaded files
- [x] Handle photos from Imgur
- [x] Add new feature to send text from reddit submission
