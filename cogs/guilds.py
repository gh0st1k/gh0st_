import disnake
from disnake.ext import commands
from disnake.ui import TextInput, View, Button
from main import bot

@bot.slash_command(description="Создает клан")
async def guild(inter: disnake.AppCmdInter):
    await inter.response.send_modal(modal=MyModal())
        
class MyModal(disnake.ui.Modal):
    def __init__(self):

            guild_general_member = disnake.ui.TextInput(
                label="Ваш дискорд",
                placeholder="Wumpus#0755",
                custom_id="General in guild",
                style=disnake.TextInputStyle.short,
                max_length=35,
                required=True,
            ),

            guild_members = disnake.ui.TextInput(
                label="Учасники клана",
                style=disnake.TextInputStyle.long,
                placeholder="sn0w.gh0st1k#0755",
                custom_id="Members in guild",
            ),

            guild_name = disnake.ui.TextInput(
                label="Название клана",
                placeholder="ПДБ, Сила Воли, Украина!",
                custom_id="Guild Title",
                style=TextInputStyle.short,
                max_length=15,
                min_length=3,
                required=True,
            ),

            guild_descr = disnake.ui.TextInput(
                label="Описание",
                placeholder="Мой клан лучший!",
                custom_id="Description guild",
                style=TextInputStyle.paragraph,
                required=False,
            ),

            super().__init__(
            title="Клан",
            custom_id=f"Клан",
            components=guild_name + guild_descr + guild_general_member + guild_members,
            )
            
    async def callback(self, interaction: disnake.ModalInteraction):
        embed = disnake.Embed(title="Успешно!", description="Ваш клан:", color=disnake.Color.dark_gold())
        for key, value in interaction.text_values.items():
            embed.add_field(
            name=key.capitalize(),
            value=value[:1024],
            inline=False,
        )

        await interaction.response.send_message(embed=embed)
        cursor.execute(f"INSERT INTO guilds VALUES ('{embed}', '{None}', '{None}', '{None}', '{None}')")
        time.sleep(120 * 120)
        await interaction.response.send_message(embed=disnake.Embed(title="Вновь можно создать клан!", description="Создавай клан! 4 часа прошло!"))