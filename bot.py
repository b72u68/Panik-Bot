# import libraries
import discord
import os
import sys
import configparser
import pathlib
from redditSubmissionScraper import redditSubmissionScraper


# supporting functions
def read_token():           # read token from token.init
    config = configparser.ConfigParser()
    config.read('discord_conf.ini')
    return config['DISCORD']['bot_token']


# discord bot token
client = discord.Client()
token = read_token()


# connect to server
@client.event
async def on_ready():
    print(f'[+] {client.user} has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Sending memes'))


# receive message from channel
@client.event
async def on_message(message):

    # channels name
    channels = ['bot_spam']
    
    # some default path/file
    default_memes_path = os.path.abspath('default_memes/')

    no_memes = discord.File(os.path.join(default_memes_path, 'no_memes.png'), filename='no_memes.png')
    panik = discord.File(os.path.join(default_memes_path, 'panik.png'), filename='panik.png')
    kalm = discord.File(os.path.join(default_memes_path, 'kalm.png'), filename='kalm.png')
    orange = discord.File(os.path.join(default_memes_path, 'orange.png'), filename='orange.png')
    lifegood = discord.File(os.path.join(default_memes_path, 'lifegood.png'), filename='lifegood.png')


    if str(message.channel) in channels:

        if message.author == client.user:   # avoid loop
            return

        # commands for channel
        guide = '''```Panik Bot Commands Guide
    \'!h\'                          get bot commands 
    \'!panik\'                      send Panik meme
    \'!kalm\'                       send Kalm meme
    \'!meme <subreddit>\'           send meme from subreddit
    \'!joke <subreddit>\'           send joke from subreddit
    \'!s <query>\'                  search for subreddits```'''
    
        commands = ['!h', '!', '!kalm', '!panik', '!meme', '!joke', '!s']
        
        if message.content.startswith('!') and message.content.split()[0] not in commands:  # check entered command
            await message.channel.send('`Invalid command.`')
            await message.channel.send(guide)
            return
   
        if message.content in ('!', '!h'):  # send command guide
            await message.channel.send(guide)
            return

        if message.content == '!panik':    # send panik meme
            await message.channel.send(file=panik)
            return

        if message.content == '!kalm':   # send kalm meme
            await message.channel.send(file=kalm)
            return

        # supporting function for commands !meme and !joke
        def check_sub(subreddit):   # check input subreddit
            r = redditSubmissionScraper(subreddit)
            return r.check_sub()

        if message.content.startswith('!meme'):     # send meme in /memes directory
            subreddit = message.content[len('!meme')+1:].strip()

            # return reddit submission image through its url
            def get_image(subreddit):   # download image in subreddit
                r = redditSubmissionScraper(subreddit)
                data = r.get_image()
                
                try:
                    url = data['url']

                    # log writing
                    with open('image_log.txt', 'a') as f:
                        f.write(f'{subreddit.lower()}   {url}\n')
                        f.close()

                    return data 

                except Exception as e:
                    print(f'[-] Error Occurred: {e}')
                    return None

            if not subreddit:
                subreddit = 'memes'
            else:
                if not check_sub(subreddit):
                    await message.channel.send('`Invalid subreddit.`')
                    await message.channel.send(file=panik)
                    return
            
            image_data = get_image(subreddit)
            
            if not image_data:
                await message.channel.send('`No image found in this subreddit.`')
                await message.channel.send(file=no_memes)
                return

            else:
                url, author = image_data['url'], image_data['author']
                await message.channel.send(f'{url}\n`Posted in r/{subreddit} by u/{author}`')
                return

        # return reddit submission title and content
        if message.content.startswith('!joke'):     # send jokes
            subreddit = message.content[len('!joke')+1:].strip()

            def get_content(subreddit):
                r = redditSubmissionScraper(subreddit)
                data = r.get_content()

                try:
                    url = data['url']

                    # log writing
                    with open('text_log.txt', 'a') as f:
                        f.write(f'{subreddit.lower()}   {url}\n')
                        f.close()

                    return data

                except Exception as e:
                    print(f'[-] Error Occurred: {e}')
                    return None

            if not subreddit:
                subreddit = 'jokes'
            else:
                if not check_sub(subreddit):
                    await message.channel.send('`Invalid subreddit.`')
                    await message.channel.send(file=panik)
                    return
                    
            data = get_content(subreddit)
            
            if not data:
                await message.channel.send('`No joke found in this subreddit.`')
                await message.channel.send(file=panik)
                return
            
            else:
                author, title, content = data['author'], data['title'], data['content']
                await message.channel.send(f'`Posted in r/{subreddit} by u/{author}`\n**{title}**\n\n{content}')
                return

        # return subreddits match with searched query
        if message.content.startswith('!s'):
            query = message.content[len('!s')+1:].strip().lower()
            results = redditSubmissionScraper().search_sub(query)

            if not query:
                await message.channel.send('`Invalid query`')
                await message.channel.send(file=orange)
                return

            else:
                return_string = ''

                for counter, subreddit in enumerate(results):
                    return_string += f'{counter}. {subreddit}\n'
                    counter += 1

                if not return_string:
                    await message.channel.send('`No subreddit found matches with the query.`')
                    await message.channel.send(file=lifegood)
                    return

                else:
                    await message.channel.send(f'```Subreddits match with query:\n{return_string}```') 
                    return


client.run(token)
