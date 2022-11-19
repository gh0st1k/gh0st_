from asyncio import sleep
import asyncio

import disnake
from disnake.ui import Select, View, Button
from disnake.ext import commands
import disnake.ext.commands
from disnake.utils import get
import random
from disnake import TextInput, TextInputStyle
from discord.ext import tasks

import config
from config import economy_commands
from config import TOKEN
from config import moderator_commands
import os
import sqlite3
import time

connection = sqlite3.connect('base.db')
cursor = connection.cursor()


bot = commands.Bot(command_prefix='&', intents=disnake.Intents.all())

# Cogs
@bot.command()
async def load(ctx, extension):
    if ctx.author.id != 825815799654514709:
        await ctx.send(embed=disnake.Embed(title="Упс...", description="Вы не розробтчик бот!", color=disnake.Color.dark_gold()))
    else:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Вы успешно загрузили коги!", color=disnake.Color.dark_blue()))

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id != 825815799654514709:
        await ctx.send(embed=disnake.Embed(title="Упс...", description="Вы не розробтчик бот!", color=disnake.Color.dark_gold()))
    else:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Вы успешно удалили коги!", color=disnake.Color.dark_blue()))

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id != 825815799654514709:
        await ctx.send(embed=disnake.Embed(title="Упс...", description="Вы не розробтчик бот!", color=disnake.Color.dark_gold()))
    else:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(embed=disnake.Embed(title="Успешно!", description="Вы успешно перезагрузили коги!", color=disnake.Color.dark_blue()))

@bot.event
async def on_guild_join(ctx):
    embed=disnake.Embed(title="Привет!", description="Приветсвую всех кто есть на Вашём сервере! Меня добавили сюда не просто так, ладно, роскажу какие у меня есть команды (Также все команды есть и на слеш командах)", color=disnake.Color.dark_gold())
    embed.add_field(name="Все команды можно посмотреть командой &menu или слеш командой.", value=config.general_commands)
    embed.add_field(name="Чем этот бот особеный?", value="1. Можно выбрать язык дискорд сервера. Потдержуються: Україньскій, Руский, English языки. По умолчанию стоит руский язык. \n")
    await ctx.send(embed=embed)

# Events

