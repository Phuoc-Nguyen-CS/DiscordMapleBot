import mapleRanks
import discord
from os import environ
from discord.ext import commands

token = environ["TOKEN"]

client = commands.Bot(command_prefix='>>', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'Connected to server')
    print('---------------------')

@client.command(name='exp')
async def getExp(ctx, name):
    '''
    A function in which once a command has been detected.
    Get data from mapleranks and display user exp and future progress here.

     Args:
        ctx: User's command.
        name: Character name to look up.
    
    Returns:
        None
    '''
    await ctx.message.delete()
    # Get information for character
    info = mapleRanks.getInfo(name)

    # Create embed for display
    embed = discord.Embed(title=f"{info['name']}",
                      description=f"{info['level']}")

    embed.set_author(name="MSBot")

    exp = info['exp_1']
    embed.add_field(name="Average Daily Exp",
                    value=f"{exp}",
                    inline=False)
    print(info['url'])
    embed.set_thumbnail(url=info['url'])

    await ctx.send(embed=embed)


client.run(token)