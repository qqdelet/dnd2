import disnake
from disnake.ext import commands
from typing import Callable, Optional
from Paginator import Pagination, L

pages = {
    1: "https://media.discordapp.net/attachments/1173430202022498334/1221079015805292564/cain.jpg?ex=66114573&is=65fed073&hm=bbc124f4c151e0a8a5c00b80b765ee23e28aa6c892a271e23a21be32eedf60c3&=&format=webp&width=745&height=676",
    2: "https://media.discordapp.net/attachments/1173430202022498334/1221079017004859482/meretrix.jpg?ex=66114574&is=65fed074&hm=d1f395d1b7b6b0e4b758d72beb7a1ff4e722ede59ad435fb9c7a656926eb6f04&=&format=webp&width=745&height=676",
    3: "https://media.discordapp.net/attachments/1173430202022498334/1221079016652542042/Medicus.png?ex=66114574&is=65fed074&hm=8580873283e44378e68869321cbdf7f92aa18d0a6641f5f0afe88083a49f8896&=&format=webp&quality=lossless&width=745&height=676",
    4: "https://media.discordapp.net/attachments/1173430202022498334/1221079017398997002/Nolla.png?ex=66114574&is=65fed074&hm=d489bd3758780f2fc3467b8c7c1701b720a21c049ac411365802939b7d7d6a47&=&format=webp&quality=lossless&width=745&height=676",
    5: "https://media.discordapp.net/attachments/1173430202022498334/1221079015431868427/Bella.png?ex=66114573&is=65fed073&hm=1df7461fe7af8eb29fc3bafaf22aa84bcfe040346b177b0c14bdd0835f41f758&=&format=webp&quality=lossless&width=745&height=676",
    6: "https://media.discordapp.net/attachments/1173430202022498334/1221079016253952090/Eleonora.png?ex=66114574&is=65fed074&hm=c2e16fb243ba433e1676629fb2bdb3b390e85cbaedc9db2d15fd3f0e00faf91f&=&format=webp&quality=lossless&width=745&height=676"
}

class ShowP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="show", description="Покажет вам всех игровых персонажей")
    async def show(self, interaction):
        async def get_page(page: int):
            n = Pagination.compute_total_pages(5, L)
            emb = disnake.Embed(title="Карточки персонажей", description="", color=0x839cff)
            emb.set_footer(text=f"Page {page} from {n}")
            emb.set_image(url=pages[page])
            return emb, n
        await Pagination(interaction, get_page).navegate()

def setup(bot):
    print("sp ready")
    bot.add_cog(ShowP(bot))
