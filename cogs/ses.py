import disnake
from disnake.ext import commands
import json

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())

json_file_path = "sessions.json"


class SessionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='create_session',description="Создание игровой сесий")
    async def create_session(self, ctx: disnake.ApplicationCommandInteraction,
                            game_master: disnake.Member,
                            cain: disnake.Member,
                            meretrix: disnake.Member,
                            medicus: disnake.Member,
                            nolla: disnake.Member,
                            bella: disnake.Member):

        log_embed = disnake.Embed(title="Новая игровая сессия (логи)", color=disnake.Color.blue())
        log_embed.add_field(name="Гейм мастер", value=game_master.mention, inline=False)
        log_embed.add_field(name="Cain", value=cain.mention, inline=False)
        log_embed.add_field(name="Meretrix", value=meretrix.mention, inline=False)
        log_embed.add_field(name="Medicus", value=medicus.mention, inline=False)
        log_embed.add_field(name="Nolla", value=nolla.mention, inline=False)
        log_embed.add_field(name="Bella", value=bella.mention, inline=False)

        log_channel = self.bot.get_channel(1263505388116902000) 
        if log_channel is None:
            await ctx.send(f"Не удалось найти канал с ID 1263505388116902000. Проверьте правильность ID и права доступа бота.", ephemeral=True)
            return

        await log_channel.send(embed=log_embed)

        role_dict = {
            game_master: "Гейм мастер",
            cain: "Cain",
            meretrix: "Meretrix",
            medicus: "Medicus",
            nolla: "Nolla",
            bella: "Bella"
        }

        for member, role in role_dict.items():
            user_embed = disnake.Embed(title="Новая игровая сессия", color=disnake.Color.green())
            user_embed.add_field(name="Ваш персонаж", value=role, inline=False)
            user_embed.add_field(name="Гейм мастер", value=game_master.mention, inline=False)
            user_embed.add_field(name="Пожелание", value="Удачи в игре и получайте удовольствие!", inline=False)

            try:
                await member.send(embed=user_embed)
            except disnake.errors.HTTPException:
                await ctx.send(f"Не удалось отправить личное сообщение {member.mention}. Убедитесь, что у вас открыты личные сообщения.", ephemeral=True)

        await ctx.response.send_message("Игровая сессия создана и личные сообщения отправлены.", ephemeral=True)

def setup(bot):
    print("\nSessionCog ready")
    bot.add_cog(SessionCog(bot))