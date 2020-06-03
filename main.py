#Required Libs
import discord
import json
import asyncio
import aiohttp
from discord.ext.commands import Bot
import os
import datetime
TOKEN = os.getenv("DISCORD_TOKEN")

class bot(Bot): #creating subclass for async implementation
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) #inheriting
    async def on_ready(self): 
        print('Logged in as') #Check for login
        self.session = aiohttp.ClientSession() #making ClientSession()
        print(bot.user.name)
        print(bot.user.id)
        print('------')

bot = bot(command_prefix = "!") #creating instance of bot
@bot.command(aliases=['x'])
async def xkcd(ctx,num=None,**kwargs): 
        """Posts the XKCD of the given number, if no number is given, posts the latest."""
        if num is None:
            url = 'https://xkcd.com/info.0.json'
        else:
            url = f'https://xkcd.com/{num}/info.0.json'
        async with bot.session.get(url) as resp: #getting data
            print(resp.status)
            data = await resp.json() #Pulling data
        em = discord.Embed(title=data['safe_title'], color = 0x000000, timestamp=datetime.datetime.now()) #Because black is nice.
        em.set_image(url = data['img']) #making embed
        em.add_field(name='Number',value=str(data['num']))
        em.set_footer(text=f'Requested by {ctx.message.author.display_name}')
        await ctx.send(embed = em)
bot.run(TOKEN)
#Made by @Extr3mis#9663
