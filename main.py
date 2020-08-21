#Required Libs
import discord
import json
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord.ext import menus
import os
import datetime
import random
TOKEN = os.getenv("DISCORD_TOKEN")
left = '⬅️'
right = '➡️'
rand = '🔀'
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

class Menu(menus.Menu): 
#Menu required for reaction buttons.
    def __init__(self,num=None,ctx):
        super().__init__()
        self.latest = int(await latest())
        if num is None:
            self.num = self.latest
        else:
            self.num = int(num)
        self.ctx = ctx
    async def send_initial_message(self,channel,ctx):
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
        num = await latest()
    async with bot.session.get(f'https://xkcd.com/{num}/info.0.json') as resp: #getting data
        print(resp.status)
        data = await resp.json() #Pulling data
    num = data['num']
    alt = data['alt']
    title = data['safe_title']
    desc = f'{alt} Link to the original [here](https://xkcd.com/{num}).'
    em = discord.Embed(title=f'{title}: #{num}', color = 0x000000, timestamp=datetime.datetime.now(), description = desc) #Because black is nice.
    em.set_image(url = data['img']) #making embed
    em.set_footer(text=f'Requested by {ctx.message.author.display_name}')
    return em

async def latest():
    async with bot.session.get('https://xkcd.com/info.0.json') as resp: #getting data
        print(resp.status)
        data = await resp.json() #Pulling data
    num = int(data['num'])
    return num

bot.run(TOKEN)
#Made by @Extr3mis#9663
