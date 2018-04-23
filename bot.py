import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio

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
    
@bot.command()
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
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
        await self.save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')
    
@bot.command(name='presence')
@bot.is_owner
async def _presence(ctx, type=None, *, game=None):
    '''Change the bot's presence'''
    if type is None:
        await ctx.send(f'Usage: `{ctx.prefix}presence [game/stream/watch/listen] [message]`')
    else:
        if type.lower() == 'stream':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.streaming))
            await ctx.send(f'Set presence to. `Streaming {game}`')
        elif type.lower() == 'game':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.playing))
            await ctx.send(f'Set presence to `Playing {game}`')
        elif type.lower() == 'watch':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
            await ctx.send(f'Set presence to `Watching {game}`')
        elif type.lower() == 'listen':
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.listening))
            await ctx.send(f'Set presence to `Listening to {game}`')
        elif type.lower() == 'clear':
            await bot.change_presence(activity=discord.Activity(name=None))
            await ctx.send('Cleared Presence')
        else:
            await ctx.send('Usage: `.presence [game/stream/watch/listen] [message]`')
 
    
bot.run(os.environ.get("TOKEN"))
