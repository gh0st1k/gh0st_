from turtle import position
from disnake.ui import Button
from unicodedata import category
import disnake
from disnake.ext import commands

class private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def private(self, ctx):
        category=await ctx.guild.create_category(name="Приватные комнаты")
        
        await ctx.guild.create_voice_channel(name='Приватные комната', category=category)
        emb = disnake.Embed(title="Приватные комнаты успешно созданы!", description=f"Создано администратором: {ctx.author}")
        emb.set_author(name="Удачи!")
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_voice_state_update(self, ctx, before, after):
        if before.channel is None and after.channel is not None:
            category = await ctx.guild.create_category(name="Приватные комнаты")
            await ctx.guild.create_voice_channel(name='Приватная комната', category=category)



def setup(bot):
    bot.add_cog(private(bot))
    print('Комнаты в работе..')