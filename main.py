#Required Libs
import discord
import json
import asyncio
import aiohttp
from discord.ext.commands import Bot
import os
TOKEN = os.getenv("DISCORD_TOKEN")

# bot is a subclass of client
bot = Bot(command_prefix='!') #Change it if you want to

@bot.event
async def on_ready(): 
    print('Logged in as') #Check for login
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(aliases = ['x'])
async def xkcd(ctx,num=None,**kwargs): 
    """Posts the XKCD of the given number, if no number is given, posts the latest."""
    if num == None:
        num = ''
    else:
        num=num+'/'
    async with aiohttp.ClientSession() as session: #Making Clientsession
        async with session.get(f'https://xkcd.com/{num}info.0.json') as resp:
            print(resp.status)
            data = await resp.text()
            data = json.loads(data)
            img_url = data['img'] #Pulling data
            title = data['safe_title']
            num = str(data['num'])
        embed = discord.Embed(title=title, color = 0x000000) #Because black is nice.
        embed.set_image(url = img_url)
        embed.add_field(name='Number',value=num)
        await ctx.send(embed = embed)
# Token here
bot.run(TOKEN)
#Made by @Extr3mis#9663
