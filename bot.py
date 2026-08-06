import asyncio
import os
import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all(), test_guilds=[1534901683690274916, 1385567845089542204])
activeVoices = []
voiceStatuses = {
    1534927334371754116: ["default", "<:default1:1535021935430209536>" + "<:default2:1535021950181707866>" + "<:default3:1535021962970136768>" + "<:default4:1535021971115475014>"],
    1535025690704089161: ["vip", "<:vip1:1535024198278447206>" + "<:vip2:1535024308106166332>"],
    1535025706277273702: ["admin", "<:admin1:1535024872512688288>" + "<:admin2:1535024888975327322>" + "<:admin3:1535024899184267394>" + "<:admin4:1535024909326221724>"]
}

# class VoiceControlPanel(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(label="Изменить имя голосового канала", style=disnake.ButtonStyle.primary)
#     async def button_callback1(self, button, interaction):
#         await interaction.response.send_message("Кнопка нажата!", ephemeral=True)

#     @disnake.ui.button(label="Масимальное количество участников", style=disnake.ButtonStyle.primary)
#     async def button_callback2(self, button, interaction):
#         await interaction.response.send_message("Кнопка нажата!", ephemeral=True)

#     @disnake.ui.button(label="Скрыть от всех голосовой канал", style=disnake.ButtonStyle.primary)
#     async def button_callback3(self, button, interaction):
#         await interaction.response.send_message("Кнопка нажата!", ephemeral=True)
# embed = disnake.Embed(
            #     title="Панель управления голосовым каналом",
            #     description=f"Канал [{new_channel.mention}]\nВладелец [{member.mention}]",
            #     color=disnake.Color.light_grey()
            # )
            # embed.add_field(name="Информация", value="Канал фывфвы", inline=False)
            # embed.add_field(name="фывфвы", value="ввв фывфвы", inline=False)
            # embed.set_footer(text="wasixs bot")
            # await new_channel.send(embed=embed, view=VoiceControlPanel())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("--------------------------------------------------")

@bot.slash_command()
async def set_voice_creator(inter, channel: disnake.VoiceChannel, mode: str):
    for key, value in voiceStatuses.items():
        mode_name, emoji_string = value
        if mode_name == mode:
            voiceStatuses[channel.id] = voiceStatuses.pop(key)

            await inter.response.send_message(
                f"[{mode}] Voice creator set in [{channel.mention}]!", ephemeral=True)
            return

    await inter.response.send_message(f"Mode [{mode}] not found!", ephemeral=True)

@bot.event
async def on_voice_state_update(member: disnake.Member, before, after: disnake.VoiceState):
    if before.channel is not None:
        if before.channel.id in activeVoices:
            if len(before.channel.members) == 0:
                activeVoices.remove(before.channel.id)
                try:
                    await before.channel.delete()
                except disnake.NotFound:
                    pass

    if after.channel is not None:
        id: int = after.channel.id
        if id in voiceStatuses.keys():
            category = after.channel.category
            numbers = []
            for ch in category.channels:
                if ch.name.startswith("voice "):
                    try:
                        num = int(ch.name.split(" ")[1])
                        numbers.append(num)
                    except:
                        pass

            next_number = max(numbers) + 1 if numbers else 1

            new_channel = await after.channel.clone(name=f"voice {next_number}", user_limit=99, position=len(category.channels))
            activeVoices.append(new_channel.id)

            await asyncio.sleep(0.1)
            try:
                await member.move_to(new_channel)
            except:
                await asyncio.sleep(0.1)
                await member.move_to(new_channel)

            route = disnake.http.Route("PUT", "/channels/{channel_id}/voice-status", channel_id=new_channel.id)
            await bot.http.request(route, json={"status": voiceStatuses[id][1]})

@bot.event
async def on_guild_channel_delete(channel):
    if channel.id in activeVoices:
        activeVoices.remove(channel.id)         

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)