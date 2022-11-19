
import disnake
from disnake.ext import commands
from disnake.ui import Button, View, Select
import sqlite3

bot = commands.Bot(command_prefix='&', intents=disnake.Intents.all())
connection = sqlite3.connect('base.db')
cursor = connection.cursor()

class dgshop(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.slash_command(description="Купить DG-shop")
    async def buydg(self, inter: disnake.AppCmdInter):
        view = View()

        select = Select(placeholder="Вибери заказ", options=[
            disnake.SelectOption(emoji=None, label="Аватарка", description="Ава для дс, тг, ютуба.", value="0x0"),
            disnake.SelectOption(emoji=None, label="Логотип", description="Логотип для дс, тг, ютуба.", value="0x1"),
            disnake.SelectOption(emoji=None, label="Шапка", description="Шапка для ютуба.", value="0x2"),
            disnake.SelectOption(emoji=None, label="Превью", description="Превью для ютуба и для тг.", value="0x3"),
            disnake.SelectOption(emoji=None, label="Ютуб Пак", description="Входит: аватарка, шапка", value="0x4"),
            disnake.SelectOption(emoji=None, label="Превью Пак", description="Входит: 3 превьюшки", value="0x5"),
            disnake.SelectOption(emoji=None, label="Фулл Пак", description="Входит: аватарка, шапка, логотип, превью", value="0x6")
        ])
        async def select1_callback(interaction):
            if select.values[0] == "0x0":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 5грн/8руб/0,14dollars", description="Теперь ВСЕ что хочешь добавить в свою аватарку, через команду ```&dgina <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x1":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 23грн/40руб/0,62dollars", description="Теперь ВСЕ что хочешь добавить в свое лого напиши через команду ```&dginl <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x2":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 9грн/15руб/0,24dollars", description="Теперь ВСЕ что хочешь добавить в свою шапку напиши через команду ```&dginh <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x3":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 13грн/22руб/0,35dollars", description="Теперь ВСЕ что хочешь добавить в свое превью напиши через команду ```&dginp <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x4":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 10грн/17руб/0,27dollars", description="В свой ЮтубПак напиши что хочешь видеть паке```&dginpy <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x5":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 25грн/42руб/0,68dollars", description="В свой ПревьюПак напиши что хочешь видеть в паке```&dginpp <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
            if select.values[0] == "0x6":
                await interaction.response.send_message(embed=disnake.Embed(title="ЦЕНА: 35грн/59руб/0,95dollars", description="В свой ФуллПак напиши что хочешь видеть в паке```&dginfp <text>``` и обезательно впиши свой дискорд!", color=disnake.Color.dark_purple()))
        select.callback = select1_callback

        view.add_item(select)
        await inter.send(embed=disnake.Embed(title="Привет!", description="Ты ввел эту команду чтоб купить аву, шапку, логотип, превью. Виберы снизу что хочешь заказать (У нас есть и паки!)", color=disnake.Color.dark_gold()), view=view, ephemeral=True)

    @commands.command()
    async def shopdg(self, ctx):
        await ctx.send(embed=disnake.Embed(title="Цены DG-shop", color=disnake.Color.dark_purple()))

    @commands.command()
    async def dgina(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO avatar VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginl(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO logo VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginh(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO hapka VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()
    
    @commands.command()
    async def dginp(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO preview VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginpy(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO ytpack VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginpy(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO ytpack VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginpp(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO prpack VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

    @commands.command()
    async def dginfp(self, ctx, text: str):
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Успешно отправлено продвцам ваши пожелания по товару. Ожидайте!", color=disnake.Color.dark_purple()))
        cursor.execute(f"INSERT INTO fullpack VALUES ('{text}', '{ctx.author.id}')")
        connection.commit()

def setup(bot):
    bot.add_cog(dgshop(bot))

