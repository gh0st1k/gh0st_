from asyncio import sleep
import random
import time
import disnake
from disnake.ext import commands
from disnake.ui import Button, View, Select
import disnake.ui
import sqlite3
import config

class funny(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fight(self, ctx, member: disnake.Member):
        if member.bot is True:
            await ctx.send(embed = disnake.Embed(title="EROR &40031", description="Нельзя ударить бота!", color=disnake.Color.dark_gold()))
            return
        if member == 1013189601025871874:
            await ctx.send(embed = disnake.Embed(title="EROR &00001", description="Мразь ебучая ты не прихуела меня бить? Я блять тут стараюсь, команды вивожу а ты блять со мной так? Ахуела совсем.", color=disnake.Color.dark_gold()))
            return
        if member is ctx.author:
            await ctx.send(embed = disnake.Embed(title="EROR &40036", description="Вы не можете ударить самого себя.", color=disnake.Color.dark_gold()))
            return
        else:
            emb = disnake.Embed(title="Удар!", description=f"Вы ударили пользователя ```{member}```", color=disnake.Color.dark_red())
            emb.set_image(url= random.choice(config.fight_gif))
            await ctx.send(embed=emb)
            time.sleep(120)

    @commands.command()
    async def kiss(self, ctx, member: disnake.Member):
        if member.bot is True:
            await ctx.send(embed = disnake.Embed(title="EROR &40031", description="Нельзя поцеловать бота!", color=disnake.Color.dark_gold()))
            return
        if member is ctx.author:
            await ctx.send(embed = disnake.Embed(title="EROR &40036", description="Вы не можете поцеловать самого себя.", color=disnake.Color.dark_gold()))
            return
        else:
            emb = disnake.Embed(title="Поцелуй!", description=f"Вы поцеловали пользователя {member}", color=disnake.Color.dark_purple())
            emb.set_image(url=random.choice(config.kiss_gif))
            await ctx.send(embed=emb)
            time.sleep(120)

    @commands.command()
    async def seks(self, ctx, member:disnake.Member):
        if member.bot is True:
            await ctx.send(embed=disnake.Embed(title="EROR &40031", description="Ебанулься?", color=disnake.Color.dark_gold()))
            return
        if member is ctx.author:
            await ctx.send(embed=disnake.Embed(title="EROR &40036", description="Вы не можете заняться сексом з самим собой. Только дрочить)", color=disnake.Color.dark_gold()))
            return
        else:
            emb=disnake.Embed(title="Ах-ах", description=f"Вы занялись сексом з пользователем **{member}**",  color=disnake.Color.dark_purple())
            emb.set_image(url=random.choice(config.seks_gif))
            await ctx.send(embed=emb)
            time.sleep(120)

    @commands.command()
    async def minet(self, ctx, member: disnake.Member):
        if member.bot is True:
            await ctx.send(embed=disnake.Embed(title="EROR &40031", description="Ебанулься?", color=disnake.Color.dark_gold()))
            return
        if member is ctx.author:
            await ctx.send(embed=disnake.Embed(title="EROR &40036", description="Вы не можете зделать себе минет.", color=disnake.Color.dark_gold()))
            return
        else:
            emb=disnake.Embed(title="Мммм", description=f"Вы зделали минет пользователю **{member}**",  color=disnake.Color.dark_purple())
            await ctx.send(embed=emb)
            time.sleep(120)

    @commands.command()
    async def menurp(self, ctx):
        await ctx.send(embed=disnake.Embed(title="Фанни команды", description=config.funny_commands, color=disnake.Color.dark_gold()))


    # Slash commands
    @commands.slash_command(description="Побить пользователя")
    async def fight(self, inter: disnake.AppCmdInter, member: disnake.Member):
        if member.bot is True:
            await inter.send(embed = disnake.Embed(title="EROR &40031", description="Нельзя ударить бота!", color=disnake.Color.dark_gold()))
            return
        if member == 1013189601025871874:
            await inter.send(embed = disnake.Embed(title="EROR &00001", description="Мразь ебучая ты не прихуела меня бить? Я блять тут стараюсь, команды вивожу а ты блять со мной так? Ахуела совсем.", color=disnake.Color.dark_gold()))
            return
        if member is inter.author:
            await inter.send(embed = disnake.Embed(title="EROR &40036", description="Вы не можете ударить самого себя.", color=disnake.Color.dark_gold()))
            return
        else:
            emb = disnake.Embed(title="Удар!", description=f"Вы ударили пользователя ```{member}```", color=disnake.Color.dark_red())
            emb.set_image(url= random.choice(config.fight_gif))
            await inter.send(embed=emb)
            time.sleep(120)

    @commands.slash_command(description="Поцеловать пользователя")
    async def kiss(self, inter: disnake.AppCmdInter, member: disnake.Member):
        if member.bot is True:
            await inter.send(embed = disnake.Embed(title="EROR &40031", description="Нельзя поцеловать бота!", color=disnake.Color.dark_gold()))
            return
        if member is inter.author:
            await inter.send(embed = disnake.Embed(title="EROR &40036", description="Вы не можете поцеловать самого себя.", color=disnake.Color.dark_gold()))
            return
        else:
            emb = disnake.Embed(title="Поцелуй!", description=f"Вы поцеловали пользователя {member}", color=disnake.Color.dark_purple())
            emb.set_image(url=random.choice(config.kiss_gif))
            await inter.send(embed=emb)
            time.sleep(120)

    @commands.slash_command(description="Заняться любовью")
    async def seks(self, inter: disnake.AppCmdInter, member:disnake.Member):
        if member.bot is True:
            await inter.send(embed=disnake.Embed(title="EROR &40031", description="Ебанулься?", color=disnake.Color.dark_gold()))
            return
        if member is inter.author:
            await inter.send(embed=disnake.Embed(title="EROR &40036", description="Вы не можете заняться сексом з самим собой. Только дрочить)", color=disnake.Color.dark_gold()))
            return
        else:
            emb=disnake.Embed(title="Ах-ах", description=f"Вы занялись сексом з пользователем **{member}**",  color=disnake.Color.dark_purple())
            emb.set_image(url=random.choice(config.seks_gif))
            await inter.send(embed=emb)
            time.sleep(120)

    @commands.slash_command(description="Зделать приятно пользователю")
    async def minet(self, inter: disnake.AppCmdInter, member: disnake.Member):
        if member.bot is True:
            await inter.send(embed=disnake.Embed(title="EROR &40031", description="Ебанулься?", color=disnake.Color.dark_gold()))
            return
        if member is inter.author:
            await inter.send(embed=disnake.Embed(title="EROR &40036", description="Вы не можете зделать себе минет.", color=disnake.Color.dark_gold()))
            return
        else:
            emb=disnake.Embed(title="Мммм", description=f"Вы зделали минет пользователю **{member}**",  color=disnake.Color.dark_purple())
            await inter.send(embed=emb)
            time.sleep(120)

    @commands.slash_command(description="Меню фанни команд")
    async def menuf(self, inter: disnake.AppCmdInter):
        await inter.send(embed=disnake.Embed(title="Фанни команды", description=config.funny_commands, color=disnake.Color.dark_gold()))

def setup(client):
    client.add_cog(funny(client))
