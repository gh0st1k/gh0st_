import disnake
from disnake.ext import commands
from disnake.ui import Select, Button, View
from disnake import TextInput, TextInputStyle

import config
import sqlite3
import random
import time
from time import sleep

connection = sqlite3.connect('base.db')
cursor = connection.cursor()

class settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Настройка модерации")
    @commands.has_guild_permissions(administrator=True, moderate_members=True)
    async def moderator_settings(self,* ,inter: disnake.AppCmdInter):
        view=Ms(guild=disnake.Guild)

        embed = disnake.Embed(title="Настройка модерации", description="Настройка модератор команд. Например: Включение **авто модерации на сылки** и так далее", color=disnake.Color.dark_gold())
        await inter.send(embed=embed, view=view, ephemeral=True)
        
class Ms(View):
    def __init__(self, guild: disnake.Guild):
        super().__init__()
        self.guild = guild

    @disnake.ui.button(label="Авто-модерация сыллок", style=disnake.ButtonStyle.red, custom_id="AMs")
    async def AMs_button_callback(self, button: disnake.Button, interaction: disnake.MessageInteraction):
        self.AMs_button_callback.style = disnake.ButtonStyle.green
        view1 = Ms(guild=disnake.Guild)
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{interaction.guild.id}"(
            AVs TEXT,
            AVp TEXT,
            LG TEXT
        )""")
        embed = disnake.Embed(title="Настройка модерации", description="Настройка модерации команд", color=disnake.Color.dark_gold())
        embed.add_field(name="🟢", value="Включена настойка")
        embed.add_field(name="🔴", value="Выключена настройка")
        cursor.execute(f"UPDATE '{interaction.guild.id}' SET AVs = AVs + '+'")
        await interaction.response.edit_message(embed=embed,view = self)
    




def setup(client):
    client.add_cog(settings(client))