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
    # Get information for character
    info = mapleRanks.getInfo(name)

    # Create embed for display
    embed = discord.Embed(title=f"{info['name']}",
                      description=f"{info['level']}")

    embed.set_author(name="MSBot")

    # Temporary, should be done in mapleranks.py
    text = info['exp_1']
    words = text.split()
    val = words[-1]
    embed.add_field(name="Average Daily Exp",
                    value=f"{val}",
                    inline=False)

    embed.set_thumbnail(url="https://i.mapleranks.com/u/FOEBIAKMEBDFKPLJMKFDKEMBOMBADJBMAKMLAGNMGHABCCIOLLJMEDGAEGLLDNDKOHOBBNCKMFNFLAKLPCNFAIIDKNNAKAJNAAKNPPECMCJJPHNACNLLPMEFFDDMIFNNKMKHFBLKEHDMDLGKCOFBGNMOBCAJOJAIDAHEPGOHLIPIJBBCDJLBIDDKOCJBIMAPEHJOKIBHAGCABDIDFILKFOGDNJAHGFHKLDJLFPNMIPPNBGDHNOHDPFBCIAIOEBIG.png")

    await ctx.send(embed=embed)


client.run(token)