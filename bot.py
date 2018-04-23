import discord
from discord.ext import commands
import os
import sys
import motor.motor_asyncio

dbclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://hellobitgame:' + os.environ.get("DBPASS") + '@ds255329.mlab.com:55329/hellobitgame')
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
    
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {bot.ws.latency:.4f * 1000} ms")
    
@bot.command()
async def say(ctx, *, msg: str):
    await message.delete()
    await ctx.send(msg)
    
@commands.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        await ctx.send('Please provide a prefix for this command to work')
    try:
        await self.save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `{e}`')
    
bot.run(os.environ.get("TOKEN"))
