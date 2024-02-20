import discord
import os
from discord import member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
channel_id = int(os.getenv('CHANNEL_ID'))

class help_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.text_channel_list = []
        self.set_message()

    def set_message(self):
        self.help_message = f"""
```
Music-player commands:
    /p       - Plays or resume music (song title - artist).
    /q       - displays music in the queue.
  /pause     - pauses current song.
  /skip[s]   - skips the current song.
 /resume[r]  - resumes playing current song.
 /remove[r]  - removes last song from the queue.
 /clear[c]   - Stops the music and clears the queue.
  /stop      - Disconnects bot from channel.
```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(f"Welcome to MrOrnito's server :tada: {member.mention}")
            
    @commands.command(name="kick")
    @has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"User {member.mention} has been kicked!")
        
    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do **not** have permission to kick people!")
            
    @commands.command(name="ban")
    @has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"User {member.mention} has been banned!")
        
    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do **not** have permission to ban people!")