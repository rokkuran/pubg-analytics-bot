import discord
import asyncio
import os
import yaml

# from common import Query
from pubg_python import PUBG, Shard



client = discord.Client()
responses = yaml.safe_load(open('responses.yaml', 'rb'))


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

        api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
        players = api.players().filter(player_names=[username])
        last_match_id = api.matches().get(players[0].matches[0].id)

        # query = Query()
        # last_match_id = query.get_user_last_match_id(username)

        # await client.send_message(message.channel, "processing lastmatchid query...")

        await client.send_message(message.channel, last_match_id)

client.run(os.environ['DISCORD_BOT_TOKEN'])
