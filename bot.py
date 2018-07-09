import discord
import asyncio
import os
import yaml

from pubg_python import PUBG, Shard

from common import Query



client = discord.Client()
RESPONSES = yaml.safe_load(open('responses.yaml', 'rb'))


def test(a):
    return "test function returned with arg={}".format(a)

def testargs(*args):
    return "testargs function returned with args={}".format(args)



commands_text_response = {
    "help": RESPONSES["help"],
    "test": test,
    "testargs": testargs,
}

commands_img_response = {
    "zonedist": "PLACEHOLDER",
}


def get_cmd(msg):
    return msg[1:].split()[0]

def get_cmd_args(msg):
    return msg[1:].split()[1:]

def process_cmd(msg):
    cmd = get_cmd(msg)
    if cmd in commands_text_response:
        
        args = get_cmd_args(msg)
        f = commands_text_response[cmd]
        
        if callable(f):
            if len(args) > 0:
                return f(*args)
            else:
                return None  # no arguments specified
        else:
            return f

    elif cmd in commands_img_response:
        pass



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content in RESPONSES:
        await client.send_message(message.channel, RESPONSES[message.content])

    if message.content.startswith("!"):
        response = process_cmd(message.content)
        await client.send_message(message.channel, response)
  
    # if message.content == "!help":
    #     await client.send_message(message.channel, RESPONSES['help'])

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
                "duration": match.duration,
                "map": match.map,
            } 

            await client.send_message(message.channel, a)

        except Exception as e:
            await client.send_message(message.channel, e)


client.run(os.environ['DISCORD_BOT_TOKEN'])
