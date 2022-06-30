import discord
from youtube import Music


def create_music_detail_embed(music: Music) -> discord.Embed:
    embed = discord.Embed(
        title=music.artist,
        description=f'[{music.title}]({music.url})',
        color=discord.Colour.green()
    )
    embed.set_thumbnail(url=music.thumbnail)

    return embed

