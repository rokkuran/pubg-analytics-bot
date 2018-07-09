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
    
    if message.content.startswith("!playerid"):
        try:
            username = message.content.replace("!playerid", "").strip()
            api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
            players = api.players().filter(player_names=[username])
            await client.send_message(message.channel, players[0].id)

        except Exception as e:
            await client.send_message(message.channel, e)

    if message.content.startswith("!lastmatchid"):
        try:
            username = message.content.replace("!lastmatchid", "").strip()
            api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
            players = api.players().filter(player_names=[username])
            last_match_id = players[0].matches[0].id
            await client.send_message(message.channel, last_match_id)

        except Exception as e:
            await client.send_message(message.channel, e)

    if message.content.startswith("!lastmatchinfo"):
        try:
            username = message.content.replace("!lastmatchinfo", "").strip()
            api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
            players = api.players().filter(player_names=[username])
            last_match_id = players[0].matches[0].id

            match = api.matches().get(last_match_id)
            
            a = {
                "game_mode": match.game_mode,
                "duration": match.game_mode,
                "map": match.map,
            } 

            await client.send_message(message.channel, a)

        except Exception as e:
            await client.send_message(message.channel, e)


client.run(os.environ['DISCORD_BOT_TOKEN'])
