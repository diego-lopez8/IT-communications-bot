# main.py
# Author: Diego Lopez
# last updated: July 22, 2021
# Notes: THis file calls discord's api to connect and send messages to the server with connection to googles api

"""
TO IMPLEMENT:
- create a function to loop every 24 hours that updates the list to the correct sheet eg rooms are now reflecting the next day
- create a function that loops every 5 minutes to update deploy times
     -if demployment time is 30,15,5 minutes later, ping discord that the deployment is needed
- create a function that loops every 5 minutes (but different starting time than deploy function) to update check times
     -if check time is 30,15,5 minutes later and also past the earliest check time, ping discord that the checks is needed
"""

import os
import discord
from discord.ext import tasks
import time
from dotenv import load_dotenv
from gs import *

load_dotenv()
TOKEN             = os.getenv('DISCORD_TOKEN')
GUILD             = os.getenv('DISCORD_SERVER')
CHANNEL_ID        = int(os.getenv("CHANNEL_ID"))
intents           = discord.Intents.default()
intents.members   = True
intents.typing    = False
intents.presences = False
client            = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    """
    async for member in guild.fetch_members():
        print(member)
    """
    daily_deploy_update.start()

@tasks.loop(minutes=1)
async def daily_deploy_update():
    x = deploy_update_full()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"The classes for today, {date.today()} are as follows:\n")
    # logic to print just the rooms? 
    # This is run at the beginning of the day so obviously they wont be checked
    for elem in x:
        await channel.send(elem)

# what do we need before the loop?
@daily_deploy_update.before_loop
async def daily_update():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("...")    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ";help":
        await message.channel.send("...List commands")

client.run(TOKEN)
