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

    if message.content.startswith("!username_split_test"):
        username = ' '.join(message.content.split("!username_split_test")[1:])

        await client.send_message(message.channel, username)
    
    if message.content.startswith("!test"):
        username = ' '.join(message.content.split("!test")[1:])

        try:
            api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)

            players = api.players().filter(player_names=[username])

            await client.send_message(message.channel, players)


            # sample = api.samples().get()
            # for match in sample.matches:   
            #     await client.send_message(message.channel, match.id)

        except Exception as e:
            await client.send_message(message.channel, e)


client.run(os.environ['DISCORD_BOT_TOKEN'])
