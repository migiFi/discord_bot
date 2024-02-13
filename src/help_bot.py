import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
channel_id = int(os.getenv('CHANNEL_ID'))

class help_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.text_channel_list = []
        self.set_message()

    def set_message(self):
        self.help_message = f"""
```
Music-player commands:
   /p    - Plays or resume music (song title - artist).
   /q    - displays music in the queue.
 /pause  - pauses current song.
 /resume - resumes playing current song.
 /skip   - skips the current song.
 /remove - removes last song from the queue.
 /clear  - Stops the music and clears the queue.
 /stop   - Disconnects bot from channel.
```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="send_to_all")
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(f"Welcome to MrOrnito's server :tada: {member.mention}")