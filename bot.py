import discord
from discord.utils import get

import asyncio
import os
import yaml
import requests
import emoji
import random

from pubg_python import PUBG, Shard

from common import Query


import numpy as np


import plotly
plotly.tools.set_credentials_file(username='rokkuran', api_key=os.environ['PLOTLY_API_KEY'])


import plotly.plotly as py
import plotly.graph_objs as go



client = discord.Client()
RESPONSES = yaml.safe_load(open('responses.yaml', 'rb'))


def test(a):
    return "test function returned with arg={}".format(a)

def testargs(*args):
    return "testargs function returned with args={}".format(args)


query = Query()


trigger_text_single_responses = RESPONSES['trigger_text_single_responses']
trigger_text_multiple_responses = RESPONSES["trigger_text_multiple_responses"]
cmd_based_text_responses = RESPONSES["cmd_based_text_responses"]
emoji_reactions = RESPONSES["emoji_reactions"]

command_text_responses = {
    "responses": RESPONSES,
    "help": cmd_based_text_responses["help"],
    "test": test,
    "testargs": testargs,
    "playerid": query.get_player_id,
    "lastmatchid": query.get_last_match_id,
    "lastmatchinfo": query.get_last_match_info,
    "playerattackevents": query.get_player_attack_events,
    "playerkillevents": query.get_player_kill_events,
}

trigger_anywhere_text_responses = RESPONSES['trigger_anywhere_text_responses']


command_img_responses = {
    "zonedist": "PLACEHOLDER",
    "sakamoto": "img/nichijou-sakamoto-san.jpg",
    "portrait": "img/profile-pic_kitan-club-lemon.jpg",
    # "testplot", query.test_plot,
}

command_embed_responses = {
    "tatamigalaxy": 'https://media.kitsu.io/anime/poster_images/5122/small.jpg',
    "embedtest": query.plot_test,
    "embedplottest": 'https://plot.ly/%7Erokkuran/0.jpeg',
    "embedplottest2": 'https://plot.ly/%7Erokkuran/12.jpeg',
    "plotweapondmg": query.plot_weapon_dmg,
    "pdmgn": query.plot_all_weapon_dmg_for_user_match,
}


def get_cmd(msg):
    return msg[1:].split()[0]


def get_cmd_args(msg):
    return msg[1:].split()[1:]


def cmd_response(msg, cmd, response_dict):
    args = get_cmd_args(msg)
    f = response_dict[cmd]
    
    result = f
    if callable(f):
        if len(args) > 0:
            result = f(*args)    
        else:
            # if no arg cmd is not recognised it will return an exception later
            pass
    return result


def process_cmd(msg):
    """
    Returns: cmd_type, result
    """
    cmd = get_cmd(msg)

    if cmd in command_text_responses:
        return "text", cmd_response(msg, cmd, command_text_responses)

    elif cmd in command_img_responses:
        return "img", command_img_responses[cmd]
    
    elif cmd in command_embed_responses:
        return "embed", cmd_response(msg, cmd, command_embed_responses)
    
    else:
        return None, "Command not recognised."


def random_reaction(emoji_long_names: list):
    reactions = [emoji.emojize('{}'.format(e), use_aliases=True) for e in emoji_long_names]
    return random.choice(reactions)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):

    try:
        if not message.author.bot:
            trigger_text_single_responses = RESPONSES['trigger_text_single_responses']

            if message.content in trigger_text_single_responses:
                response = trigger_text_single_responses[message.content]
                await client.send_message(message.channel, response)

            elif message.content in trigger_text_multiple_responses:
                response = random.choice(trigger_text_multiple_responses[message.content])
                await client.send_message(message.channel, response)
                

            elif message.content.startswith("!"):
                cmd_type, response = process_cmd(message.content)

                if cmd_type == "text":
                    await client.send_message(message.channel, response)
                elif cmd_type == "img":
                    await client.send_file(message.channel, response)
                elif cmd_type == "embed":
                    # await client.send_message(message.channel, response)
                    embed = discord.Embed(colour=discord.Colour.blue())
                    embed.set_image(url=response)
                    await client.send_message(message.channel, embed=embed)
                else:
                    await client.send_message(message.channel, response)

            for k in trigger_anywhere_text_responses:
                if k in message.content.lower():
                    await client.send_message(message.channel, trigger_anywhere_text_responses[k])
            
            # add reactions to messages
            for k, v in emoji_reactions.items():
                if k in message.content.lower():
                    await client.add_reaction(message, random_reaction(v))         

    except Exception as e:
        await client.send_message(message.channel, e)



client.run(os.environ['DISCORD_BOT_TOKEN'])
