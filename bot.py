import discord
from discord.ext import commands
import os
import sys

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


bot = commands.Bot(command_prefix="+", description="This is an example bot", owner_id=279974491071709194)

async def save_prefix(self, prefix, guildID):
await self.db.settings.update_one({'_id': guildID}, {'$set': {'_id': guildID, 'prefix': prefix}}, upsert=True)

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
    
bot.run(os.environ.get("TOKEN"))
