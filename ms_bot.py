import maple_ranks
import exp_calculations
import discord
import culvert_score
from os import environ
from discord.ext import commands
import numpy as np
import cv2
import aiohttp

# Globals
MAX_LEVEL = 300

# Discord bot setup
token = environ["TOKEN"]
client = commands.Bot(command_prefix='#', intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'Connected to server')
    print('---------------------')

@client.command(name='msr')
async def exp(ctx, name):
    '''
    Command to grab player's daily exp and day to level

     Args:
        ctx: User's command.
        name: Character name to look up.
    
    Returns:
        None
    '''
    await ctx.message.delete()
    # Get information for character
    info = maple_ranks.get_info(name)

    # Get the values needed for predicted days to level based on players daily average exp.
        # Start
    # String manipulation to grab players current percentage within their level.
    s_index = info['level'].find('(') + 1
    e_index = info['level'].find('%')
    curr_perc = info['level'][s_index : e_index + 1].strip()

    # String manipulation to grab players current level
    s_index = info['level'].find(' ') + 1
    e_index = info['level'].find('(')
    curr_lvl = info['level'][s_index : e_index].strip()

    daily_exp = info['exp_1']
    base = exp_calculations.expand_number(daily_exp)
        # End

    if (int(curr_lvl) + 5) <= MAX_LEVEL:
        added_lvls = 5
        exp_dic = exp_calculations.calculate_days_to_x_level(int(curr_lvl), float(daily_exp[:-1]) * base, curr_perc, int(curr_lvl) + 5)
    else:
        if int(curr_lvl) != MAX_LEVEL:
            added_lvls = MAX_LEVEL - int(curr_lvl)
            exp_dic = exp_calculations.calculate_days_to_x_level(int(curr_lvl), float(daily_exp[:-1]) * base, curr_perc, int(curr_lvl) + added_lvls)

    # Create embed for display
    embed = discord.Embed(title=f"{info['name']}",
                          url = info['url'],
                          description=f"{info['level']}\n{info['class_world']}")

    embed.set_author(name="LotusBot")

    embed.add_field(name="Average Daily Exp",
                    value=f"{daily_exp}",
                    inline=False)
    
    if int(curr_lvl) != MAX_LEVEL:
        for i in range(added_lvls):
            embed.add_field(name=f"Days to level {exp_dic[i][0]}",
                        value=f"{exp_dic[i][1]}",
                        inline=False)
   

    embed.set_thumbnail(url=info['img'])

    await ctx.send(embed=embed)

@client.command(name='msrg')
async def exp(ctx, name, goal):
    '''
    Command to grab player's daily exp and day to level that they specified

     Args:
        ctx: User's command.
        name: Character name to look up.
        goal: Integer value to the player's goals

    Returns:
        None
    '''

    await ctx.message.delete()

    # Get information for character
    info = maple_ranks.get_info(name)

    # Get the values needed for predicted days to level based on players daily average exp.
        # Start
    # String manipulation to grab players current percentage within their level.
    s_index = info['level'].find('(') + 1
    e_index = info['level'].find('%')
    curr_perc = info['level'][s_index : e_index + 1].strip()

    # String manipulation to grab players current level
    s_index = info['level'].find(' ') + 1
    e_index = info['level'].find('(')
    curr_lvl = info['level'][s_index : e_index].strip()

    daily_exp = info['exp_1']
    base = exp_calculations.expand_number(daily_exp)
        # End

    if int(goal) < 0 or (int(goal) - int(curr_lvl)) <= 0:
        await ctx.send('Please enter your desired level goal.')

    if (int(curr_lvl) + 5) <= MAX_LEVEL:
        added_lvls = int(goal) - int(curr_lvl)
        exp_dic = exp_calculations.calculate_days_to_x_level(int(curr_lvl), float(daily_exp[:-1]) * base, curr_perc, int(curr_lvl) + added_lvls)
    else:
        if int(curr_lvl) != MAX_LEVEL:
            added_lvls = MAX_LEVEL - int(curr_lvl)
            exp_dic = exp_calculations.calculate_days_to_x_level(int(curr_lvl), float(daily_exp[:-1]) * base, curr_perc, int(curr_lvl) + added_lvls)

    # Create embed for display
    embed = discord.Embed(title=f"{info['name']}",
                          url = info['url'],
                          description=f"{info['level']}\n{info['class_world']}")

    embed.set_author(name="LotusBot")

    embed.add_field(name="Average Daily Exp",
                    value=f"{daily_exp}",
                    inline=False)
    
    if int(curr_lvl) != MAX_LEVEL:
        for i in range(added_lvls):
            embed.add_field(name=f"Days to level {exp_dic[i][0]}",
                        value=f"{exp_dic[i][1]}",
                        inline=False)
   

    embed.set_thumbnail(url=info['img'])

    await ctx.send(embed=embed)

@client.command(name='guildimg')
async def guildimg(ctx):
    '''
    How to use:
        #guildimg <img>
        The program will extract the image for data.
        Ensure that the image contains data from Name -> GPQ Score.

        Please make sure to fix any errors within data extraction and compile a txt file containing the entirety of the guild
    '''
    if ctx.message.attachments and any(att.filename.endswith(('.png', '.jpg', '.jpeg')) for att in ctx.message.attachments):
        # Loop through all attachments
        for attachment in ctx.message.attachments:
            # Download the attachment
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    image_bytes = await resp.read()
            print('Received image:', len(image_bytes), 'bytes')
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            s = culvert_score.get_data(image)
            await ctx.send(f'```{s}```')
            # for data in data_dic:
            #     await ctx.send(f"Name: {data['name']}, Class: {data['class']}, Level: {data['level']}, Score: {data['score']}")
client.run(token)