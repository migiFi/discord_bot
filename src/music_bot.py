import discord
import asyncio
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

class music_bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.voiceChannel = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    def youtube_search(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return{'source':item, 'title':title}
        search = VideosSearch(item, limit=1)
        return{'source':search.result()["result"][0]["link"],
                'title':search.result()["result"][0]["title"]}

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            music_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(music_url, download=False))
            song = data['url']
            self.voiceChannel.play(discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS),
                          after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    async def to_play(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            music_url = self.music_queue[0][0]['source']
            if self.voiceChannel == None or not self.voiceChannel.is_connected():
                self.voiceChannel = await self.music_queue[0][1].connect()

                if self.voiceChannel == None:
                    await ctx.send("-->> I cannot to connect to the channel :neutral_face: <<--")
                    return
            else:
                await self.voiceChannel.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(music_url, download=False))
            song = data['url']
            self.voiceChannel.play(discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS),
                          after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))

        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("-->> You need to connect to a voice channel first! <<--")
            return
        if self.is_paused:
            self.voiceChannel.to_resume()
        else:
            song = self.youtube_search(query)
            if type(song) == type(True):
                await ctx.send("-->> Download failed: issues with the playlist or wrong format. Try a different keyword. <<--")
            else:
                if self.is_playing:
                    await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** was added to the queue")  
                else:
                    await ctx.send(f"**'{song['title']}'** was added to the queue!:notes: ")  
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.to_play(ctx)

    @commands.command(name="to_pause")
    async def to_pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.voiceChannel.to_pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.voiceChannel.to_resume()

    @commands.command(name = "to_resume", aliases=["r"])
    async def to_resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.voiceChannel.to_resume()

    @commands.command(name="to_skip", aliases=["s"])
    async def to_skip(self, ctx):
        if self.voiceChannel != None and self.voiceChannel:
            self.voiceChannel.stop()
            # tries to play next in for_queue
            await self.to_play(ctx)


    @commands.command(name="for_queue", aliases=["q"])
    async def for_queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(f"-->> Next in the queue:\n{retval}")
        else:
            await ctx.send("-->> Nothing in the queue, feel free to add a song.:wink:")

    @commands.command(name="clear_queue", aliases=["c"])
    async def clear_queue(self, ctx):
        if self.voiceChannel != None and self.is_playing:
            self.voiceChannel.stop()
        self.music_queue = []
        await ctx.send("-->> Queued music cleared <<--")

    @commands.command(name="stop", aliases=["dc"])
    async def disconnect_bot(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.voiceChannel.disconnect()
    
    @commands.command(name="remove", aliases=["rm"])
    async def remove_last_song(self, ctx):
        self.music_queue.pop()
        await ctx.send("-->> Last song was removed <<--")