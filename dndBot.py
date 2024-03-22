from enum import member
import discord
import disnake
import random
from disnake.ext import commands 
from datetime import datetime
import json

bot = commands.Bot(command_prefix="/",help_command=None, intents=disnake.Intents.all())

DisnakeVersion = disnake.__version__

current_datetime = datetime.now()

#тут типа загрузка токена
with open('config.json', 'r') as f:
  config = json.load(f)
token = config['token']

#тут типа загрузка
@bot.event
async def on_ready():
    print(
        f"Бот {bot.user} запушен\n"
        f"Версия disnake:{DisnakeVersion}v\n"
        f"{current_datetime}\n")


print()
#тут типа лог входа + выдача роли
@bot.event
async def on_member_join(member):

    await member.add_roles(discord.utils.get(member.guild.roles, name="guest"))

    channel = bot.get_channel(1220774884662313071)

    if channel is not None:
        embed = disnake.Embed(
            title="new person",
            description=f"{member.name}#{member.discriminator}\n<@{member.id}>",
            color=0x839cff
        )
        await channel.send(embed=embed)

#тут типа ролл 
@bot.slash_command(name="roll", description="Бросить кубик")
async def roll(ctx, min: int, max: int):
    # Проверка диапазона
    channel = bot.get_channel(1220775464029786123)
    if min > max:
        await ctx.respond("Минимальное значение не может быть больше максимального.", ephemeral=True)
        return

    result = random.randint(min, max)

    embed = disnake.Embed(
        title="Результат броска",
        description=f"**Пользователь:** {ctx.author.name}\n**Выпало число:** {result}",
        color=0x839cff
    )
    print(f"**Пользователь:** {ctx.author.name}\n**Выпало число:** {result}")
    await ctx.response.send_message(embed=embed)
    await channel.send(embed=embed)


class Plbuttons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=0)
        self.add_item(disnake.ui.Button(label="Показать героев", style=disnake.ButtonStyle.green,row=1, custom_id="show_heroes"))
        self.add_item(disnake.ui.Button(label="Участвовать в игре!", style=disnake.ButtonStyle.primary,row=0, custom_id="play_game"))
        self.add_item(disnake.ui.Button(label="Отменить участие =(", style=disnake.ButtonStyle.danger,row=0, custom_id="end_for_me_game"))



@bot.slash_command(name="start_game", description="Начало игры")
async def start_game(ctx):
    embed = disnake.Embed(
        title="Подготовка к игре",
        description="Внимательно слушай GM`A!!!",
        color=0x839cff
    )
    gameb = Plbuttons()
    await ctx.response.send_message(embed=embed, view=gameb)

@bot.event
async def on_button_click(interaction: disnake.Interaction):
    if interaction.component.custom_id == "show_heroes":
        await interaction.response.send_message("coming soon", ephemeral=True)
    
    if interaction.component.custom_id == "play_game":
        member = interaction.user
        player_role = discord.utils.get(member.guild.roles, name="player")
        if player_role:
            await member.add_roles(player_role)
            await interaction.response.send_message(f"Роль {player_role.name} Вы в игре!", ephemeral=True)
        else:
            await interaction.response.send_message("Роль 'player' не найдена!", ephemeral=True)
    
    if interaction.component.custom_id == "end_for_me_game":
        await interaction.response.send_message("coming soon", ephemeral=True)

bot.run(token)