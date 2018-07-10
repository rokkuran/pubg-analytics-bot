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


query = Query()


commands_text_response = {
    "help": RESPONSES["help"],
    "test": test,
    "testargs": testargs,
    "playerid": query.get_player_id,
    "lastmatchid": query.get_last_match_id,
    "lastmatchinfo": query.get_last_match_info,
}

commands_img_response = {
    "zonedist": "PLACEHOLDER",
    "sakamoto": "img/nichijou-sakamoto-san.jpg",
    # "testplot", query.test_plot,
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
        else:
            result = f
        
        return "text", result

    elif cmd in commands_img_response:
        # TODO: need to introduce callable function as well
        return "img", commands_img_response[cmd]
    else:
        return None, "Command not recognised."





@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):

    try:
        if message.content in RESPONSES:
            await client.send_message(message.channel, RESPONSES[message.content])

        if message.content.startswith("!"):
            cmd_type, response = process_cmd(message.content)

            if cmd_type == "text":
                await client.send_message(message.channel, response)
            elif cmd_type == "img":
                await client.send_file(message.channel, response)
            else:
                await client.send_message(message.channel, response)

    except Exception as e:
        await client.send_message(message.channel, e)


client.run(os.environ['DISCORD_BOT_TOKEN'])
