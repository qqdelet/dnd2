import disnake
from disnake.ext import commands
from disnake import OptionChoice
import json
import random
from typing import List

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())

with open("game.items.json", "r", encoding="UTF-8") as f:
    case_data = json.load(f)
    available_cases = list(case_data["cases"].keys())

class HpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="set_hp", description="Установить показатели HP и армора")
    async def set_hp(self, interaction, member: disnake.Member, hp: int, armor: int):
        user_id = member.id
        channel = self.bot.get_channel(1259466605075890308)

        with open("log.hp.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        data[str(user_id)] = {
            "hp": hp,
            "armor": armor}

        with open("log.hp.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2)

        embed = disnake.Embed(
            title="Установка показателей HP и армора",
            color=0xff216f,
            description=f"Показатели HP и армора для пользователя {member.mention} были успешно установлены:\n"
                        f"Здоровье: {hp}\n"
                        f"Армор: {armor}")

        embed2 = disnake.Embed(
            title="Установка показателей HP и армора",
            color=0xff216f,
            description=f"by {interaction.author.mention} to {member.mention}\n"
                        f"Установил показатели HP и Армора "
                        f"Здоровье: {hp}\n"
                        f"Армор: {armor}")

        await interaction.response.send_message(embed=embed)
        await channel.send(embed=embed2)

        if hp == 0:
            death_embed = disnake.Embed(
                title="Игрок был убит",
                color=0x000000,
                description=f"Игрок {member.mention} мертв."
            )
            await channel.send(embed=death_embed)
            

    @bot.slash_command(name="view_hp", description="Просмотреть текущие показатели HP и армора")
    async def view_hp(self, interaction, member: disnake.Member):
        user_id = member.id

        with open("log.hp.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        if str(user_id) not in data:
            await interaction.response.send_message(f"Показатели HP для пользователя {member.mention} не найдены.")
            return

        hp_value = data[str(user_id)]["hp"]
        armor_value = data[str(user_id)]["armor"]

        if hp_value == 0:
            death_embed = disnake.Embed(
                title="Игрок мертв",
                color=0x000000,
                description=f"Игрок {member.mention} мертв."
            )
            await interaction.response.send_message(embed=death_embed)
        else:
            embed = disnake.Embed(
                title="Текущие показатели HP и армора",
                color=0xff216f,
                description=f"Текущие показатели HP и армора для пользователя {member.mention}:\n"
                            f"Здоровье: {hp_value}\n"
                            f"Армор: {armor_value}")

            await interaction.response.send_message(embed=embed)

def setup(bot):
    print("\nheals ready")
    bot.add_cog(HpCog(bot))
