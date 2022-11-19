import os
import disnake
from disnake.ext import commands
import sqlite3
from disnake.ui import Button, View, Select
from disnake import TextInput, TextInputStyle
import time


connection = sqlite3.connect('base.db')
cursor = connection.cursor()

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Добавление роли")
    @commands.has_guild_permissions(administrator=True)
    async def add_role(inter: disnake.AppCmdInter, role: disnake.Role, amount: int):
        cursor.execute(f"INSERT INTO shop VALUES ({role.id}, {amount}, {inter.guild.id})")
        await inter.send(embed=disnake.Embed(title="Роль успешно добавлена!", description=f"Роль **{role}** успешно добавлена в магазин! Стоимость роли **{amount}**"), ephemeral=True)


    @commands.slash_command(description="Магазин ролей")
    async def shop(self, inter: disnake.AppCmdInter):
        embed=disnake.Embed(title="Магазин", description="Магазин ролей которые выставление администратором либо модератором", color=disnake.Color.dark_gold())

        for row in cursor.execute(f"SELECT role_id, role_amount FROM shop WHERE guild_id = {inter.guild.id}"):
            if inter.guild.get_role(row[0]) != None:
                embed.add_field(name=f"Роль: **{inter.guild.get_role(row[0]).mention}**", value=f"Стоимость: **{row[1]}**")

        await inter.send(embed=embed, ephemeral=True)

    @commands.slash_command(description="Баланс пользователя")
    async def balance(self, inter: disnake.AppCmdInter, member: disnake.Member):
        embed=disnake.Embed(title=f"Баланс пользователя: {member}", description="""Его баланс: **{}**""".format(cursor.execute(f"SELECT cash FROM economy WHERE member_id = {member.id}")), color=disnake.Color.dark_gold())
        embed.add_field(name="Его лвл:", value="""**{}**""".format(cursor.execute(f"SELECT lvl FROM economy WHERE member_id = {member.id}").fetchone()[0]))
        await inter.send(embed=embed, ephemeral=True)
    
    @commands.slash_command(description="Перевод денег пользователю")
    async def pay(inter: disnake.AppCmdInter, member: disnake.Member, amount: int):
        view=YN(member, amount)
        if amount > cursor.execute(f"SELECT cash FROM economy WHERE member_id = {member.id}"):
            await inter.send(embed=disnake.Embed(title="EROR &40051", description="Вы указали сумму больше, чем у вас есть", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        if member.bot is True:
            await inter.send(embed=disnake.Embed(title="EROR &40052", description="Вы не можете передать деньги боту!", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        if member is inter.author:
            await inter.send(embed=disnake.Embed(title="EROR &40053", description="Вы не можете передать деньги самому себе.", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        else:
            await inter.send(embed=disnake.Embed(title=f"Пользователь {member}", description="Вы уверены что хотите передать деньги этому пользователю?", color=disnake.Color.dark_gold()), view=view, ephemeral=True)
    
class YN(View):
    def __init__(self, member: disnake.Member, amount: int):
        super().__init__()
        self.member = member
        self.amount = amount

    @disnake.ui.button(label="Да", style=disnake.ButtonStyle.green, custom_id="Y")
    async def Y_button_callback(self, button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message(embed=disnake.Embed(title="Успешно!", description=f"Вы перевели пользователю: **{self.member}** столько монет: **{self.amount}**", color=disnake.Color.dark_gold()), ephemeral=True)
        cursor.execute(f"UPDATE cash SET cash = cash + {self.amount} WHERE member_id = {self.member.id}")
    
    @disnake.ui.button(label="Нет", style=disnake.ButtonStyle.red, custom_id="N")
    async def N_button_callback(self, button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message(embed=disnake.Embed(title="Успешно!", description="Вы отменили перевод монет", color=disnake.Color.dark_gold()), ephemeral=True)

    
def setup(bot):
    bot.add_cog(economy(bot))
    print('Економика в норме...')