@bot.event
async def on_ready():
# BD

    cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
        role_id INT,
        role_amount INT,
        guild_id INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS economy(
        member TEXT,
        member_id INT,
        guild_id INT,
        cash INT,
        lvl INT,
        warns INT,
        forces INT,
        turret INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS avatar(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS logo(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS hapka(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS preview(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS ytpack(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS prpack(
        text TEXT,
        member INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS fullpack(
        text TEXT,
        member INT
    )""")
    
    for guild in bot.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT member_id FROM economy WHERE member_id = {member.id}").fetchone() is None:
                    cursor.execute(f"INSERT INTO economy VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (str(member), member.id, guild.id, 0, 1, 0, 0))
                else:
                    pass
            connection.commit()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS guilds(
        server_id INT,
        guild_name TEXT,
        general_member_in_guild TEXT,
        members_guild TEXT,
        descreption_guild TEXT
    )""")

    connection.commit()

# Text on_ready

    probl = ' ' * 25

    print('%s -БОТ АКТИВИРОВАН НА СЕРВЕРАХ-' % probl)
    print(f'Имя бота: {bot.user}')
    print(f'Айди бота: {bot.user.id}')
    print(f'Используеться на серверах: {len(bot.guilds)}')
    

    await bot.change_presence(status=disnake.Status.dnd,activity=disnake.Streaming(name=f'{len(set(bot.get_all_members()))} участников',url='https://www.twitch.tv/gh0st1k_csgo'))


# Moderator commands
# kick


@bot.slash_command(title="kick", description="Кикает пользователя")
@commands.has_permissions(administrator = True)
async def kick(inter: disnake.AppCmdInter, member: disnake.Member, *, reason):
    if reason == None:
        await inter.send(embed=disnake.Embed(title = "EROR $40034", description = "Вы не указали причину кика.", color = disnake.Color.dark_gold()), ephemeral=True)
        return
    if member.bot == True:
        await inter.send(embed=disnake.Embed(title = "EROR $40038", description = "Вы не можете кикнуть бота.", color = disnake.Color.dark_gold()), ephemeral=True)
        return
    if member == inter.send:
        await inter.send(embed=disnake.Embed(title= "EROR $40042", description="Вы не можете кикнуть самого себя!", color=disnake.Colour.dark_gold()), ephemeral=True)
        return
    else:
        await member.kick(reason=reason)
        embed=disnake.Embed(title=f"Обидчик был успешно кикнут!", color=disnake.Color.dark_blue())
        embed.add_field(name="Причина кика:", value=f"```{reason}```")
        await inter.send(embed=embed, ephemeral=True)

#Ban and Unban commands

@bot.command(pass_context=True)
@commands.has_permissions(administrator = True, ban_members = True)
async def ban(inter: disnake.AppCmdInter, member: disnake.Member = None, time: int = None,*, reason: str = None):
    if member is None:
        emb = disnake.Embed(title="Как пользоваться командой &ban.", description="Нужно указать пользователя которого надо забанить", color=disnake.Color.dark_gold())
        emb.add_field(name="&ban <member>", value="**<member>** - учасник которого хотите забанить")
        emb.add_field(name="&ban <member> <reason>", value="**<reason>** - причина бана, ее можно и не указывать")
        msg = await inter.send(embed=emb, ephemeral=True)
        await sleep(15)
        await msg.delete()
        return 
    if reason is None:
        emb = disnake.Embed(title="Как пользоваться командой &ban.", description="Нужно указать пользователя которого надо забанить", color=disnake.Color.dark_gold())
        emb.add_field(name="&ban <member>", value="**<member>** - учасник которого хотите забанить")
        emb.add_field(name="&ban <member> <reason>", value="**<reason>** - причина бана, ее можно и не указывать")
        msg = await inter.send(embed=emb)
        await sleep(15)
        await msg.delete()
        return
    if member.bot == True:
        await inter.reply(embed=disnake.Embed(title = "EROR $40038", description = "Вы не можете забанить бота.", color = disnake.Color.dark_gold()))
        return
    if member == inter.author:
        await inter.send(embed=disnake.Embed(title= "EROR $40042", description="Вы не можете забанить самого себя!", color=disnake.Colour.dark_gold()))
        return
    if time is None:
        await inter.send(embed=disnake.Embed(title= "EROR $40049", description="Вы не указали время бана.", color=disnake.Colour.dark_gold()))
        return
    else:
        await member.ban()
        emb = disnake.Embed(title= f"Нарушитель был успешно забанен!", color=disnake.Colour.dark_blue())
        emb.add_field(name="Причина бана:", value=f"```{reason}```")
        emb.add_field(name="Забанен пользователем:", value=f"```{inter.author}```")
        emb.add_field(name="Время бана:", value=f"```{time}```")
        msg = await inter.send(embed=emb)
        await asyncio.sleep(time * 60)
        await member.unban()
        await sleep(25)
        await msg.delete()

@bot.slash_command(title="Бан", description="Команда выдает бан пользователя")
@commands.has_permissions(administrator=True)
async def ban(inter: disnake.AppCmdInter, member: disnake.Member,time: int, reason = "Не указана"):
    if member.bot is True:
        await inter.send(embed=disnake.Embed(title = "EROR $40038", description = "Вы не можете забанить бота.", color = disnake.Color.dark_gold()), ephemeral=True)
        return
    if member is inter.author:
        await inter.send(embed=disnake.Embed(title= "EROR $40042", description="Вы не можете забанить самого себя!", color=disnake.Colour.dark_gold()), ephemeral=True)
        return
    if member.ban is True:
        await inter.send(embed=disnake.Embed(title= "EROR $40045", description="Пользователь уже находиться в бане!", color=disnake.Colour.dark_gold()), ephemeral=True)
        return
    if time is None:
        await inter.send(embed=disnake.Embed(title= "EROR $40049", description="Вы не указали время бана.", color=disnake.Colour.dark_gold()), ephemeral=True)
        return
    else:
        await member.ban()
        emb = disnake.Embed(title= f"Нарушитель был успешно забанен!", color=disnake.Colour.dark_blue())
        emb.add_field(name="Причина бана:", value=f"```{reason}```")
        emb.add_field(name="Забанен пользователем:", value=f"```{inter.author}```")
        emb.add_field(name="Время бана:", value=f"```{time}m```")
        await inter.send(embed=emb, ephemeral=True)
        await asyncio.sleep(time * 60)
        await member.unban()


@bot.slash_command(description="Разбанивает пользователя")
@commands.has_permissions(administrator=True)
async def unban(inter: disnake.AppCmdInter, id):

    user = await bot.fetch_user(id)

    try:
        await inter.guild.unban(user)
        emb=disnake.Embed(title= f"Пользователь был успешно розбанен!", color=disnake.Colour.dark_blue())
        emb.add_field(name="Ник пользователя..", value=f"```{user}```")
        await inter.send(embed=emb, ephemeral=True)
    except:
        msg = await inter.send(embed=disnake.Embed(title= "EROR $40036", description="Пользователь не был забанен!", color=disnake.Colour.dark_blue()), ephemeral=True)
        await sleep(25)
        await msg.delete()

# Mute and unmute commands

@bot.slash_command(title="Мут", description="Мутит пользователя")
@commands.has_permissions(manage_roles=True, ban_members=True, kick_members=True, administrator = True)
async def mute(inter: disnake.AppCmdInter, member: disnake.Member, time: int, reason="Не указана"):
    if member is inter.author:
        await inter.send(embed=disnake.Embed(title= "EROR $40042", description="Вы не можете замутить самого себя!", color=disnake.Colour.dark_gold()))
        return
    else:
        emb=disnake.Embed(title="Успешно!", description=f"Игрок замучен администатором/модератором: ```{inter.author}```", color=disnake.Color.dark_blue())
        emb.add_field(name="Пользователь замучен на:", value=f"```{time}m```")
        emb.add_field(name="Причина мута:", value=f"```{reason}```")
        await member.timeout(duration=time * 60)
        await inter.send(embed=emb)
        await member.move_to(channel=None)

@bot.slash_command(title="Размут", description="Команда размучивает пользователя")
@commands.has_permissions(administrator = True)
async def unmute(inter: disnake.AppCmdInter, member: disnake.Member):

    await member.timeout(duration=None)
    emb = disnake.Embed(title="Пользователь был размучен!", description="Пользователь размучен!", color=disnake.Color.dark_blue())
    emb.add_field(name="Был размучен пользователем..", value=f"```{inter.author}```", inline=True)
    await inter.send(embed=emb, ephemeral=True)

# General commands
# Profile command

@bot.slash_command(title="profile", description="Показывает профиль пользователяа")
async def profile(inter: disnake.AppCmdInter, member: disnake.Member, role=None):

    if str(member.status) == 'dnd': status = '⛔Не беспокоить'
    if str(member.status) == 'idle': status = '🌙Отошёл'
    if str(member.status) == 'invisible': status = '🖤Неведимка'
    if str(member.status) == 'online': status = '💚Онлайн'
    if str(member.status) == 'offline': status = '🖤Офлайн'

    emb = disnake.Embed(title=f"Профиль пользователя: ```{member}```", color=disnake.Color.dark_gold())
    emb.add_field(name="Статус:", value=f"```{status}```")
    emb.add_field(name="Самая высокая роль:", value=f"```{member.top_role}```")
    emb.add_field(name="Аккаунт зарегестрирован:", value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:D>")
    emb.set_author(name="by 『🌙』gh0st", url="https://discord.com/api/oauth2/authorize?client_id=1013189601025871874&permissions=8&scope=bot%20applications.commands")
    emb.set_footer(icon_url=f'{member.avatar}')
    emb.set_thumbnail(member.avatar)

    await inter.send(embed=emb, ephemeral=True)

# Server command
@bot.slash_command(title="Сервер", description="Статистика сервера")
async def server(inter: disnake.AppCmdInter):
    if str(inter.guild.verification_level) == 'none': vLevel = 'Отсутствует'
    if str(inter.guild.verification_level) == 'low': vLevel = 'Низкий'
    if str(inter.guild.verification_level) == 'medium': vLevel = 'Средний'
    if str(inter.guild.verification_level) == 'high': vLevel = 'Высокий'
    if str(inter.guild.verification_level) == 'extreme': vLevel = 'Очень высокий'
    emb = disnake.Embed(color = disnake.Color.dark_gold(), title = f'Информация о сервере ```{inter.guild.name}```')
    emb.add_field(
        name = '```Участники:```',
        value = 'Всего: **{}**\nЛюдей: **{}**\nБотов: **{}**'.format(
            len(inter.guild.members),
            len([m for m in inter.guild.members if not m.bot]),
            len([m for m in inter.guild.members if m.bot])
        )
    )
    emb.add_field(
        name = '```По статусам:```',
        value = 'В сети: **{}**\nНе активен: **{}**\nНе беспокоить: **{}**\nНе в сети: **{}**'.format(
            len([m for m in inter.guild.members if str(m.status) == 'online']),
            len([m for m in inter.guild.members if str(m.status) == 'idle']),
            len([m for m in inter.guild.members if str(m.status) == 'dnd']),
            len([m for m in inter.guild.members if str(m.status) == 'offline'])
        )
    )
    emb.add_field(
        name = '```Каналы:```',
        value = 'Всего: **{}**\nТекстовых: **{}**\nГолосовых: **{}**'.format(
            len(inter.guild.channels),
            len(inter.guild.text_channels),
            len(inter.guild.voice_channels)
        )
    )
    emb.add_field(
        name = 'Владелец:',
        value = f'```{inter.guild.owner}```'
    )
    emb.add_field(
        name = 'Уровень проверки:',
        value = f"```{vLevel}```"
    )
    emb.add_field(
        name = 'Дата создания:',
        value = '<t:{}:D>'.format(int(time.mktime(inter.guild.created_at.timetuple())))
    )
    emb.set_footer(text = f'ID: {inter.guild.id}')
    await inter.send(embed = emb, ephemeral=True)

@bot.command()
async def invite(ctx, server_id: int):
    guild = bot.get_guild(server_id)
    invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
    await ctx.send(f"https://discord.gg/{invite.code}")

@bot.slash_command(description="Очистка сообщений")
@commands.has_permissions(administrator=True, moderate_members=True)
async def clear(inter: disnake.AppCmdInter, amount: int):
    if amount is None:
        e = disnake.Embed(title='EROR $40032', description='Вы не указали число удалёных сообщений')
    if amount <= 0:
        e = disnake.Embed(title = 'EROR $40033', description=f'Нельзя очистить меньше нуля. Ваше значение: {amount}' ,color = disnake.Color.dark_gold())
    elif amount == None:
        e = disnake.Embed(title='EROR $40033', description='Вы не указали значение очистки.', color = disnake.Color.dark_gold())
    else:
        message = await inter.channel.purge(limit=amount)
        e = disnake.Embed(title = 'Очистка прошла... Удачно!',  description=f'{inter.author.mention} очистил {amount} сообщений.', color = disnake.Color.dark_gold())
    await inter.send(embed=e, ephemeral=True)


@bot.slash_command(description="Меню команд бота")
async def menu(inter: disnake.AppCmdInter):
    select = Select(placeholder="Выбери список команд!" ,options=[
        disnake.SelectOption(emoji="💙" ,label="Модератор-команды", description="Показывает все модер команды бота", value="0x1"),
        disnake.SelectOption(emoji="💚" ,label="Економические команды", description="Показывает все економические команды", value="0x2"),
        disnake.SelectOption(emoji="🤍" ,label="Фанни команды", description="Показывает все фанни команды", value="0x3"),
        disnake.SelectOption(emoji="🕴", label="DG-shop команды", description="Магазин DG-shop, команды.", value="0x4"),
        disnake.SelectOption(emoji="🌌", label="Настройка", description="Настройка экономики, рп и много чего!", value="0x5")
    ])
    async def my_callback(interaction):
        if select.values[0] == "0x1":
            await interaction.response.edit_message(embed=disnake.Embed(title = "Модератор команды", description= moderator_commands, color=disnake.Color.dark_gold()), view=view)
        if select.values[0] == "0x2":
            await interaction.response.edit_message(embed=disnake.Embed(title = "Економические команды", description= economy_commands, color=disnake.Color.dark_gold()), view=view)
        if select.values[0] == "0x3":
            await interaction.response.edit_message(embed=disnake.Embed(title = "Фанни команды", description=config.funny_commands, color=disnake.Color.dark_gold()), view=view)
        if select.values[0] == "0x4":
            await interaction.response.edit_message(embed=disnake.Embed(title="DG-shop", description=config.dgshop_commands, color=disnake.Color.dark_gold()), view=view)
        if select.values[0] == "0x5":
            await interaction.response.edit_message(embed=disnake.Embed(title="Настройка", description=config.help_commands, color=disnake.Color.dark_gold()), view=view)

    select.callback = my_callback
    view = View()
    view.add_item(select)

    await inter.send(embed=disnake.Embed(title='Меню команд', description='Меню всех команд бота', color=disnake.Color.dark_gold()), view=view, ephemeral=True)

@bot.slash_command(description="Показывает всю инфу о боте")
async def botinfo(inter: disnake.AppCmdInter):
    emb = disnake.Embed(title="Бот инфо", description="Информация про бота", color=disnake.Color.dark_gold())
    emb.add_field(name="Пинг:", value=f"{bot.user.mention}", inline=True)
    emb.add_field(name="Создатель бота:", value="**sn0w.gh0st1k#0755**", inline=True)
    emb.add_field(name="Команда меню команд:", value="**&menu** или **/menu**", inline=True)
    emb.add_field(name="О боте:", value="Сам бот назвалься в честь учасника групы 1-4-1 солдата Ghost. Сам ник создателя тоже был придуман от его имени.")
    emb.set_author(url="https://github.com/gh0st1k", name="GitHub создателя")
    await inter.send(embed=emb, ephemeral=True)



@bot.slash_command(description="Выдает предупреждение пользователю")
async def warn(inter: disnake.AppCmdInter, member: disnake.Member,*, reason: str):
    if cursor.execute(f"SELECT warns FROM economy WHERE member_id = {member.id}") > 4:
        await inter.send(embed=disnake.Embed(title="4 варна", description="Пользователь имеет 4 варна, поетому отправляеться в БАН! На 30 минут", color=disnake.Color.dark_gold()))
        await member.ban(delete_message_days=15)

bot.run(TOKEN)