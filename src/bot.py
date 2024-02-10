import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
channel_id = int(os.getenv('CHANNEL_ID'))

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print('--------------------')
    print('TurtleBot is online!')
    print('--------------------')

@client.event
async def on_member_join(member):
    channel = client.get_channel(channel_id)
    await channel.send("Welcome to MrOrnito's server :tada:")

@client.command()
async def help_commands(ctx):
    await ctx.send('-----ADD BOT COMMANDS HERE----')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(channel_id)
    await channel.send("Sad to see you go :smiling_face_with_tear:")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('You must be in a voice channel to run this command!')

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('TurtleBot has left the chat!')
    else:
        await ctx.send('I am not in a voice channel.')


client.run(token)