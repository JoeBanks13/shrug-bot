"""
A discord bot to superimpose your avatar onto a shrug.
"""

import logging
from os import getenv
from io import BytesIO

import discord

from discord.ext import commands
from PIL import Image, ImageDraw, ImageOps


if getenv("TOKEN") is None:
    print("Woah! You forgot to set a TOKEN environment variable.")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shrug-bot")

canvas = Image.open("shrug.png")
bot = commands.Bot(command_prefix="!", pm_help=False, description=r"¯\_(ツ)_/¯")


def draw_face(base: Image, avatar: Image, destination: tuple, size: tuple, rotation: int):
    mask = Image.new("L", avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + avatar.size, fill=255)
    head = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    head.putalpha(mask)
    face = head.resize(size, Image.LANCZOS)
    face = face.rotate(rotation, expand=True)
    base.paste(face, destination, face)


@bot.event
async def on_ready():
    logger.info(f"Logged in on {len(bot.guilds)} guilds")


@bot.command()
async def shrug(ctx, user: discord.Member = None):
    base = canvas.copy()
    user = user or ctx.author
    avatar = Image.open(BytesIO(await user.avatar_url.read()))
    draw_face(base, avatar, (155, 70), (78, 78), 15)
    draw_face(base, avatar, (351, 43), (36, 36), -4)
    draw_face(base, avatar, (350, 225), (40, 40), 5)
    result = BytesIO()
    base.save(result, format="png")
    result.seek(0)
    await ctx.send(
        file=discord.File(fp=result, filename="shrug.png")
    )


bot.run(getenv("TOKEN"))
