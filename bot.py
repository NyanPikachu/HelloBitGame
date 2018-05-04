import discord
from discord.ext import commands
import os
import sys
from motor import motor_asyncio
import requests
import json
from ext import utils

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
    await bot.change_presence(activity=discord.Activity(name=f'BattleBit | !help', type=discord.ActivityType.playing))
    
@bot.command(hidden=True)
async def ping(ctx):
    '''Pong! Get the bot's response time'''
    em = discord.Embed(color=discord.Color.gold())
    em.title = "Pong!"
    em.description = f'{bot.latency * 1000:.0f} ms'
    await ctx.send(embed=em)
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        return await ctx.send('Please provide a prefix for this command to work')
    try:
        await save_prefix(prefix, guildID)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')
    
@bot.command()
async def suggest(ctx, *, suggestion=None):
    """suggest a feature to be added"""
    if not suggestion:
        em = discord.Embed(color=utils.random_color())
        em.title = f'Usage: {ctx.prefix}suggest <suggestion>'
        em.description ='suggest a feature to be added!'
        return await ctx.send(embed=em)
    ch = bot.get_channel(377192503474126866)
    em = discord.Embed(color=utils.random_color())
    em.description = str(suggestion)
    em.title = 'Suggestion'
    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    em.set_footer(text="Bot created By Nyan Pikachu#4148")
    await ch.send(embed=em)
    await ctx.send('Thanks for your suggestion Soldier!')
    
@bot.command()
async def bug(ctx, type=None, *, body=None):
    """Report a bug to the Dev Team!"""
    possible_types = ["gameplay", "map", "glitch", "hardware", "optimization" , "rendering" ,"networking", "connection", "ui" , "general" ,"sound", "other"]
    
    if type not in possible_types:
        em = discord.Embed(color=utils.random_color())
        em.title = f'{ctx.prefix}bug <bug-type> <description>'
        em.description ='Report a hug within BattleBit!'
        em.add_field(name='Types:', value=", ".join(possible_types))
        return await ctx.send(embed=em)
    if not body:
        em = discord.Embed(color=utils.random_color())
        em.title = f'{ctx.prefix}bug <bug-type> <description>'
        em.description ='Report a hug within BattleBit!'
        em.add_field(name='Types:', value=", ".join(possible_types))
        return await ctx.send(embed=em)

    ch = bot.get_channel(377192455679901706)
    
    em = discord.Embed(color=utils.random_color())
    em.title = 'Bug Reported'
    em.description = str(body)
    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    em.set_footer(text="Bot created By Nyan Pikachu#4148")
    await ch.send(embed=em)
    await ctx.send('Thanks for your report Soldier!')

@bot.command(aliases=['ui'])
@commands.guild_only()
async def userinfo(ctx, user: discord.Member=None):
    """user info"""
    if not user:
        user = ctx.author
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what i found.", color=utils.random_color())
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Game", value=str(user.activity.name))
    embed.add_field(name="Highest role", value=user.top_role.name or "Empty")
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    em.set_footer(text="Bot created By Nyan Pikachu#4148")
    await ctx.send(embed=embed)
    
@bot.command()
@commands.guild_only()
async def serverinfo(ctx): 
    """server info"""
    embed = discord.Embed(name=f"{user.name}'s info", description="Here's what I found.", color=utils.random_color())
    embed.set_author(name="Pika Bot")
    embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.add_field(name="Owner", value=(ctx.message.guild.owner))
    embed.add_field(name="Created at", value=(ctx.message.guild.created_at))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    em.set_footer(text="Bot created By Nyan Pikachu#4148")
    await ctx.send(embed=embed)

bot.run(os.environ.get("TOKEN"))
