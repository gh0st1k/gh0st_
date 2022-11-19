import disnake
from disnake.ext import commands
from disnake.ui import Button, Select, View, TextInput
import time
from time import sleep
import random
import sqlite3

connection = sqlite3.connect('base.db')
cursor = connection.cursor()

class rpcommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Магазин самооборони (Для защиты от атак)")
    async def shoppvp(inter: disnake.AppCmdInter):
        emb = disnake.Embed(title="Магазин", description="Здесь вы сможете приобрести турели, щиты на 24, 48 и 64 часа. Также вы сможете купить допополнение к своей базе. Удачи!", color=disnake.Color.dark_gold())
        emb.add_field(name="Турель", value="1000")


    @commands.slash_command(description="Атака на пользователя")
    async def atack(inter: disnake.AppCmdInter, member: disnake.Member):
        view = Att(member)
        await inter.send(embed=disnake.Embed(title=f"Атака на {member}", description=f"Вы точно хотите напасть на пользователя **{member}**?", color=disnake.Color.dark_gold()), view=view, ephemeral=True)

class Att(View):
    def __init__(self, member: disnake.Member):
        super().__init__()
        self.member = member

    @disnake.ui.button(label="Да", style=disnake.ButtonStyle.green, custom_id="Y")
    async def Y_button_callback(self, button, inter: disnake.MessageInteraction):
        embed=disnake.Embed(title=f"Введеться атака на {self.member}!", color=disnake.Color.dark_gold())
        embed.add_field(name="Ваши силы:", value="**{}**".format(cursor.execute(f"SELECT forces FROM economy WHERE member_id = {inter.author.id}").fetchone()[0]))
        embed.add_field(name="Всего турелей:", value="**{}**".format(cursor.execute(f"SELECT turret FROM economy WHERE member_id = {inter.author.id}").fetchone()[0]))
        await inter.send(embed=embed)

    @disnake.ui.button(label="Нет", style=disnake.ButtonStyle.red, custom_id="N")
    async def N_button_callback(self, button, inter: disnake.MessageInteraction):
        await inter.send(embed=disnake.Embed(title="Отмена", description=f"Вы отменили атаку на пользователя: {self.member}. Правильное решение или нет, решай сам.", color=disnake.Color.dark_gold()), ephemeral=True)

def setup(client):
    client.add_cog(rpcommands(client))