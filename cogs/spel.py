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

class SpellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot






def setup(bot):
    print("\nspells ready")
    bot.add_cog(SpellCog(bot))