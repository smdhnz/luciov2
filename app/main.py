import os
import discord
from discord import Bot, VoiceClient, Option
from discord import ApplicationContext
from discord.utils import get

from youtube import Youtube, Music
from data import Queue
from message import create_music_detail_embed
from options import ytdl_options, ffmpeg_options


if os.getenv('DEBUG') == '1':
    bot = Bot(debug_guilds=[os.getenv('GUILD_ID')])
else:
    bot = Bot()

yt = Youtube(os.getenv('YT_API_KEY'), ytdl_options, ffmpeg_options)
q = Queue()


async def connect(ctx: ApplicationContext, voice: VoiceClient):
    channel = ctx.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
        return voice
    else:
        voice = await channel.connect()
        return voice



def play_queue(voice: VoiceClient, guild_id: str):
    music = q.poll(guild_id)

    if music is None:
        return

    voice.play(
        yt.create_stream_source(music),
        after=lambda e: play_queue(voice, guild_id)
    )



@bot.command()
async def play(ctx: ApplicationContext, input: Option(str, '検索語句またはURL')):
    if ctx.author.voice is None:
        await ctx.respond(f'{ctx.author} is not in vc')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    voice = await connect(ctx, voice)

    music: Music = yt.search(input)
    embed = create_music_detail_embed(music)
    await ctx.respond(embed=embed)

    q.add(ctx.guild_id, music)

    if voice.is_playing():
        return

    play_queue(voice, ctx.guild_id)



@bot.command()
async def queue(ctx: ApplicationContext):
    if ctx.author.voice is None:
        await ctx.respond(f'{ctx.author} is not in vc')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is None:
        await ctx.respond(f'{bot.user} is not in vc')
        return

    list_of_queue = [music.title for music in q.get_queue(ctx.guild_id)]

    if len(list_of_queue) == 0:
        await ctx.respond('no songs in queue')
        return

    await ctx.respond('\n'.join(list_of_queue))



@bot.command()
async def bye(ctx: ApplicationContext):
    if ctx.author.voice is None:
        await ctx.respond(f'{ctx.author} is not in vc')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice is None:
        await ctx.respond(f'{bot.user} is not in vc')
        return

    q.reset(ctx.guild_id)
    await voice.disconnect()
    await ctx.respond('disconnected')



bot.run(os.getenv('TOKEN'))

