import discord
from discord.ext import commands
import os, asyncio
from dotenv import load_dotenv

from help_bot import help_bot
from music_bot import music_bot

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

async def main():
    async with bot:
        print("--------------------")
        print("TurtleBot is online!")
        print("--------------------")
        await bot.add_cog(help_bot(bot))
        await bot.add_cog(music_bot(bot))
        await bot.start(token)

asyncio.run(main())