import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json

dbclient = motor_asyncio.AsyncIOMotorClient('mongodb://hellobitgame:' + os.environ.get("DBPASS") + '@ds255329.mlab.com:55329/hellobitgame')
db = dbclient.hellobitgame

async def get_pre(bot, message):
    try:
        result = await db.settings.find_one({'_id': str(message.guild.id)})
    except AttributeError:
        return "!"
    if not result or not result.get('prefix'):
        return "!"
    return result['prefix']


bot = commands.Bot(command_prefix=get_pre, description="This is an example bot", owner_id=279974491071709194)

async def save_prefix(prefix, guildID):
    await db.settings.update_one({'_id': guildID}, {'$set': {'_id': guildID, 'prefix': prefix}}, upsert=True)

@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.change_presence(activity=discord.Activity(name=f'BattleBit stats! | !help', type=discord.ActivityType.playing))
    
@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
    await ctx.send(embed=em)
    
@bot.command()
async def getmygames(ctx, steamid):
    resp = requests.get(f"http://api.steampowered.com/iplayerservice/getownedgames/v0001/?key=c82192eae76ff13e92aa7b3355b9aa44&steamid={steamid}&format=json")
    data = resp.json()
    em =discord.Embed(color=discord.Color.blue())
    em.title = steamid
    em.description = f"You own {data['response']['game_count']} games!"
    for ids in data['response']['games']:
        em.add_field(name=ids['appid'], value=ids['playtime_forever'])
    await ctx.send(embed=em)
    
@bot.command()
async def say(ctx, *, msg: str):
    await message.delete()
    await ctx.send(msg)
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        await ctx.send('Please provide a prefix for this command to work')
    try:
        await save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')
    

bot.run(os.environ.get("TOKEN"))
