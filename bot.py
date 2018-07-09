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

def get_last_match_id(username):
    api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
    players = api.players().filter(player_names=[username])
    return players[0].matches[0].id


commands_text_response = {
    "help": RESPONSES["help"],
    "test": test,
    "testargs": testargs,
    "lastmatchid": get_last_match_id,
}

commands_img_response = {
    "zonedist": "PLACEHOLDER",
    "sakamoto": "img/nichijou-sakamoto-san.jpg",
    "shimoneta": "https://i2.wp.com/snapthirty.com/wp-content/uploads/2017/08/shimoneta-screenshot-01.jpg?resize=700%2C394&ssl=1",
}


def get_cmd(msg):
    return msg[1:].split()[0]

def get_cmd_args(msg):
    return msg[1:].split()[1:]

def process_cmd(msg):
    """
    Returns: cmd_type, result
    """
    cmd = get_cmd(msg)
    result = None

    if cmd in commands_text_response:
        
        args = get_cmd_args(msg)
        f = commands_text_response[cmd]
        
        if callable(f):
            if len(args) > 0:
                result = f(*args)
                # return "text", f(*args)
            # else:
                # return "text", None  # no arguments specified
        else:
            # return "text", f
            result = f
        
        return "text", result

    elif cmd in commands_img_response:
        # TODO: need to introduce callable function as well
        return "img", commands_img_response[cmd]



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
        cmd_type, response = process_cmd(message.content)

        if cmd_type == "text":
            await client.send_message(message.channel, response)
        elif cmd_type == "img":
            await client.send_file(message.channel, response)
        else:
            await client.send_message(message.channel, "ERROR: cmd_type not 'text' or 'img'")
  
    # if message.content == "!help":
    #     await client.send_message(message.channel, RESPONSES['help'])

    # if message.content == "!sakamoto":
    #     await client.send_file(message.channel, "img/nichijou-sakamoto-san.jpg")

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

    # if message.content.startswith("!lastmatchid"):
    #     try:
    #         username = message.content.replace("!lastmatchid", "").strip()
    #         api = PUBG(os.environ['PUBG_API_KEY'], Shard.PC_OC)
    #         players = api.players().filter(player_names=[username])
    #         last_match_id = players[0].matches[0].id
    #         await client.send_message(message.channel, last_match_id)

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
