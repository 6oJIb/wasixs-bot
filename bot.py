# from VoiceSystem import VoiceSystem
from PunishedSystem import PunishedSystem

import disnake
from disnake.ext import commands

# import asyncio
# import json
import os

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all(), test_guilds=[1534901683690274916, 1385567845089542204])
# activeVoices = []

@bot.event
async def on_ready():
    print(f"[{bot.user.name}({bot.user.id}] loaded")
    # print("--------------------------------------------------")


@bot.event
async def on_slash_command_error(inter: disnake.AppCmdInter, error: Exception):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole, commands.MissingPermissions)):
        await inter.response.send_message("You don't have permission to do that", ephemeral=True)
    else:
        print(f"Unhandled error: {error}")
        await inter.send("An unexpected error occurred.", ephemeral=True)


# region VoiceCreator Logic
# @bot.slash_command(name="set-voice-category", description="Set category for created voices")
# async def SetVoiceCategory(inter, channel: disnake.CategoryChannel):
#     with open("data/config.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     data["category_id"] = channel.id

#     with open("data/config.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

#     await inter.response.send_message(f"Voice category set to [{channel.mention}]!", ephemeral=True)


# @bot.slash_command(name="add-voicecreator", description="Set up a voice channel that creates voice channels")
# async def AddVoiceCreator(inter, channel: disnake.VoiceChannel, mode: str):
#     if mode not in VoiceSystem.GetVCREmojis():
#         await inter.response.send_message(
#             f"Invalid mode. Please choose from {', '.join(VoiceSystem.GetVCREmojis().keys())}",
#             ephemeral=True
#         )
#         return

#     VoiceSystem.SetVCRMode(channel, mode)

#     await inter.response.send_message(f"Voice creator set in [{channel.mention}] for mode [{mode}]!", ephemeral=True)


# @bot.slash_command(name="delete-voicecreator", description="The channel will not create new channels")
# async def DeleteVoiceCreator(inter, channel: disnake.VoiceChannel):
#     with open("data/VCModes.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     del data[str(channel.id)]

#     with open("data/VCModes.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

#     await inter.response.send_message(f"Voice creator deleted!", ephemeral=True)


# @bot.slash_command(name="voicecreators", description="Send voice creators list")
# async def SendVoiceCreatorsList(inter):
#     with open("data/VCModes.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     if not data:
#         await inter.response.send_message("No voice creators found.", ephemeral=True)
#         return

#     embed = disnake.Embed(title="Voice Creators", color=disnake.Color.blue())
#     for channel_id, mode in data.items():
#         channel = bot.get_channel(int(channel_id))
#         if channel:
#             embed.add_field(name=f"{channel.name} [{channel.id}]", value=f"Mode: {mode}", inline=False)

#     await inter.response.send_message(embed=embed, ephemeral=True)


# @bot.event
# async def on_voice_state_update(member: disnake.Member, before, after: disnake.VoiceState):
#     if before.channel is not None:
#         if before.channel.id in activeVoices:
#             if len(before.channel.members) == 0:
#                 activeVoices.remove(before.channel.id)
#                 try:
#                     await before.channel.delete()
#                 except disnake.NotFound:
#                     pass

#     if after.channel is not None:
#         ch: disnake.VoiceChannel = after.channel
#         id: int = ch.id
        
#         if VoiceSystem.IsVoiceCreatorExist(ch):
#             with open("data/config.json", "r", encoding="utf-8") as f:
#                 config = json.load(f)

#             category: disnake.CategoryChannel = bot.get_channel(config["category_id"])
#             if category is None:
#                 await member.send("The voice category is not found!")
#                 return

#             new_channel = await after.channel.clone(
#                 category=category,
#                 name=f"{ch.name} - {VoiceSystem.GetVoiceNumber(ch.name, category)}",
#                 user_limit=99,
#                 position=len(category.channels)
#             )

#             activeVoices.append(new_channel.id)
#             route = disnake.http.Route("PUT", "/channels/{channel_id}/voice-status", channel_id=new_channel.id)
#             await bot.http.request(route, json={"status": VoiceSystem.GetVoiceCreatorEmoji(new_channel)})
#             await asyncio.sleep(0.1)

#             try:
#                 await member.move_to(new_channel)
#             except:
#                 await asyncio.sleep(0.1)
#                 await member.move_to(new_channel)


# @bot.event
# async def on_guild_channel_delete(channel):
#     if channel.id in activeVoices:
#         activeVoices.remove(channel.id)
# endregion

# region Punished Logic
@bot.slash_command(name="add-punished", description="Add user to punished list")
async def AddUserToPunishedList(inter, member: disnake.Member, reason: str):
    if len(reason) <= 0:
        await inter.response.send_message(
            f"Please provide a valid reason",
            ephemeral=True
        )
        return

    PunishedSystem.AddPunished(member, reason)
    await inter.response.send_message("User added to punished list", ephemeral=True)


@bot.slash_command(name="remove-punished", description="Remove user from punished list")
async def RemoveUserFromPunishedList(inter, member: disnake.Member, reason: str):
    if len(reason) <= 0:
        await inter.response.send_message(
            f"Please provide a valid reason",
            ephemeral=True
        )
        return

    PunishedSystem.RemovePunished(member, reason)
    await inter.response.send_message("User removed from punished list", ephemeral=True)


@bot.slash_command(name="list-punished", description="Shows people with 'Отброс' role")
async def SendPunishedList(inter):
    trashList = PunishedSystem.GetPunished()

    if len(trashList) == 0:
        await inter.response.send_message(f"List is empty", ephemeral=True)
        return

    description = ""
    for i, kv in enumerate(trashList.items()):
        k, v = kv
        description += f"**{i + 1}.** **{k}** **-** `{v}`\n"

    embed = disnake.Embed(
        title="🗑️ Punished List",
        description=description,
        color=0x00BFFF
    )

    await inter.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(name="clear-punished", description="Clears punished data")
async def ClearPunishedList(inter):
    PunishedSystem.ClearPunishedList()
    await inter.response.send_message("Punished cleared", ephemeral=True)
# endregion

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)