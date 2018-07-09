import discord
import asyncio
import os



client = discord.Client()

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
    
    if message.content == "!help":
        msg = """
        commands:
        Hello - ...
        !sakamoto - sakamoto-san
        """
        await client.send_message(message.channel, msg)

    if message.content == "!sakamoto":
        await client.send_file(message.channel, "img/nichijou-sakamoto-san.jpg")


client.run(os.environ['TOKEN'])
