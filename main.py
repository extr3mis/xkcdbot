#Required Libs
import discord
import json
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord.ext import menus, tasks
import os
import datetime
import random

left = '⬅️'
right = '➡️'
rand = '🔀'

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class bot(Bot): #creating subclass for async implementation
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) #inheriting
    async def on_ready(self): 
        print('Logged in as') #Check for login
        self.session = aiohttp.ClientSession() #making ClientSession()
        print(bot.user.name)
        print(bot.user.id)
        print('------')
    async def latest(self):
        async with self.session.get('https://xkcd.com//info.0.json') as resp: #getting data
            data = await resp.json() #Pulling data
        return int(data['num'])
           
bot = bot(command_prefix = "!") #creating instance of bot

class Menu(menus.Menu): 
#Menu required for reaction buttons.
    def __init__(self,num=None,ctx=None):
        super().__init__()
        if num is None:
            self.latest = 0
            self.num = 0
        else:
            self.num = int(num)
        self.ctx = ctx
    async def send_initial_message(self,channel,ctx):
        self.latest = await bot.latest()
        if self.num == 0: self.num = self.latest
        return await channel.send(embed = await getcomic(self.ctx,self.num))
    @menus.button(left)
    async def left(self,payload):
        if self.num != 1:
            self.num=int(self.num)-1
            await self.message.edit(embed = await getcomic(self.ctx,self.num))
    @menus.button(right)
    async def right(self,payload):
        if self.num != self.latest:
            self.num=int(self.num)+1
            await self.message.edit(embed = await getcomic(self.ctx,self.num))
    @menus.button(rand)#random comic
    async def rand(self,payload):
        self.num = random.randint(1,self.latest)
        await self.message.edit(embed = await getcomic(self.ctx,self.num))
        
@bot.command(aliases=['x']) #command acceptor
async def xkcd(ctx,num=None,**kwargs): 
    """Posts the XKCD of the given number, if no number is given, posts the latest."""
    m = Menu(num,ctx)
    await m.start(ctx)

async def getcomic(ctx,num=None): #async func to get comic
    if num is None:
        num = await bot.latest()
    async with bot.session.get(f'https://xkcd.com/{num}/info.0.json') as resp: #getting data
        data = await resp.json() #Pulling data
    num = data['num']
    alt = data['alt']
    title = data['safe_title']
    desc = f'{alt} Link to the original [here](https://xkcd.com/{num}).'
    em = discord.Embed(title=f'{title}: #{num}', color = 0x000000, timestamp=datetime.datetime.now(), description = desc) #Because black is nice.
    em.set_image(url = data['img']) #making embed
    em.set_footer(text=f'Requested by {ctx.message.author.display_name}')
    return em

bot.run(TOKEN)
#Made by @Extr3mis#9663
