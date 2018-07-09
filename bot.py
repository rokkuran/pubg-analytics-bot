import discord
import asyncio
import os
import yaml

from common import Query



client = discord.Client()
responses = yaml.safe_load(open('config.yaml', 'rb'))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content == "Hello":
        await client.send_message(message.channel, "World")
    
    if message.content == "ni hao":
        await client.send_message(message.channel, "ni hao shon di!")
    
    if message.content == "!help":
        await client.send_message(message.channel, responses['help'])

    if message.content == "!sakamoto":
        await client.send_file(message.channel, "img/nichijou-sakamoto-san.jpg")

    if message.content.startswith("!lastmatchid"):
        username = ' '.join(message.content.split("!lastmatchid")[1:])
        query = Query()
        last_match_id = query.get_user_last_match_id(username)
        await client.send_message(message.channel, last_match_id)

client.run(os.environ['DISCORD_BOT_TOKEN'])
