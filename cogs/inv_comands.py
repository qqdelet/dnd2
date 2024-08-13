import disnake
from disnake.ext import commands
from disnake import OptionChoice
import json
import random
from typing import List


bot = commands.Bot(command_prefix="/",help_command=None, intents=disnake.Intents.all())

with open("game.items.json", "r", encoding="UTF-8") as f:
    case_data = json.load(f)
    available_cases = list(case_data["cases"].keys())

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="create_inv", description="Создать инвентарь")
    async def create_inv(self,interaction,member: disnake.Member):

        user_id = member.id
        channel = self.bot.get_channel(1220775292059123742)

        with open("log.invent.json", "r",encoding="UTF-8") as f:
            data = json.load(f)

        if str(user_id) in data:
            await interaction.response.send_message(f"Инвентарь для пользователя {member.mention} уже существует.")
            return

        data.update({f"{user_id}": {}})

        with open("log.invent.json", "w",encoding="UTF-8") as f:
            json.dump(data, f, indent=2)

        embed = disnake.Embed(
            title="Создание инвентаря",
            color=0x839cff,
            description=f"by {interaction.author.mention} to {member.mention}\n"
                        f"Инвентарь для пользователя был успешно создан. "
        )

        await interaction.response.send_message(f"Инвентарь для пользователя {member.mention} успешно создан.")
        await channel.send(embed=embed)

    @bot.slash_command(name="add_item_inv", description="Добавить предмет в инвентарь пользователя")
    async def add_item_inv(self,interaction, member: disnake.Member, text: str):

        channel = self.bot.get_channel(1220775292059123742)

        with open("log.invent.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        if str(member.id) not in data or "items" not in data[str(member.id)]:
            data[str(member.id)] = {"items": []}

        data[str(member.id)]["items"].append(text)

        with open("log.invent.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        embed = disnake.Embed(
            title="Выдача предмета",
            color=0x839cff,
            description=f"by {interaction.author.mention} to {member.mention}\n"
                        f"был добавлен предмет '{text}'"
        )

        await channel.send(embed=embed)

    @bot.slash_command(name="inventory", description="Показать инвентарь пользователя")
    async def show_inventory(self,interaction, member: disnake.Member = None):

        if member is None:
            member = interaction.author

        with open("log.invent.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        if str(member.id) not in data or not data[str(member.id)]["items"]:
            embed = disnake.Embed(
                title=f"Инвентарь {member.mention}",
                description="Инвентарь пуст.",
                color=0x839cff
            )
            await interaction.response.send_message(embed=embed)
            return

        items = data[str(member.id)]["items"]

        embed = disnake.Embed(
            title=f"Инвентарь",
            description=f"{member.mention}",
            color=0x839cff
        )

        for item in items:
            if isinstance(item, dict):
                item_name = items["name"]
                embed.add_field(name=item_name, value="   ", inline=False)
            else:
                embed.add_field(name=item, value="   ", inline=False)

        await interaction.response.send_message(embed=embed)

    @bot.slash_command(name="remove_item_inv", description="Удалить предмет из инвентаря пользователя")
    async def remove_item_inv(self,interaction, member: disnake.Member, text: str):

        channel = self.bot.get_channel(1220775292059123742)

        with open("log.invent.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        if str(member.id) not in data or "items" not in data[str(member.id)]:
            embed = disnake.Embed(
                title="Удаление предмета",
                color=0x839cff,
                description=f"У пользователя {member.mention} нет инвентаря или предмета '{text}'."
            )
            await interaction.response.send_message(embed=embed)
            return

        items = data[str(member.id)]["items"]

        if text not in items:
            embed = disnake.Embed(
                title="Удаление предмета",
                color=0x839cff,
                description=f"Предмет '{text}' не найден в инвентаре пользователя {member.mention}."
            )
            await interaction.response.send_message(embed=embed)
            return

        items.remove(text)

        with open("log.invent.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        embed = disnake.Embed(
            title="Удаление предмета",
            color=0x839cff,
            description=f"Предмет '{text}' был удален из инвентаря пользователя {member.mention} \nby {interaction.author.mention}."
        )
        await channel.send(embed=embed)

    @bot.slash_command(name="openchest", description="Открыть сундук для <@user> с выбранным типом кейса")
    async def cheastopencomand(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member, case_type: str):
        with open("log.invent.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        if str(member.id) not in str(data):
            await self.create_inv(interaction, member)

        with open("game.items.json", "r", encoding="UTF-8") as f:
            dataItem = json.load(f)

        if case_type not in dataItem["cases"]:
            await interaction.response.send_message("Неверный тип кейса.", ephemeral=True)
            return

        drop = [random.choice(dataItem["cases"][case_type]) for _ in range(3)]

        if str(member.id) not in data or "items" not in data[str(member.id)]:
            data[str(member.id)] = {"items": []}

        data[str(member.id)]["items"].extend(drop)

        with open("log.invent.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        main_embed = disnake.Embed(
            title="Сундук открыт!",
            description=f"Пользователь {member.mention} открыл сундук {case_type} и обнаружил в нём:\n\n" + "\n".join(drop),
            color=0x839cff)

        log_embed = disnake.Embed(
            title="Лог открытия сундука",
            description=f"by {interaction.user.mention} to {member.mention}\nОткрыл сундук {case_type}\n\nДроп:\n\n" + "\n".join(drop),
            color=0x839cff)

        await interaction.response.send_message(embed=main_embed)

        log_channel_id = 1232601811647598673
        log_channel = self.bot.get_channel(log_channel_id)

        # Отправляем Embed в лог-чат
        if log_channel:
            await log_channel.send(embed=log_embed)
        else:
            print("Лог-канал не найден.")

    @cheastopencomand.autocomplete("case_type")
    async def case_autocompletion(
        interaction: disnake.ApplicationCommandInteraction,
        current: str
    ) -> List[OptionChoice]:
        data = [
            OptionChoice(name="обычный", value="обычный"),
            OptionChoice(name="редкий", value="редкий"),
            OptionChoice(name="легендарный", value="легендарный")]
        return data 

def setup(bot):
    print("inv_comands ready\n")
    bot.add_cog(Menu(bot))