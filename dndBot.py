from enum import member
import discord
import disnake
from disnake import OptionChoice
import random
from disnake.ext import commands
from datetime import datetime
from typing import Callable, Optional
import json
from Paginator import Pagination, L

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all(), test_guilds=[1220705242014941306])

DisnakeVersion = disnake.__version__

current_datetime = datetime.now()

# Загрузка токена
with open('config.json', 'r') as f:
    config = json.load(f)
token = config['token']

def save_participants(participants):
    with open('participants.json', 'w') as f:
        json.dump(participants, f, indent=4)

# Лог запуска
@bot.event
async def on_ready():
    print(
        f"Бот {bot.user} запущен\n"
        f"Версия disnake: {DisnakeVersion}v\n"
        f"{current_datetime}\n")

# Выдача роли
@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name="guest"))

    channel = bot.get_channel(1251281527208149043)

    if channel is not None:
        embed = disnake.Embed(
            title="new person",
            description=f"{member.name}#{member.discriminator}\n<@{member.id}>",
            color=0x839cff)
        
        await channel.send(embed=embed)

# Команда ролл
@bot.slash_command(name="roll", description="Бросить кубик")
async def roll(ctx, min: int, max: int):
    channel = bot.get_channel(1220775464029786123)
    if min > max:
        await ctx.respond("Минимальное значение не может быть больше максимального.", ephemeral=True)
        return

    result = random.randint(min, max)

    embed = disnake.Embed(
        title="Результат броска",
        description=f"**Пользователь:** {ctx.author.name}\n**Выпало число:** {result}",
        color=0x839cff)
    
    print(f"**Пользователь:** {ctx.author.name} использует /roll \n**Выпало число:** {result}")
    await ctx.response.send_message(embed=embed)
    await channel.send(embed=embed)

bot.load_extension("cogs.heals")
bot.load_extension("cogs.sp")
bot.load_extension("cogs.ses")
bot.load_extension("cogs.inv_comands")

bot.run(token)