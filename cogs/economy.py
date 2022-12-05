import os
import disnake
from disnake.ext import commands
import sqlite3
from disnake.ui import Button, View, Select
from disnake import TextInput, TextInputStyle
import time
import random
import config

bot = commands.Bot(command_prefix='&', intents=disnake.Intents.all())
connection = sqlite3.connect('base.db')
cursor = connection.cursor()

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ежедневная награда!")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def reward(self, inter: disnake.AppCmdInter):
        await inter.send(embed=disnake.Embed(title="Успешно!", description="Вы получили награду в размере **{}**. Следуйщею награду можно получить через **24 часа**".format(cursor.execute("SELECT reward FROM economy_reward WHERE guild_id = ?", [inter.author.id]).fetchone()[0])), ephemeral=True)
        cursor.execute("UPDATE economy SET cash = cash + ? WHERE member_id = ?", [cursor.execute("SELECT reward FROM economy_reward WHERE guild_id = ?", [inter.guild.id]), inter.author.id])
        connection.commit()
    @reward.error
    async def reward_error(error, inter: disnake.AppCmdInter):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send(embed=disnake.Embed(title="ERROR 40054", description=f"Подождите ещё {error.retry_after:.2f}!", color=disnake.Color.dark_gold()), ephemeral=True)
 
    @commands.slash_command(description="Выдавать сумму пользователю (только могу админы и модеры)")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def amount(self, inter: disnake.AppCmdInter, member: disnake.Member, amount: int):
        cursor.execute(f"UPDATE economy SET cash = cash + ? WHERE member_id = ?", [amount, member.id])
        await inter.send(embed=disnake.Embed(title="Успешно!", description=f"Вы успешно перевели деньги {amount} пользователю {member.mention}", color=disnake.Color.dark_gold()), ephemeral=True)
    @amount.error
    async def amount_error(self, error, inter: disnake.AppCmdInter):
        if isinstance(error, commands.MissingPermissions):
            await inter.send(embed=disnake.Embed(title="ERROR &40051", description="Недостаточно прав чтоб использовать эту команду", color=disnake.Color.dark_gold()), ephemeral=True)

    @commands.slash_command(description="Установка размер ежедневной награды")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def economy_set_reward(self, inter: disnake.AppCmdInter, reward: int):
        if reward < 100000 and cursor.execute("SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id]) is None:
            await inter.send(embed=disnake.Embed(title="ERROR 40055", description="Лимит награды становит **100к**.", color=disnake.Color.dark_gold()), ephemeral=True)
        cursor.execute(f"INSERT INTO economy_reward VALUES (?, ?)", [reward, inter.guild.id])
        await inter.send(embed=disnake.Embed(title="Успешно!", description=f"Вы успешно установили размер (размер награды **{reward}**) ежедневной награды", color=disnake.Color.dark_gold()), ephemeral=True)
        connection.commit()
    @economy_set_reward.error
    async def economy_set_reward_error(error, inter: disnake.AppCmdInter):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send(embed=disnake.Embed(title="ERROR 40054", description="Подождите некоторое время", color=disnake.Color.dark_gold()), ephemeral=True)

    @commands.slash_command(description="Работа (каждые 24 часа)")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def work(self, inter: disnake.AppCmdInter):
        ran1 = [100, 200, 250, 350, 500, 750, 1000]
        ran = random.choice(ran1)
        cursor.execute(f"UPDATE economy SET cash = cash + ? WHERE member_id = ?", [ran, inter.author.id])
        await inter.send(embed=disnake.Embed(title="Ваша работа..", description=f"**{random.choice(config.work)}**! \n Ваша зарплата: {ran}", color=disnake.Color.dark_gold()), ephemeral=True)
        connection.commit()
    @work.error
    async def work_error(self, error, inter: disnake.AppCmdInter):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send(embed=disnake.Embed(title="ERROR 40054", description=f"Подождите ещё **{error.retry_after:.2f}**", color=disnake.Color.dark_gold()), ephemeral=True)

    @commands.slash_command(description="Купить роль из магазина")
    async def buy(self, inter: disnake.AppCmdInter, role: disnake.Role):
        if cursor.execute(f"SELECT role_id FROM shop WHERE role_id = ?", [role.id]).fetchone() is None:
            await inter.send(embed=disnake.Embed(title="ERROR ", description="Нету такой роли в магазине", color=disnake.Color.dark_gold()), ephemeral=True)
        
        role = inter.guild.get_role(role.id)
        await inter.author.add_roles(role)
        cursor.execute(f"DELETE FROM shop WHERE role_id = {role.id}")
        await inter.send(embed=disnake.Embed(title="Успешно!", description="Вы успешно купили роль из магазина. Роль: <@{}>, стоимость роли: **{}**".format(cursor.execute(f"SELECT role_id FROM shop WHERE role_id = ?", [role.id]).fetchone()[0], cursor.execute(f"SELECT role_amount FROM shop WHERE role_id = ?", [role.id]).fetchone()[0]), color=disnake.Color.dark_gold()), ephemeral=True)

    @commands.slash_command(description="Поставить емодзи валюти")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def economy_set_emoji(self, inter: disnake.AppCmdInter, emoji: str):
        if cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = {inter.guild.id}").fetchone() is not None:
            await inter.send(embed=disnake.Embed(title="ERROR 6000", description="На этом сервере есть емоджи валюты, чтоб его убрать используйте команду **/economy_remove_emoji**.", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        else:
            cursor.execute(f"INSERT INTO economy_emoji VALUES ('{emoji}', {inter.guild.id})")
            await inter.send(embed=disnake.Embed(title="Успешно!", description=f"Вы успешно поставили емоджи **{emoji}** в економику!", color=disnake.Color.dark_gold()), ephemeral=True)
            connection.commit()

    @commands.slash_command(description="Удалить емоджи валюти")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def economy_remove_emoji(self, inter: disnake.AppCmdInter):
        if cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = {inter.guild.id}").fetchone() is None:
            await inter.send(embed=disnake.Embed(title="ERROR ", description="На этом сервере нету емодзи валюти, установите емодзи командой **/economy_set_emoji**.", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        else:
            cursor.execute(f"DELETE FROM economy_emoji WHERE guild_id = {inter.guild.id}")
            await inter.send(embed=disnake.Embed(title="Успешно!", description="Вы успешно удалили емодзи валюти", color=disnake.Color.dark_gold()), ephemeral=True)
            connection.commit()

    @commands.slash_command(description="Убирает роль из магазина")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def shop_remove_role(self, inter: disnake.AppCmdInter, role: disnake.Role):
        cursor.execute(f"DELETE FROM shop WHERE role_id = ?", [role.id])
        await inter.send(embed=disnake.Embed(title="Успешно!", description=f"Вы успешно удалили роль из магазина, роль: {role.mention}", color=disnake.Color.dark_gold()), ephemeral=True)
        connection.commit()

    @commands.slash_command(description="Добавление роль в магазин")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def shop_add_role(self, inter: disnake.AppCmdInter, role: disnake.Role, amount: int):
        cursor.execute(f"INSERT INTO shop VALUES (?, ?, ?)", [role.id, amount, inter.guild.id])
        if cursor.execute(f"SELECT member_id FROM economy WHERE member_id=?", [inter.author.id]).fetchone() is not None:
            await inter.send(embed=disnake.Embed(title="Роль успешно добавлена!", description="Роль {} успешно добавлена в магазин! Стоимость роли **{}{}**".format(role.mention, amount, cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id]).fetchone()[0]), color=disnake.Color.dark_gold()), ephemeral=True)
            connection.commit()

    @commands.slash_command(description="Магазин ролей")
    async def shop(self, inter: disnake.AppCmdInter):
        embed=disnake.Embed(title="Магазин", description="Магазин ролей которые выставление администратором либо модератором", color=disnake.Color.dark_gold())
        if cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id]).fetchone() is not None:
            for row in cursor.execute(f"SELECT role_id, role_amount FROM shop WHERE guild_id = ?", [inter.guild.id]):
                if inter.guild.get_role(row[0]) != None:
                    embed.add_field(name="Стоимость: **{}{}**".format(row[1],cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id]).fetchone()[0]), value=f"Роль: **{inter.guild.get_role(row[0]).mention}**", inline=True)
            await inter.send(embed=embed, ephemeral=True)
            connection.commit()
        else:
            for row in cursor.execute(f"SELECT role_id, role_amount FROM shop WHERE guild_id = ?", [inter.guild.id]):
                if inter.guild.get_role(row[0]) != None:
                    embed.add_field(name="Стоимость: **{}**".format(row[1]), value=f"Роль: **{inter.guild.get_role(row[0]).mention}**", inline=True)
            await inter.send(embed=embed, ephemeral=True)
            connection.commit()

    # @shop.error
    #async def shop_error(error, inter: disnake.AppCmdInter):
        # if isinstance(error, )

    @commands.slash_command(description="Баланс пользователя")
    async def balance(self, inter: disnake.AppCmdInter, member: disnake.Member):
        if cursor.execute("SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id]) is None:
            embed=disnake.Embed(title=f"Баланс пользователя: {member}", description="""Его баланс: **{}**""".format(cursor.execute(f"SELECT cash FROM economy WHERE member_id = {member.id}").fetchone()[0]), color=disnake.Color.dark_gold())
            embed.add_field(name="Его лвл:", value="""**{}**""".format(cursor.execute(f"SELECT lvl FROM economy WHERE member_id = ?", [member.id]).fetchone()[0], cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id])))
            await inter.send(embed=embed, ephemeral=True)
        else:
            embed=disnake.Embed(title=f"Баланс пользователя: {member}", description="""Его баланс: **{}{}**""".format(cursor.execute(f"SELECT cash FROM economy WHERE member_id = {member.id}").fetchone()[0], cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = {inter.guild.id}").fetchone()[0]), color=disnake.Color.dark_gold())
            embed.add_field(name="Его лвл:", value="""**{}**""".format(cursor.execute(f"SELECT lvl FROM economy WHERE member_id = ?", [member.id]).fetchone()[0], cursor.execute(f"SELECT emoji_id FROM economy_emoji WHERE guild_id = ?", [inter.guild.id])))
            await inter.send(embed=embed, ephemeral=True)
    
    @commands.slash_command(description="Перевод денег пользователю")
    async def pay(self, inter: disnake.AppCmdInter, member: disnake.Member, amount: int):
        if amount > cursor.execute(f"SELECT cash FROM economy WHERE member_id = {inter.author.id}").fetchone()[0]:
            await inter.send(embed=disnake.Embed(title="ERROR &40051", description="Вы указали сумму больше, чем у вас есть", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        if member.bot is True:
            await inter.send(embed=disnake.Embed(title="ERROR &40052", description="Вы не можете передать деньги боту!", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        if member is inter.author:
            await inter.send(embed=disnake.Embed(title="ERROR &40053", description="Вы не можете передать деньги самому себе.", color=disnake.Color.dark_gold()), ephemeral=True)
            return
        else:
            cursor.execute(f"UPDATE economy SET cash = cash + ? WHERE member_id = ?", [amount, member.id])
            cursor.execute(f"UPDATE economy SET cash = cash - ? WHERE member_id = ?", [amount, inter.author.id])
            await inter.send(embed=disnake.Embed(title=f"Успешно!", description=f"Вы успешно перевели пользователю {member.mention} сумму **{amount}**", color=disnake.Color.dark_gold()), ephemeral=True)
            connection.commit()

    
def setup(bot):
    bot.add_cog(economy(bot))
    print('Економика в норме...')
