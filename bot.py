import discord
import asyncio
import os
import yaml

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




commands_text_response = {
    "help": RESPONSES["help"],
    "helpfs": RESPONSES["helpfs"],
    "helpls": RESPONSES["helpls"],
    "test": test,
    "testargs": testargs,
    "playerid": query.get_player_id,
    "lastmatchid": query.get_last_match_id,
    "lastmatchinfo": query.get_last_match_info,
}

commands_img_response = {
    "zonedist": "PLACEHOLDER",
    "sakamoto": "img/nichijou-sakamoto-san.jpg",
    "ritalinlost": "img/ritalin_lost.jpg",
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


def plot_test(N=50):
    random_x = np.linspace(0, 1, N)
    random_y = np.random.randn(N)

    # Create a trace
    trace = go.Scatter(
        x = random_x,
        y = random_y
    )

    data = [trace]

    # py.iplot(data, filename='basic-line')
    # a = py.iplot(data, filename='basic-line')

    a = py.plot(data, filename='basic-line')
    
    return a.resource



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

        if message.content == "~embedtest":
            # embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
            # embed.add_field(name="Field1", value="hi", inline=False)
            # embed.add_field(name="Field2", value="hi2", inline=False)
            # plot_url = plot_test()
            # await client.send_message(message.channel, plot_url)

            embed = discord.Embed()
            plot_url = plot_test()
            # plot_url = "https://plot.ly/~rokkuran/0"
            # embed.add_field(name="url", value=plot_url)
            embed.set_image(url=plot_url)
            await client.send_message(message.channel, embed=embed)

    except Exception as e:
        await client.send_message(message.channel, e)


client.run(os.environ['DISCORD_BOT_TOKEN'])
