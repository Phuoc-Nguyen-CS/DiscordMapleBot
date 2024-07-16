import maple_ranks
import exp_calculations
import discord
import culvert_score
from os import environ
from discord.ext import commands
import numpy as np
import cv2
import aiohttp
import re
import csv
import pandas as pd

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

@client.command(name='img')
async def img(ctx):
    '''
    How to use:
        #img <img>
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

@client.command(name='guild')
async def guild(ctx):
    result = []
    if ctx.message.attachments and any(att.filename.endswith('.txt') for att in ctx.message.attachments):
        for attachment in ctx.message.attachments:
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    text = await resp.text()
    lines = text.strip().split('\n')
    for line in lines:
        match = re.search(r'(\w+)\s+(\w+(?: \w+)*)\s+(\d+)\s+(\w+)\s+(\d+)\s+(\d+)', line)
        if match:
            name, player_class, level, score = match.groups()[:3] + match.groups()[5:]
            result.append({
                'Name': name,
                'Class': player_class,
                'Level': level,
                'GPQ': score
            })
    fields = ['Name', 'Class', 'Level', 'GPQ']
    filename = 'guild.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result)

    # Read the csv
    csv_file = pd.read_csv('guild.csv')
    # Save as xlsx file
    csv_file.to_excel('guild.xlsx', sheet_name='Guild', index=False)
    file = discord.File('guild.xlsx')
    await ctx.send(file=file)

@client.command(name='guildxp')
async def guildxp(ctx):
    if ctx.message.attachments and any(att.filename.endswith('.xlsx') for att in ctx.message.attachments):
        # Loop through all attachments
        for attachment in ctx.message.attachments:
            # Download the attachment
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status != 200:
                        return await ctx.send('Could not download file...')
                    data = await resp.read()
                    with open(attachment.filename, 'wb') as f:
                        f.write(data)
            # Now you can use pandas to read the file
            file = pd.read_excel(attachment.filename)
            if '7 Day Avg. Exp' not in file.columns:
                file['7 Day Avg. Exp'] = ''
            file['7 Day Avg. Exp'] = file['7 Day Avg. Exp'].astype(str)
            for name in file['Name']:
                val = maple_ranks.get_xp(name)
                file.loc[file['Name'] == name, '7 Day Avg. Exp'] += val
            print(file)
        file.to_excel('guild.xlsx', index=False)
        file = discord.File('guild.xlsx')
        await ctx.send(file=file)

client.run(token)